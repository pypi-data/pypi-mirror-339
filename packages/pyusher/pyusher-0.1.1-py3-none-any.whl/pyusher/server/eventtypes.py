# from typing import Any, Dict, Optional, Union
# from dataclasses import dataclass
#
# # Events sent from main process to worker
# @dataclass
# class AgentInput:
#     payload: Dict[str, Any]
#
# @dataclass
# class UserInput:
#     input_data: Any
#
# @dataclass
# class Cancel:
#     pass
#
# @dataclass
# class Shutdown:
#     pass
#
# # Events sent from worker to main process
# @dataclass
# class AgentOutput:
#     output: Any
#
# @dataclass
# class AgentLog:
#     message: str
#     source: str  # 'stdout' or 'stderr'
#
# @dataclass
# class AgentRequestInput:
#     prompt: Optional[str] = None
#
# @dataclass
# class AgentMetric:
#     name: str
#     value: float
#
# @dataclass
# class Done:
#     error: bool = False
#     error_detail: str = ""
#     canceled: bool = False
#
# # Envelope to wrap events with an optional tag
# @dataclass
# class Envelope:
#     event: Union[
#         AgentInput,
#         UserInput,
#         Cancel,
#         Shutdown,
#         AgentOutput,
#         AgentLog,
#         AgentRequestInput,
#         AgentMetric,
#         Done
#     ]
#     tag: Optional[str] = None  # For correlating events in concurrent scenarios


# agent_runner/events.py

from typing import Any, Dict, Optional, Union
from dataclasses import dataclass

# Events from main process to worker
@dataclass
class AgentInput:
    payload: Dict[str, Any]

@dataclass
class UserInput:
    input_data: Any

@dataclass
class SensitiveUserInput:
    input_data: Any

@dataclass
class Cancel:
    pass

@dataclass
class Pause:
    pass

@dataclass
class Shutdown:
    pass

# Events from worker to main process
@dataclass
class AgentOutput:
    output: Any

@dataclass
class AgentLog:
    message: str
    source: str  # 'stdout' or 'stderr'

@dataclass
class AgentRequestInput:
    prompt: Optional[str] = None

@dataclass
class AgentRequestSensitiveInput:
    prompt: Optional[str] = None

@dataclass
class AgentMetric:
    name: str
    value: float

@dataclass
class Done:
    error: bool = False
    error_detail: str = ""
    canceled: bool = False

# Envelope to wrap events with an optional tag
@dataclass
class Envelope:
    event: Union[
        AgentInput,
        UserInput,
        SensitiveUserInput,
        Cancel,
        Pause,
        Shutdown,
        AgentOutput,
        AgentLog,
        AgentRequestInput,
        AgentRequestSensitiveInput,
        AgentMetric,
        Done
    ]
    tag: Optional[str] = None  # For correlating events in concurrent scenarios
