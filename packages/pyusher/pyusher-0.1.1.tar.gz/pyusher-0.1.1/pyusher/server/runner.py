# from .eventtypes import *
# from multiprocessing.connection import Connection
# from threading import Thread
# from typing import Any, Callable, Optional, Dict
#
#
# class AgentRunner:
#     def __init__(self, connection: Connection):
#         self.connection = connection
#         self.callbacks: Dict[type, Callable[[Event], None]] = {}
#         self.running = True
#         self.thread = Thread(target=self.listen_to_worker, daemon=True)
#         self.thread.start()
#
#     def listen_to_worker(self):
#         while self.running:
#             try:
#                 message = self.connection.recv()
#                 if isinstance(message, Envelope):
#                     event = message.event
#                     event_type = type(event)
#                     if event_type in self.callbacks:
#                         self.callbacks[event_type](event)
#                     if isinstance(event, AgentDone):
#                         self.running = False
#                 else:
#                     # Handle unexpected messages
#                     pass
#             except EOFError:
#                 break
#
#     def send_inputs(self, inputs: Dict[str, Any]):
#         self.connection.send(inputs)
#
#     def send_user_input(self, user_input: Any):
#         self.connection.send(Envelope(event=UserInput(input_data=user_input)))
#
#     def register_callback(self, event_type: Any, callback: Callable[[Event], None]):
#         self.callbacks[event_type] = callback
#
#     def stop(self):
#         self.running = False
#         self.connection.close()
# agent_runner/runner.py

# import threading
# import uuid
# from typing import Any, Dict, Callable, Optional
# from .worker import Worker
# from .eventtypes import Envelope, AgentOutput, AgentLog, AgentRequestInput, Done, UserInput
# from .exceptions import AgentRunnerError, AgentBusyError, UnknownAgentError
#
# class AgentRunner:
#     def __init__(self):
#         self.active_workers: Dict[str, Worker] = {}
#         self.callbacks: Dict[str, Dict[str, Callable]] = {}
#         self.lock = threading.Lock()
#
#     def start_agent(self, agent_path: str, inputs: Dict[str, Any]) -> str:
#         tag = str(uuid.uuid4())
#         worker = Worker(agent_path)
#         worker.subscribe(lambda envelope: self._handle_event(tag, envelope))
#         with self.lock:
#             self.active_workers[tag] = worker
#         worker.start()
#         worker.send_event(Envelope(event=AgentInput(payload=inputs), tag=tag))
#         return tag
#
#     def _handle_event(self, tag: str, envelope: Envelope):
#         event = envelope.event
#         if isinstance(event, AgentOutput):
#             # Handle output
#             if 'output' in self.callbacks.get(tag, {}):
#                 self.callbacks[tag]['output'](event.output)
#         elif isinstance(event, AgentLog):
#             # Handle logs
#             if 'log' in self.callbacks.get(tag, {}):
#                 self.callbacks[tag]['log'](event.message)
#         elif isinstance(event, AgentRequestInput):
#             # Handle input request
#             if 'input_request' in self.callbacks.get(tag, {}):
#                 self.callbacks[tag]['input_request'](event.prompt)
#         elif isinstance(event, Done):
#             # Handle agent completion
#             if 'done' in self.callbacks.get(tag, {}):
#                 self.callbacks[tag]['done'](event)
#             with self.lock:
#                 if tag in self.active_workers:
#                     del self.active_workers[tag]
#                 if tag in self.callbacks:
#                     del self.callbacks[tag]
#
#     def send_user_input(self, tag: str, user_input: Any):
#         with self.lock:
#             if tag not in self.active_workers:
#                 raise UnknownAgentError(f"No agent running with tag {tag}")
#             worker = self.active_workers[tag]
#         worker.send_event(Envelope(event=UserInput(input_data=user_input), tag=tag))
#
#     def register_callback(self, tag: str, event_type: str, callback: Callable):
#         with self.lock:
#             if tag not in self.callbacks:
#                 self.callbacks[tag] = {}
#             self.callbacks[tag][event_type] = callback
#
#     def stop_agent(self, tag: str):
#         with self.lock:
#             if tag in self.active_workers:
#                 worker = self.active_workers.pop(tag)
#                 worker.shutdown()
#             if tag in self.callbacks:
#                 del self.callbacks[tag]


# agent_runner/runner.py

import threading
import asyncio
import uuid
from typing import Any, Dict, Optional
from .worker import Worker
from .eventtypes import (
    Envelope,
    AgentOutput,
    AgentLog,
    AgentRequestInput,
    AgentRequestSensitiveInput,
    Done,
    UserInput,
    SensitiveUserInput,
    Cancel,
    Pause, AgentInput,
)
from .exceptions import AgentBusyError, UnknownAgentError


class TaskStatusEnum:
    PENDING = 'PENDING'
    RUNNING = 'RUNNING'
    PAUSED = 'PAUSED'
    STOPPED = 'STOPPED'
    COMPLETED = 'COMPLETED'
    FAILED = 'FAILED'


