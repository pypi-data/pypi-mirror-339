# import multiprocessing
# from multiprocessing.connection import Connection
# from ..base_agent import BaseAgent
# from .eventtypes import *
# import traceback
# import sys
# from typing import Any, Dict, Optional
#
#
# class Worker(multiprocessing.Process):
#     def __init__(self, agent_class: Any, connection: Connection):
#         super().__init__()
#         self.agent_class = agent_class
#         self.connection = connection
#         self.agent: Optional[BaseAgent] = None
#
#     def run(self):
#         try:
#             self.agent = self.agent_class()
#             if hasattr(self.agent, 'setup'):
#                 self.agent.setup()
#             self.event_loop()
#         except Exception as e:
#             error_message = ''.join(traceback.format_exception_only(type(e), e))
#             self.connection.send(Envelope(event=AgentDone(error=error_message)))
#             sys.exit(1)
#
#     def event_loop(self):
#         while True:
#             message = self.connection.recv()
#             if isinstance(message, Envelope):
#                 event = message.event
#                 if isinstance(event, AgentDone):
#                     # Gracefully shutdown worker
#                     break
#                 elif isinstance(event, UserInput):
#                     # Handle user input
#                     self.agent.on_user_input(event.input_data)
#                 else:
#                     # Handle other events if necessary
#                     pass
#             else:
#                 # Assume it's inputs for `act`
#                 inputs = message
#                 self.handle_act(inputs)
#
#     def handle_act(self, inputs: Dict[str, Any]):
#         try:
#             # Run the agent's action method
#             result = self.agent.act(**inputs)
#             # Send the output back
#             self.connection.send(Envelope(event=AgentOutput(output=result)))
#             # Notify that the agent is done
#             self.connection.send(Envelope(event=AgentDone()))
#         except Exception as e:
#             error_message = ''.join(traceback.format_exception_only(type(e), e))
#             self.connection.send(Envelope(event=AgentDone(error=error_message)))
#

# agent_runner/worker.py

