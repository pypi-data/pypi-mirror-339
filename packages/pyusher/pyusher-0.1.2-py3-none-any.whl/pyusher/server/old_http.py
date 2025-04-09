import multiprocessing
from multiprocessing.connection import Connection
import uuid
from typing import Any, Dict, Optional

from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

from ..base_agent import BaseAgent
from ..load_agent import load_agent_from_ref


################################################################################
# 1. EVENT DEFINITIONS
################################################################################

class EventType:
    """Marker class so all events can be recognized."""
    pass

class RunTask(EventType):
    def __init__(self, task_id: str, instructions: str):
        self.task_id = task_id
        self.instructions = instructions

class StopTask(EventType):
    def __init__(self, task_id: str):
        self.task_id = task_id

class UserInput(EventType):
    """Parent -> Child event to supply the user input to the agent."""
    def __init__(self, task_id: str, input_value: str):
        self.task_id = task_id
        self.input_value = input_value

class RequestInput(EventType):
    """Child -> Parent event indicating the agent is waiting for user input."""
    def __init__(self, task_id: str, prompt: str):
        self.task_id = task_id
        self.prompt = prompt

class Log(EventType):
    """Child -> Parent logs."""
    def __init__(self, task_id: str, message: str):
        self.task_id = task_id
        self.message = message

class PartialOutput(EventType):
    """Child -> Parent partial output."""
    def __init__(self, task_id: str, data: Any):
        self.task_id = task_id
        self.data = data

class TaskDone(EventType):
    """Child -> Parent final result or error."""
    def __init__(self, task_id: str, success: bool, result: Optional[Any] = None, error: str = ""):
        self.task_id = task_id
        self.success = success
        self.result = result
        self.error = error

class Shutdown(EventType):
    """Parent -> Child shutdown signal."""
    pass


################################################################################
# 2. CHILD PROCESS CODE
################################################################################

import os
import signal
import traceback
import threading


class ChildProcess(multiprocessing.Process):
    """
    The child loads the developer's agent, listens for events (RunTask, UserInput),
    and communicates back (Log, RequestInput, PartialOutput, TaskDone).
    """

    def __init__(self, conn: Connection):
        super().__init__()
        self.conn = conn
        agent_ref = os.getenv("AGENT_REF", "my_agent:MyAgent")
        self.agent_ref = agent_ref
        self.agent: Optional[BaseAgent] = None
        self._running_tasks = {}  # task_id -> something
        self._stop_signal = False

    def run(self):
        """Main loop: wait for events from parent, handle them."""

        # SIGINT can be ignored here because parent manages it.
        signal.signal(signal.SIGINT, signal.SIG_IGN)

        # 1. Read the agent ref from environment
        agent_ref = os.getenv("AGENT_REF", "my_agent:MyAgent")
        self.agent = load_agent_from_ref(agent_ref)

        if not self.agent:
            raise Exception("Couldn't load agent")

        self.agent.set_local_mode(False)  # We'll rely on the event-based user input

        # If there's a setup method, optionally call it:
        if hasattr(self.agent, "setup"):
            try:
                self.agent.setup()
            except Exception as e:
                traceback.print_exc()
                # Optionally notify parent there's a setup error, then exit
                return

        while True:
            if self.conn.poll(0.1):
                evt = self.conn.recv()
                if isinstance(evt, RunTask):
                    self._handle_run_task(evt)
                elif isinstance(evt, UserInput):
                    self._handle_user_input(evt)
                elif isinstance(evt, StopTask):
                    self._handle_stop_task(evt)
                elif isinstance(evt, Shutdown):
                    break
            # If needed, do other housekeeping
            if self._stop_signal:
                break

        self.conn.close()

    def _handle_run_task(self, evt: RunTask):
        """Start running the agent logic in a separate thread or sync."""
        def task_thread():
            task_id = evt.task_id
            instructions = evt.instructions
            try:
                # We'll do partial output or logs if the agent calls
                # get_user_input or partial output, etc.

                # A minimal run:
                self._log(task_id, f"Starting task with instructions: {instructions}")
                # maybe partial output
                # self.conn.send(PartialOutput(task_id, "some partial data"))

                self.agent.run(instructions)

                # If there's a final result we can gather:
                final_data = getattr(self.agent, "final_result", "No final result")
                self.conn.send(TaskDone(task_id, True, result=final_data))

            except Exception as e:
                traceback.print_exc()
                self.conn.send(TaskDone(task_id, False, error=str(e)))

        t = threading.Thread(target=task_thread, daemon=True)
        self._running_tasks[evt.task_id] = t
        t.start()

    def _handle_user_input(self, evt: UserInput):
        """Relay user input to the agent so that get_user_input() unblocks."""
        # Our agent's get_user_input in container mode is blocked on a queue
        self.agent.on_user_input(evt.input_value)

    def _handle_stop_task(self, evt: StopTask):
        task_id = evt.task_id
        thr = self._running_tasks.get(task_id)
        if thr:
            # The agent can optionally have a stop method
            self.agent.stop()
            self._log(task_id, f"Stopped task {task_id}")
        # we can forcibly kill the thread if needed, or rely on agent to stop

    def _log(self, task_id, msg):
        self.conn.send(Log(task_id, msg))

    def request_user_input(self, task_id: str, prompt: str):
        """If the agent calls get_user_input, we send RequestInput to the parent."""
        self.conn.send(RequestInput(task_id, prompt))


