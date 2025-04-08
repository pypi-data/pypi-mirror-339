"""
Copyright (C) 2024 Interactive Brokers LLC. All rights reserved. This code is subject to the terms
 and conditions of the IB API Non-Commercial License or the IB API Commercial License, as applicable.
"""

from dtscore.ibapi.const import UNSET_INTEGER
from dtscore.ibapi.object_implem import Object
from dtscore.ibapi.utils import intMaxString

class OrderCancel(Object):
    def __init__(self):
        self.manualOrderCancelTime = ""
        self.extOperator = ""
        self.externalUserId = ""
        self.manualOrderIndicator = UNSET_INTEGER

    def __str__(self):
        s = "manualOrderCancelTime: %s, extOperator: %s, externalUserId: %s, manualOrderIndicator: %s" % (
            self.manualOrderCancelTime,
            self.extOperator,
            self.externalUserId,
            intMaxString(self.manualOrderIndicator),
        )

        return s
