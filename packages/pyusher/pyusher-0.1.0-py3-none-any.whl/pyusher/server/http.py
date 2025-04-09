# usher/server/http.py

import argparse
import asyncio
import logging
import os
import signal
import sys
import threading

import uvicorn
from fastapi import FastAPI, Query, HTTPException, Path, Body
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel
from typing import Any, Dict, Optional, Callable

import structlog

# Import your runner and exceptions
from .runner import AgentRunner, TaskStatusEnum
from .exceptions import UnknownAgentError, AgentBusyError

# Initialize the logger
log = structlog.get_logger("usher.server.http")

def create_app() -> FastAPI:
    app = FastAPI()
    loop = asyncio.get_event_loop()
    agent_runner = AgentRunner(loop=loop)
    # agent_runner = AgentRunner()

    class RunTaskRequest(BaseModel):
        task: Dict[str, Any]  # The inputs for the agent's act method

    class UserInputModel(BaseModel):
        user_input: Any

    class SensitiveUserInputModel(BaseModel):
        sensitive_user_input: Any

    @app.post("/tasks")
    async def run_task(request: RunTaskRequest):
        try:
            task_id = agent_runner.start_agent(request.task)
        except Exception as e:
            log.error(f"Error starting task: {e}")
            raise HTTPException(status_code=500, detail=str(e))
        return {"task_id": task_id}

    @app.post("/tasks/{task_id}/stop")
    async def stop_task(task_id: str = Path(...)):
        try:
            agent_runner.stop_agent(task_id)
        except UnknownAgentError:
            raise HTTPException(status_code=404, detail="Task not found")
        return {"status": "Task stopped"}

    @app.post("/tasks/{task_id}/pause")
    async def pause_task(task_id: str = Path(...)):
        try:
            agent_runner.pause_agent(task_id)
        except UnknownAgentError:
            raise HTTPException(status_code=404, detail="Task not found")
        except NotImplementedError:
            raise HTTPException(status_code=501, detail="Pause functionality not implemented by the agent")
        return {"status": "Task paused"}

    @app.get("/tasks/{task_id}/logs")
    async def get_logs(
            task_id: str,
            from_beginning: bool = Query(False, description="Stream logs from the beginning"),
            stream: bool = Query(True, description="Stream logs if True, else return immediately"),
    ):
        try:
            task_status = agent_runner.get_task_status(task_id)
        except UnknownAgentError as e:
            raise HTTPException(status_code=404, detail=str(e))

        # If stream is True, return a streaming response
        if stream:
            log_generator = agent_runner.stream_logs(task_id, from_beginning=from_beginning)
            return StreamingResponse(
                log_generator,
                media_type="text/event-stream"
            )
        else:
            # If the task is completed or not running, return all logs immediately
            if task_status in [
                TaskStatusEnum.COMPLETED,
                TaskStatusEnum.FAILED,
                TaskStatusEnum.STOPPED,
            ]:
                logs = agent_runner.task_logs.get(task_id, [])
                return JSONResponse(content={"logs": logs})
            else:
                # If the task is still running and stream is False, you may decide how to handle it
                # Here, we return the logs collected so far
                logs = agent_runner.task_logs.get(task_id, [])
                return JSONResponse(content={"logs": logs})

    @app.post("/tasks/{task_id}/on_user_input")
    async def on_user_input(task_id: str = Path(...), user_input_model: UserInputModel = Body(...)):
        try:
            agent_runner.send_user_input(task_id, user_input_model.user_input)
        except UnknownAgentError:
            raise HTTPException(status_code=404, detail="Task not found")
        except AgentBusyError:
            raise HTTPException(status_code=400, detail="Agent is not awaiting user input")
        return {"status": "User input sent"}

    @app.post("/tasks/{task_id}/on_sensitive_user_input")
    async def on_sensitive_user_input(task_id: str = Path(...), sensitive_user_input_model: SensitiveUserInputModel = Body(...)):
        try:
            agent_runner.send_sensitive_user_input(task_id, sensitive_user_input_model.sensitive_user_input)
        except UnknownAgentError:
            raise HTTPException(status_code=404, detail="Task not found")
        except AgentBusyError:
            raise HTTPException(status_code=400, detail="Agent is not awaiting sensitive user input")
        return {"status": "Sensitive user input sent"}

    @app.get("/health")
    async def health_check():
        # Implement health check logic as needed
        return {"status": "OK"}

    @app.get("/tasks/{task_id}/user_input_request")
    async def latest_user_input_request(task_id: str = Path(...)):
        try:
            prompt = agent_runner.get_latest_user_input_request(task_id)
            if prompt is None:
                return {"status": "No pending user input request"}
            else:
                return {"prompt": prompt}
        except UnknownAgentError:
            raise HTTPException(status_code=404, detail="Task not found")

    @app.get("/tasks/{task_id}/status")
    async def get_status(task_id: str = Path(...)):
        try:
            status = agent_runner.get_task_status(task_id)
            return {"status": status}
        except UnknownAgentError:
            raise HTTPException(status_code=404, detail="Task not found")

    return app

def signal_ignore(signum: Any, frame: Any) -> None:
    # Log the signal and ignore it
    log.warning(f"Got a signal to exit, ignoring it... (signal: {signal.Signals(signum).name})")

def signal_set_event(event: threading.Event) -> Callable[[Any, Any], None]:
    def _signal_set_event(signum: Any, frame: Any) -> None:
        event.set()
    return _signal_set_event

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Usher HTTP server")
    parser.add_argument(
        "-v", "--version", action="store_true", help="Show version and exit"
    )
    parser.add_argument(
        "--host",
        type=str,
        default="0.0.0.0",
        help="Host to bind to",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.getenv("PORT", "5000")),
        help="Port to bind to",
    )
    parser.add_argument(
        "--log-level",
        type=str,
        default=os.environ.get("USHER_LOG_LEVEL", "INFO"),
        help="Logging level",
    )
    parser.add_argument(
        "--await-explicit-shutdown",
        action="store_true",
        help="Wait for a request to /shutdown before exiting",
    )

    args = parser.parse_args()

    # Handle version argument
    if args.version:
        print("usher.server.http version X.Y.Z")  # Replace with actual version
        sys.exit(0)

    # Configure logging
    log_level = logging.getLevelName(args.log_level.upper())
    logging.basicConfig(level=log_level)
    # Additional logging configuration if needed

    # Create the FastAPI app
    app = create_app()

    # Handle graceful shutdown
    shutdown_event = threading.Event()

    if args.await_explicit_shutdown:
        signal.signal(signal.SIGTERM, signal_ignore)
    else:
        signal.signal(signal.SIGTERM, signal_set_event(shutdown_event))

    # Configure and start the server
    uvicorn_config = uvicorn.Config(
        app,
        host=args.host,
        port=args.port,
        log_level=args.log_level.lower(),
    )

    server = uvicorn.Server(config=uvicorn_config)

    def run_server():
        asyncio.run(server.serve())

    server_thread = threading.Thread(target=run_server)
    server_thread.start()

    try:
        shutdown_event.wait()
    except KeyboardInterrupt:
        pass

    server.should_exit = True
    server_thread.join()