# import multiprocessing
# import sys
# import os
# import signal
# import traceback
# import importlib
# from typing import Any, Callable, Dict, Optional, Union
# from .connection import LockedConnection
# from .eventtypes import (
#     Envelope,
#     AgentInput,
#     AgentOutput,
#     AgentLog,
#     AgentRequestInput,
#     AgentMetric,
#     UserInput,
#     Cancel,
#     Shutdown,
#     Done
# )
# from ..base_agent import BaseAgent
# from .helpers import StreamRedirector
# from .exceptions import AgentExecutionError, AgentSetupError
# import threading
#
# from ..load_agent import load_agent_from_ref, load_full_agent_from_file
#
#
# class Worker:
#     """
#     Manages the worker process that runs the agent's code.
#     """
#
#     def __init__(self, agent_path: str):
#         self.parent_conn, self.child_conn = multiprocessing.Pipe()
#         self.events = LockedConnection(self.parent_conn)
#         self.child = _ChildWorker(agent_path, self.child_conn)
#         self.subscribers = []
#         self.state = 'NEW'
#         self.thread = threading.Thread(target=self._consume_events)
#         self.thread.daemon = True
#
#     def start(self):
#         if self.state != 'NEW':
#             raise RuntimeError("Worker already started or terminated.")
#         self.child.start()
#         self.state = 'STARTED'
#         self.thread.start()
#
#     def send_event(self, event: Envelope):
#         self.events.send(event)
#
#     def subscribe(self, callback: Callable[[Envelope], None]):
#         self.subscribers.append(callback)
#
#     def _consume_events(self):
#         while True:
#             try:
#                 envelope = self.events.recv()
#                 for callback in self.subscribers:
#                     callback(envelope)
#                 if isinstance(envelope.event, Done):
#                     break
#             except EOFError:
#                 break
#
#     def shutdown(self):
#         if self.state != 'STARTED':
#             return
#         self.send_event(Envelope(event=Shutdown()))
#         self.child.join()
#         self.state = 'TERMINATED'
#
# class _ChildWorker(multiprocessing.Process):
#     """
#     Child worker process that runs the agent code.
#     """
#
#     def __init__(self, connection):
#         super().__init__()
#         agent_ref = os.getenv("AGENT_REF", "my_agent:MyAgent")
#         self.agent_ref = agent_ref
#         self.events = LockedConnection(connection)
#         self.agent: Optional[BaseAgent] = None
#         self.current_tag: Optional[str] = None
#
#     def run(self):
#         signal.signal(signal.SIGINT, signal.SIG_IGN)  # Ignore SIGINT in child
#
#         if not self.agent:
#             raise Exception("Couldn't load agent")
#
#
#         with StreamRedirector(self._stream_write_hook):
#             try:
#                 self._load_agent()
#                 self._setup_agent()
#                 self._event_loop()
#             except Exception as e:
#                 error_detail = ''.join(traceback.format_exception_only(type(e), e))
#                 self.events.send(Envelope(event=Done(error=True, error_detail=error_detail)))
#             finally:
#                 self.events.close()
#
#     def _load_agent(self):
#         # 1. Read the agent ref from environment
#         ref = os.getenv("AGENT_REF", "my_agent:MyAgent")
#         print(f"loading agent from {ref}")
#         module_path, class_name = ref.split(":", 1)
#         module_name = os.path.basename(module_path).split(".py", 1)[0]
#         module = load_full_agent_from_file(module_path, module_name)
#         agent_class = getattr(module, class_name)
#         if not issubclass(agent_class, BaseAgent):
#             raise AgentSetupError("Agent class must inherit from BaseAgent")
#         self.agent = agent_class()
#         # Attach methods for communication
#         self.agent.send_output = self._send_output
#         self.agent.send_log = self._send_log
#         self.agent.request_user_input = self._request_user_input
#         self.agent.set_metric = self._set_metric
#
#     def _setup_agent(self):
#         if hasattr(self.agent, 'setup'):
#             self.agent.setup()
#
#     def _event_loop(self):
#         while True:
#             envelope = self.events.recv()
#             event = envelope.event
#             self.current_tag = envelope.tag
#             if isinstance(event, AgentInput):
#                 self._handle_agent_input(event.payload)
#             elif isinstance(event, UserInput):
#                 self._handle_user_input(event.input_data)
#             elif isinstance(event, Cancel):
#                 # Handle cancellation
#                 self.events.send(Envelope(event=Done(canceled=True), tag=self.current_tag))
#                 break
#             elif isinstance(event, Shutdown):
#                 # Handle graceful shutdown
#                 self.events.send(Envelope(event=Done(), tag=self.current_tag))
#                 break
#             else:
#                 self._send_log(f"Unknown event received: {event}")
#
#     def _handle_agent_input(self, payload: Dict[str, Any]):
#         try:
#             output = self.agent.act(**payload)
#             if output is not None:
#                 self._send_output(output)
#             self.events.send(Envelope(event=Done(), tag=self.current_tag))
#         except Exception as e:
#             error_detail = traceback.format_exc()
#             self.events.send(Envelope(event=Done(error=True, error_detail=error_detail), tag=self.current_tag))
#
#     def _handle_user_input(self, input_data):
#         try:
#             if hasattr(self.agent, 'on_user_input'):
#                 self.agent.on_user_input(input_data)
#             else:
#                 self._send_log("Agent does not implement on_user_input method.")
#         except Exception as e:
#             error_detail = traceback.format_exc()
#             self.events.send(Envelope(event=Done(error=True, error_detail=error_detail), tag=self.current_tag))
#
#     def _send_output(self, output):
#         self.events.send(Envelope(event=AgentOutput(output=output), tag=self.current_tag))
#
#     def _send_log(self, message):
#         self.events.send(Envelope(event=AgentLog(message=message, source='stdout'), tag=self.current_tag))
#
#     def _request_user_input(self, prompt: Optional[str] = None):
#         self.events.send(Envelope(event=AgentRequestInput(prompt=prompt), tag=self.current_tag))
#
#     def _set_metric(self, name: str, value: float):
#         self.events.send(Envelope(event=AgentMetric(name=name, value=value), tag=self.current_tag))
#
#     def _stream_write_hook(self, source: str, message: str):
#         self._send_log(message)



# agent_runner/worker.py

import multiprocessing
import os
import signal
import threading
import traceback
from typing import Any, Dict, Optional, Union, Callable
from .connection import LockedConnection
from .eventtypes import (
    Envelope,
    AgentInput,
    AgentOutput,
    AgentLog,
    AgentRequestInput,
    AgentRequestSensitiveInput,
    AgentMetric,
    UserInput,
    SensitiveUserInput,
    Cancel,
    Pause,
    Shutdown,
    Done
)
from ..base_agent import BaseAgent
from .helpers import StreamRedirector
from .exceptions import AgentExecutionError, AgentSetupError
import importlib

from ..load_agent import load_full_agent_from_file


class Worker:
    def __init__(self):
        self.parent_conn, self.child_conn = multiprocessing.Pipe()
        self.events = LockedConnection(self.parent_conn)
        self.child = _ChildWorker(self.child_conn)
        self.subscribers = []
        self.state = 'NEW'

    def start(self):
        if self.state != 'NEW':
            raise RuntimeError("Worker already started or terminated.")
        self.child.start()
        self.state = 'STARTED'
        self._start_event_listener()

    def send_event(self, envelope: Envelope):
        self.events.send(envelope)

    def subscribe(self, callback: Callable[[Envelope], None]):
        self.subscribers.append(callback)

    def _start_event_listener(self):
        def listen():
            while True:
                try:
                    envelope = self.events.recv()
                    for callback in self.subscribers:
                        callback(envelope)
                    if isinstance(envelope.event, Done):
                        break
                except EOFError:
                    break
        listener_thread = threading.Thread(target=listen)
        listener_thread.daemon = True
        listener_thread.start()

    def shutdown(self):
        if self.state != 'STARTED':
            return
        self.send_event(Envelope(event=Shutdown()))
        self.child.join()
        self.state = 'TERMINATED'

