import multiprocessing
from multiprocessing.connection import Connection
from typing import Any

from threading import Lock


def create_pipe():
    """Creates a duplex (bidirectional) pipe for communication."""
    parent_conn, child_conn = multiprocessing.Pipe(duplex=True)
    return parent_conn, child_conn

class ConnectionWrapper:
    """Wraps a multiprocessing Connection object to provide send and receive methods."""
    def __init__(self, connection: Connection):
        self.connection = connection

    def send(self, obj: Any):
        self.connection.send(obj)

    def recv(self) -> Any:
        return self.connection.recv()

    def close(self):
        self.connection.close()


class LockedConnection:
    """
    Wraps a multiprocessing Connection with a lock to ensure thread-safe operations.
    """
    def __init__(self, connection: Connection):
        self.connection = connection
        self.lock = Lock()

    def send(self, obj: Any):
        with self.lock:
            self.connection.send(obj)

    def recv(self) -> Any:
        return self.connection.recv()

    def close(self):
        self.connection.close()