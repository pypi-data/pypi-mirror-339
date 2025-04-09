from abc import ABC, abstractmethod
from typing import Any, Optional

class BaseAgent(ABC):
    def setup(self):
        """
        Optional setup method for the agent.
        """
        pass

    @abstractmethod
    def act(self, **inputs):
        """
        Main method where the agent performs its actions.
        """
        pass

    def on_user_input(self, user_input):
        """
        Handle user input when received.
        """
        pass

    def on_sensitive_user_input(self, sensitive_input):
        """
        Handle sensitive user input when received.
        """
        pass

    def pause(self):
        """
        Optional method to pause the agent. Agent developers can override this.
        """
        raise NotImplementedError("Pause functionality not implemented.")

    # Methods to be implemented by the worker for communication
    def send_output(self, output: Any):
        raise NotImplementedError("send_output not implemented")

    def send_log(self, message: str):
        raise NotImplementedError("send_log not implemented")

    def request_user_input(self, prompt: Optional[str] = None):
        raise NotImplementedError("request_user_input not implemented")

    def request_sensitive_user_input(self, prompt: Optional[str] = None):
        raise NotImplementedError("request_sensitive_user_input not implemented")

    def set_metric(self, name: str, value: float):
        raise NotImplementedError("set_metric not implemented")

    # Additional attribute for pause handling
    pause_event: Optional[Any] = None  # Will be set by the worker
