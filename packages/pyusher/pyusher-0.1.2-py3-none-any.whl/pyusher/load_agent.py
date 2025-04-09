
import types
import importlib.util
import sys
from unittest.mock import patch
from typing import Any
import os
import inspect

from .base_agent import BaseAgent


def load_full_agent_from_file(
    module_path: str, module_name: str
) -> types.ModuleType:
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    # Remove any sys.argv while importing agent to avoid conflicts when
    # user code calls argparse.Parser.parse_args in production
    with patch("sys.argv", sys.argv[:1]):
        spec.loader.exec_module(module)
    return module


def get_agent(module: types.ModuleType, class_name: str) -> Any:
    agent = getattr(module, class_name)
    # It could be a class or a function
    if inspect.isclass(agent):
        return agent()
    return agent


def load_agent_from_ref(ref: str) -> BaseAgent:
    print(f"loading agent from {ref}")
    module_path, class_name = ref.split(":", 1)
    module_name = os.path.basename(module_path).split(".py", 1)[0]
    module = load_full_agent_from_file(module_path, module_name)
    agent = get_agent(module, class_name)
    return agent