class _ChildWorker(multiprocessing.Process):
    def __init__(self, connection):
        super().__init__()
        self.events = LockedConnection(connection)
        self.agent: Optional[BaseAgent] = None
        self.current_tag: Optional[str] = None
        self.paused = False
        self.pause_event = threading.Event()

    def run(self):
        signal.signal(signal.SIGINT, signal.SIG_IGN)  # Ignore SIGINT in child
        with StreamRedirector(self._stream_write_hook):
            try:
                self._load_agent()
                self._setup_agent()
                self._event_loop()
            except Exception as e:
                error_detail = traceback.format_exc()
                self.events.send(Envelope(event=Done(error=True, error_detail=error_detail)))
            finally:
                self.events.close()

    def _load_agent(self):
        # 1. Read the agent ref from environment
        ref = os.getenv("AGENT_REF", "my_agent:MyAgent")
        print(f"loading agent from {ref}")
        module_path, class_name = ref.split(":", 1)
        module_name = os.path.basename(module_path).split(".py", 1)[0]
        module = load_full_agent_from_file(module_path, module_name)
        agent_class = getattr(module, class_name)
        if not issubclass(agent_class, BaseAgent):
            raise AgentSetupError("Agent class must inherit from BaseAgent")
        # Attach methods for communication
        self.agent.send_output = self._send_output
        self.agent.send_log = self._send_log
        self.agent.request_user_input = self._request_user_input
        self.agent.request_sensitive_user_input = self._request_sensitive_user_input
        self.agent.set_metric = self._set_metric
        self.agent.pause_event = self.pause_event

    def _setup_agent(self):
        if hasattr(self.agent, 'setup'):
            self.agent.setup()

    def _event_loop(self):
        while True:
            envelope = self.events.recv()
            event = envelope.event
            self.current_tag = envelope.tag
            if isinstance(event, AgentInput):
                self._handle_agent_input(event.payload)
            elif isinstance(event, UserInput):
                self._handle_user_input(event.input_data)
            elif isinstance(event, SensitiveUserInput):
                self._handle_sensitive_user_input(event.input_data)
            elif isinstance(event, Pause):
                self._handle_pause()
            elif isinstance(event, Cancel):
                # Handle cancellation
                self.events.send(Envelope(event=Done(canceled=True), tag=self.current_tag))
                break
            elif isinstance(event, Shutdown):
                # Handle graceful shutdown
                self.events.send(Envelope(event=Done(), tag=self.current_tag))
                break
            else:
                self._send_log(f"Unknown event received: {event}")

    def _handle_agent_input(self, payload: Dict[str, Any]):
        try:
            if self.paused:
                self.pause_event.wait()  # Wait until unpaused
            output = self.agent.act(**payload)
            if output is not None:
                self._send_output(output)
            self.events.send(Envelope(event=Done(), tag=self.current_tag))
        except Exception as e:
            error_detail = traceback.format_exc()
            self.events.send(Envelope(event=Done(error=True, error_detail=error_detail), tag=self.current_tag))

    def _handle_user_input(self, input_data):
        if hasattr(self.agent, 'on_user_input'):
            self.agent.on_user_input(input_data)
        else:
            self._send_log("Agent does not implement on_user_input method.")

    def _handle_sensitive_user_input(self, input_data):
        if hasattr(self.agent, 'on_sensitive_user_input'):
            self.agent.on_sensitive_user_input(input_data)
        else:
            self._send_log("Agent does not implement on_sensitive_user_input method.")

    def _handle_pause(self):
        if hasattr(self.agent, 'pause'):
            self.paused = True
            self.agent.pause()
        else:
            raise NotImplementedError("Pause functionality not implemented by the agent")

    def _send_output(self, output):
        self.events.send(Envelope(event=AgentOutput(output=output), tag=self.current_tag))

    def _send_log(self, message):
        self.events.send(Envelope(event=AgentLog(message=message, source='stdout'), tag=self.current_tag))

    def _request_user_input(self, prompt: Optional[str] = None):
        self.events.send(Envelope(event=AgentRequestInput(prompt=prompt), tag=self.current_tag))

    def _request_sensitive_user_input(self, prompt: Optional[str] = None):
        self.events.send(Envelope(event=AgentRequestSensitiveInput(prompt=prompt), tag=self.current_tag))

    def _set_metric(self, name: str, value: float):
        self.events.send(Envelope(event=AgentMetric(name=name, value=value), tag=self.current_tag))

    def _stream_write_hook(self, source: str, message: str):
        self._send_log(message)

