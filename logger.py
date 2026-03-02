"""
Shared log queue and stop flag for crawl control and live GUI updates.
"""

from queue import Queue
import threading

log_queue = Queue()
stop_event = threading.Event()


def log(msg):
    """Push log message to queue (used by GUI live stream)."""
    print(msg)
    log_queue.put(msg)

