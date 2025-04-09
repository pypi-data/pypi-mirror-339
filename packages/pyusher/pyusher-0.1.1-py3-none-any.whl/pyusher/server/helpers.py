import sys


# class StreamRedirector:
#     """
#     Context manager to redirect stdout and stderr to a callback function.
#     """
#
#     def __init__(self, callback, tee: bool = False):
#         self.callback = callback
#         self.tee = tee
#         self.original_stdout = sys.stdout
#         self.original_stderr = sys.stderr
#
#     def write(self, message):
#         self.callback(message)
#         if self.tee:
#             self.original_stdout.write(message)
#
#     def flush(self):
#         pass
#
#     def __enter__(self):
#         sys.stdout = self
#         sys.stderr = self
#         return self
#
#     def __exit__(self, exc_type, exc_value, traceback):
#         sys.stdout = self.original_stdout
#         sys.stderr = self.original_stderr
#
#
# # agent_runner/helpers.py

import sys
import threading
from contextlib import contextmanager

class StreamRedirector:
    """
    Context manager to redirect stdout and stderr to a callback function.
    """

    def __init__(self, callback):
        self.callback = callback
        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr
        self.local = threading.local()

    def write(self, message):
        self.callback('stdout', message)

    def flush(self):
        pass

    def __enter__(self):
        self.local.stdout = sys.stdout
        self.local.stderr = sys.stderr
        sys.stdout = self
        sys.stderr = self
        return self

    def __exit__(self, *args):
        sys.stdout = self.local.stdout
        sys.stderr = self.local.stderr
