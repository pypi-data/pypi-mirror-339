# class AgentRunnerError(Exception):
#     """Base exception for agent runner errors."""
#     pass
#
# class AgentBusyError(AgentRunnerError):
#     """Raised when the agent is already processing a request."""
#     pass
#
# class UnknownAgentError(AgentRunnerError):
#     """Raised when an agent ID is not recognized."""
#     pass
#
# class AgentSetupError(AgentRunnerError):
#     """Raised when there is an error in setting up the agent."""
#     pass
#
# class AgentExecutionError(AgentRunnerError):
#     """Raised when the agent encounters an error during execution."""
#     pass
#
# class AgentCancelledError(AgentRunnerError):
#     """Raised when the agent execution is cancelled."""
#     pass

# agent_runner/exceptions.py

class AgentRunnerError(Exception):
    """Base exception for agent runner errors."""
    pass

class AgentBusyError(AgentRunnerError):
    """Raised when the agent is not in a state to receive input."""
    pass

class UnknownAgentError(AgentRunnerError):
    """Raised when an agent or task ID is not recognized."""
    pass

class AgentSetupError(AgentRunnerError):
    """Raised when there is an error setting up the agent."""
    pass

class AgentExecutionError(AgentRunnerError):
    """Raised when the agent encounters an error during execution."""
    pass
