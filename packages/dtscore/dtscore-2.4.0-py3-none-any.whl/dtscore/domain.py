"""
    Domain classes

    These classes are independent of a particular implementation
"""
#   to postpone resolution of annotations. See @classmethod returning Quote below.
from __future__ import annotations

import datetime as dt
from typing import Optional

class Quote:
    def __init__(self,
            date:dt.date, close:float, high:float, low:float, open:float, volume:int,
            adjClose:Optional[float]=None, adjHigh:Optional[float]=None, adjLow:Optional[float]=None, adjOpen:Optional[float]=None, adjVolume:Optional[int]=None,
            divCash:Optional[float]=None, splitFactor:Optional[float]=None
        ):
        self.date = date
        self.close = float(close)
        self.high = float(high)
        self.low = float(low)
        self.open = float(open)
        self.volume = int(volume)
        self.adjClose = float(adjClose) if adjClose is not None else None
        self.adjHigh = float(adjHigh) if adjHigh is not None else None
        self.adjLow = float(adjLow) if adjLow is not None else None
        self.adjOpen = float(adjOpen) if adjOpen is not None else None
        self.adjVolume = int(adjVolume) if adjVolume is not None else None
        self.divCash = float(divCash) if divCash is not None else None
        self.splitFactor = float(splitFactor) if splitFactor is not None else None

    def __str__(self) -> str:
        return f"Quote[date={self.date}, close={self.close}, high={self.high}, low={self.low}, open={self.open}, volume={self.volume}, " + \
            f"adjClose={self.adjClose}, adjHigh={self.adjHigh}, adjLow={self.adjLow}, adjOpen={self.adjOpen}, adjVolume={self.adjVolume}, "  + \
            f"divCash={self.divCash}, splitFactor={self.splitFactor}"

    def to_list(self) -> list[dt.date | Optional[float] | Optional[int]]:
        return [
            self.date, self.open, self.high, self.low, self.close, self.volume,
            self.adjOpen, self.adjHigh, self.adjLow, self.adjClose, self.adjVolume,
            self.divCash, self.splitFactor
        ]