class AgentRunner:
    def __init__(self, loop):
        self.loop = loop
        self.active_tasks: Dict[str, Worker] = {}
        self.lock = threading.Lock()
        self.task_statuses: Dict[str, str] = {}
        self.task_logs: Dict[str, list] = {}
        self.user_input_prompts: Dict[str, Optional[str]] = {}
        self.log_streams: Dict[str, asyncio.Queue] = {}

    def start_agent(self, inputs: Dict[str, Any]) -> str:
        task_id = str(uuid.uuid4())
        worker = Worker()
        worker.subscribe(lambda envelope: self._handle_event(task_id, envelope))
        with self.lock:
            self.active_tasks[task_id] = worker
            self.task_statuses[task_id] = TaskStatusEnum.RUNNING
            self.task_logs[task_id] = []
            self.user_input_prompts[task_id] = None
            self.log_streams[task_id] = asyncio.Queue()
        worker.start()
        worker.send_event(Envelope(event=AgentInput(payload=inputs), tag=task_id))
        return task_id

    def _handle_event(self, task_id: str, envelope: Envelope):
        event = envelope.event
        # Log every event received except for AgentLog events
        if not isinstance(event, AgentLog):
            log_message = f"Received event: {event}"
            self.task_logs[task_id].append(log_message)
            asyncio.run_coroutine_threadsafe(
                self.log_streams[task_id].put(log_message), self.loop
            )

        if isinstance(event, AgentOutput):
            # Handle output event (could store output if needed)
            pass
        elif isinstance(event, AgentLog):
            # Handle logs
            log_message = event.message
            self.task_logs[task_id].append(log_message)
            asyncio.run_coroutine_threadsafe(
                self.log_streams[task_id].put(log_message), self.loop
            )
        elif isinstance(event, AgentRequestInput):
            # Handle agent requesting user input
            self.user_input_prompts[task_id] = event.prompt
        elif isinstance(event, AgentRequestSensitiveInput):
            # Handle agent requesting sensitive user input
            self.user_input_prompts[task_id] = event.prompt  # Could differentiate if needed
        elif isinstance(event, Done):
            # Handle task completion
            if event.error:
                self.task_statuses[task_id] = TaskStatusEnum.FAILED
            elif event.canceled:
                self.task_statuses[task_id] = TaskStatusEnum.STOPPED
            else:
                self.task_statuses[task_id] = TaskStatusEnum.COMPLETED
            # Clean up
            self._cleanup_task(task_id)

    def _cleanup_task(self, task_id: str):
        with self.lock:
            if task_id in self.active_tasks:
                del self.active_tasks[task_id]
            if task_id in self.user_input_prompts:
                del self.user_input_prompts[task_id]
            # if task_id in self.log_streams:
            #     del self.log_streams[task_id]

    def stop_agent(self, task_id: str):
        with self.lock:
            if task_id not in self.active_tasks:
                raise UnknownAgentError(f"Task ID {task_id} not found")
            worker = self.active_tasks[task_id]
        worker.send_event(Envelope(event=Cancel(), tag=task_id))

    def pause_agent(self, task_id: str):
        with self.lock:
            if task_id not in self.active_tasks:
                raise UnknownAgentError(f"Task ID {task_id} not found")
            worker = self.active_tasks[task_id]
        worker.send_event(Envelope(event=Pause(), tag=task_id))

    def send_user_input(self, task_id: str, user_input: Any):
        with self.lock:
            if task_id not in self.active_tasks:
                raise UnknownAgentError(f"Task ID {task_id} not found")
            if self.user_input_prompts.get(task_id) is None:
                raise AgentBusyError("Agent is not awaiting user input")
            worker = self.active_tasks[task_id]
            self.user_input_prompts[task_id] = None
        worker.send_event(Envelope(event=UserInput(input_data=user_input), tag=task_id))

    def send_sensitive_user_input(self, task_id: str, sensitive_input: Any):
        with self.lock:
            if task_id not in self.active_tasks:
                raise UnknownAgentError(f"Task ID {task_id} not found")
            if self.user_input_prompts.get(task_id) is None:
                raise AgentBusyError("Agent is not awaiting sensitive user input")
            worker = self.active_tasks[task_id]
            self.user_input_prompts[task_id] = None
        worker.send_event(Envelope(event=SensitiveUserInput(input_data=sensitive_input), tag=task_id))

    async def stream_logs(self, task_id: str, from_beginning: bool = False):
        with self.lock:
            if task_id not in self.task_logs:
                raise UnknownAgentError(f"Task ID {task_id} not found")
            task_status = self.task_statuses.get(task_id)
            log_queue = self.log_streams.get(task_id)
            stored_logs = self.task_logs[task_id].copy()  # Copy to prevent mutation during iteration

        # If from_beginning is True, yield all stored logs first
        if from_beginning:
            for log_message in stored_logs:
                yield log_message

        # If the task is still running, continue streaming logs
        if log_queue and task_status in [
            TaskStatusEnum.PENDING,
            TaskStatusEnum.RUNNING,
            TaskStatusEnum.PAUSED,
        ]:
            while True:
                try:
                    log_message = await log_queue.get()
                    yield log_message
                    # If task status changes to a terminal state, break the loop
                    with self.lock:
                        current_status = self.task_statuses.get(task_id)
                    if current_status in [
                        TaskStatusEnum.COMPLETED,
                        TaskStatusEnum.FAILED,
                        TaskStatusEnum.STOPPED,
                    ]:
                        break
                except asyncio.CancelledError:
                    break
        else:
            # Task has completed; if from_beginning is False, yield nothing
            if not from_beginning:
                # Optionally, you could yield a message indicating no more logs
                return

    def get_latest_user_input_request(self, task_id: str) -> Optional[str]:
        with self.lock:
            if task_id not in self.user_input_prompts:
                raise UnknownAgentError(f"Task ID {task_id} not found")
            return self.user_input_prompts[task_id]

    def get_task_status(self, task_id: str) -> str:
        with self.lock:
            if task_id not in self.task_statuses:
                raise UnknownAgentError(f"Task ID {task_id} not found")
            return self.task_statuses[task_id]
