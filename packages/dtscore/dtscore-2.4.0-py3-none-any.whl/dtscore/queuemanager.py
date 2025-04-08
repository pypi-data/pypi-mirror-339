"""
    Queue manager
"""
import queue as q
from typing import Any

from dtscore import logging as _log

_queue = q.Queue()
    
# --------------------------------------------------------------------------------
def read_queue() -> list[Any]:
    """ Read all items on the queue until None is received. """
    items = []
    while True:
        item = _queue.get()
        if item is None: break
        items.append(item)
    return items

# --------------------------------------------------------------------------------
def put(item:Any) -> None:
    """ Put an item on the queue """
    _queue.put(item)

# --------------------------------------------------------------------------------
#   Entry point
LOG_LEVEL = _log.DEBUG
if __name__ == '__main__':
    print("Error - this package cannot be run as a script")
else:
    log = _log.get_log(__name__, LOG_LEVEL)