################################################################################
# 3. RUNNER: MANAGE TASKS & CONCURRENCY
################################################################################

class TaskState:
    def __init__(self, task_id: str):
        self.task_id = task_id
        self.is_done = False
        self.error = ""
        self.result = None
        self.logs = ""
        self.prompt = ""  # If waiting for user input
        self.partial_output = []

class Runner:
    """
    Manages concurrency and keeps track of tasks.
    Offers methods to start tasks, stop tasks, etc.
    """

    def __init__(self, conn: Connection, max_concurrency: int = 1):
        self.conn = conn
        self.tasks = {}  # task_id -> TaskState
        self.max_concurrency = max_concurrency
        self._lock = threading.Lock()

        # Start a background thread to consume child events
        self._stop_consumer = False
        self._consumer_thread = threading.Thread(target=self._consume_events, daemon=True)
        self._consumer_thread.start()

    def _consume_events(self):
        while not self._stop_consumer:
            if self.conn.poll(0.1):
                evt = self.conn.recv()
                self._handle_child_event(evt)

    def _handle_child_event(self, evt: EventType):
        if isinstance(evt, Log):
            st = self.tasks.get(evt.task_id)
            if st:
                st.logs += evt.message + "\n"

        elif isinstance(evt, RequestInput):
            st = self.tasks.get(evt.task_id)
            if st:
                st.prompt = evt.prompt
                # Mark that we're waiting for input
        elif isinstance(evt, PartialOutput):
            st = self.tasks.get(evt.task_id)
            if st:
                st.partial_output.append(evt.data)

        elif isinstance(evt, TaskDone):
            st = self.tasks.get(evt.task_id)
            if st:
                st.is_done = True
                st.error = evt.error
                st.result = evt.result

        # else: ignoring unknown events

    def start_task(self, instructions: str) -> str:
        with self._lock:
            # concurrency check
            running_count = sum(1 for s in self.tasks.values() if not s.is_done)
            if running_count >= self.max_concurrency:
                raise RuntimeError("Too many tasks in progress.")

            task_id = str(uuid.uuid4())
            self.tasks[task_id] = TaskState(task_id)

            self.conn.send(RunTask(task_id, instructions))
            return task_id

    def stop_task(self, task_id: str):
        self.conn.send(StopTask(task_id))

    def on_user_input(self, task_id: str, user_input: str):
        """Send the user input to the child process"""
        self.conn.send(UserInput(task_id, user_input))

    def get_status(self, task_id: str) -> Dict[str, Any]:
        """Retrieve logs, partial output, final result, or prompt."""
        st = self.tasks.get(task_id)
        if not st:
            return {"error": "No such task_id"}

        return {
            "done": st.is_done,
            "error": st.error,
            "result": st.result,
            "logs": st.logs,
            "prompt": st.prompt,
            "partial_output": st.partial_output,
        }

    def shutdown(self):
        """Shutdown the child process and the consumer thread"""
        self.conn.send(Shutdown())
        self._stop_consumer = True
        self._consumer_thread.join(timeout=3)


################################################################################
# 4. FASTAPI SERVER
################################################################################

app = FastAPI()

# We'll spawn child + runner at module load
parent_conn, child_conn = multiprocessing.Pipe()
# For now, assume user’s agent code is in 'my_agent.py'
child = ChildProcess(child_conn)
child.start()

runner = Runner(parent_conn, max_concurrency=2)

class StartTaskRequest(BaseModel):
    instructions: str

@app.post("/start_task")
def start_task(req: StartTaskRequest):
    """Begin a new agent task."""
    try:
        task_id = runner.start_task(req.instructions)
        return {"status": "started", "task_id": task_id}
    except RuntimeError as e:
        return {"error": str(e)}

class UserInputRequest(BaseModel):
    task_id: str
    user_input: str

@app.post("/on_user_input")
def on_user_input(req: UserInputRequest):
    """Provide user input to a running task."""
    runner.on_user_input(req.task_id, req.user_input)
    return {"status": "ok"}

class StopTaskRequest(BaseModel):
    task_id: str

@app.post("/stop_task")
def stop_task(req: StopTaskRequest):
    """Forcibly stop a running task."""
    runner.stop_task(req.task_id)
    return {"status": "stopping"}

@app.get("/task_status/{task_id}")
def get_status(task_id: str):
    """Get logs, partial outputs, final result, or prompt if waiting."""
    return runner.get_status(task_id)

@app.on_event("shutdown")
def shutdown_event():
    runner.shutdown()
    child.join(timeout=3)
    if child.is_alive():
        child.terminate()

################################################################################
# 5. OPTIONAL: MAIN ENTRY POINT
################################################################################

def main():
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "5000")))

if __name__ == "__main__":
    main()
