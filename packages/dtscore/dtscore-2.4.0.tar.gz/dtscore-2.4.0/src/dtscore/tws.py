"""
    IBroker TWS Adapter
"""

import dataclasses as dc
import random
import threading
import time
from dataclasses import dataclass
from decimal import Decimal
from typing import Iterable, NamedTuple, Optional, Self

from dtscore import logging as _log
from dtscore import queuemanager as qmgr
from dtscore.ibapi import client as ibclnt
from dtscore.ibapi import const as ibconst
from dtscore.ibapi import contract as ibcon
from dtscore.ibapi import order as ibord
from dtscore.ibapi import order_cancel as iboc
from dtscore.ibapi import wrapper as ibwrap

#   connection parameters
C_HOST = '127.0.0.1'
C_PORT = 7497
C_CLIENT = 1

Position = NamedTuple('Position', [('account',str), ('contract',ibcon.Contract), ('position',Decimal), ('avgcost',float)])
OpenOrder = NamedTuple('OpenOrder', [ ('orderId',int), ('contract',ibcon.Contract), ('order',ibord.Order), ('orderState',ibwrap.OrderState)])

# -------------------------------------------------------------------------------------------------
class OrderType:
    """ Core order ordertype constants. """
    Limit = 'LMT'
    Stop = 'STP'
    Market = 'MKT'

# -------------------------------------------------------------------------------------------------
class OrderAction:
    """ Core order action constants. """
    Buy = 'B'
    Sell = 'S'

# -------------------------------------------------------------------------------------------------
@dataclass
class CoreOrder:
    symbol:str
    action:str
    qty:int
    ordertype:str
    limitprice:Optional[float] = None
    stopprice:Optional[float] = None
    orderid:Optional[ibclnt.OrderId] = None
    ocagroup:Optional[str] = None
    ocatype:Optional[int] = None

    def __str__(self):
        ordertext = f'{self.action} {self.qty} {self.symbol} @ '
        match self.ordertype:
            case OrderType.Market: suffix = OrderType.Market
            case OrderType.Limit: suffix = f'{self.limitprice} {OrderType.Limit}'
            case OrderType.Stop: suffix = f'{self.stopprice} {OrderType.Stop}'
        ordertext += suffix
        return ordertext

# -------------------------------------------------------------------------------------------------
@dataclass
class OrderState:
    status:Optional[str]
    commission:Optional[float]
    warningtext:Optional[str]
    completedtime:Optional[str]
    completedstatus:Optional[str]

# -------------------------------------------------------------------------------------------------
class CoreContract:
    def __init__(self, symbol:str, orders:list[CoreOrder] = []):
        self.symbol = symbol
        self.orders = orders

    def append_order(self, order:CoreOrder):
        self.orders.append(order)

# -------------------------------------------------------------------------------------------------
class IBapi(ibwrap.EWrapper, ibclnt.EClient):
    """ EWrapper and EClient subclassing and handling """
    def __init__(self):
        ibclnt.EClient.__init__(self, self)
        self.nextValidOrderId: Optional[int] = None

    def error(self:ibwrap.EWrapper, reqId:ibclnt.TickerId, errorCode:int, errorString:str, advancedOrderRejectJson=""):
        # -1, 502 can't connect
        # -1, 2104 market data farm connect OK
        # -1, 2106 HMDS data farm connect OK
        # -1, 2108 Market data farm connection is inactive but should be available upon demand.cafarm
        # -1, 2158 Sec-def data farm connect OK
        error_whitelist = [2104, 2106, 2108, 2158]
        error_blacklist = [502]
        if errorCode in error_blacklist:
            match errorCode:
                case 502:
                    raise Exception('Unable to connect to Tws. Is Tws started?')
                case _:
                    raise Exception(f'Fatal error: received tws error: {errorCode}, {errorString}')
        
        if errorCode not in error_whitelist:
            log.error("Tws ERROR %s %s %s", reqId, errorCode, errorString)

    def nextValidId(self, orderId: int):
        """ this function overrides the corresponding one in EWrapper"""
        super().nextValidId(orderId)
        self.nextValidOrderId = orderId
        log.info(f'The next valid order id is: {self.nextValidOrderId}')

    def get_nextValidOrderId(self) -> int:
        if self.nextValidOrderId is None: raise Exception("Invalid application state. Retrieving a None order id.")
        orderId = self.nextValidOrderId
        self.nextValidOrderId += 1
        return orderId
    
    def orderStatus(self, orderId:ibclnt.OrderId, status:str, filled:Decimal, remaining:Decimal, avgFillPrice:float, permId:int,
            parentId:int, lastFillPrice:float, clientId:int, whyHeld:str, mktCapPrice:float,):
        #log.debug(f'orderStatus - orderid:{orderId}, status:{status}, filled:{filled}, remaining:{remaining}, lastFillPrice:{lastFillPrice}')
        pass
    
    def openOrder(self, orderId:ibclnt.OrderId, contract:ibcon.Contract, order:ibord.Order, orderState:OrderState):
        #log.debug(f'openOrder id: {orderId}, {contract.symbol}, {contract.secType} @ {contract.exchange}:{order.action} {order.orderType} {order.totalQuantity} {orderState.status}')
        qmgr.put(OpenOrder(orderId, contract, order, orderState))

    def openOrderEnd(self):
        qmgr.put(None)

    def execDetails(self, reqId, contract, execution):
        log.debug(f'Order Executed: {reqId}, {contract.symbol}, {contract.secType}, {contract.currency}, {execution.execId}, {execution.orderId}, {execution.shares}, {execution.lastLiquidity}')

    def position(self, account:str, contract:ibcon.Contract, position:Decimal, avgCost:float):
        #super().position(account, contract, position, avgCost)
        #log.debug(f"Position[Account:{account}, Symbol:{contract.symbol}, SecType:{contract.secType}, Currency:{contract.currency},Position:{position}, Avg cost:{avgCost}]")
        qmgr.put( Position(account,contract,position,avgCost) )

    def positionEnd(self):
        #super().positionEnd()
        #print("position end received")
        qmgr.put(None)
        self.cancelPositions()

# --------------------------------------------------------------------------------
class TwsAdapter:
    """ Client TWS adapter. """
    _adapterinstance:Self = None

    # --------------------------------------------------------------------------------
    def __init__(self):
        """ Ensure only singleton. """
        if TwsAdapter._adapterinstance is None:
            TwsAdapter._adapterinstance = self
        else:
            raise Exception("Cannot create another TwsAdapter instance when one already exists.") 
    
    # --------------------------------------------------------------------------------
    def __enter__(self):
        """ Connect to IB and start the TWS message loop """
        try:
            #   run the read socket loop
            def run_loop(app): app.run()
            ibapi = IBapi()
            ibapi.nextValidOrderId = None
            ibapi.connect(C_HOST, C_PORT, C_CLIENT)
            #   Start the socket in a thread
            api_thread = threading.Thread(target=lambda:run_loop(ibapi), daemon=True)
            api_thread.start()

            #   Check if the API is connected via orderid
            while True:
                if isinstance(ibapi.nextValidOrderId, int):
                    log.info('connected')
                    break
                else:
                    log.info('waiting for connection')
                    time.sleep(2)
            self._ibapi = ibapi
        except Exception as ex:
            log.fatal(f'Fatal error while initializing TWS {ex}.', exc_info=True)
            raise
        return self

    # --------------------------------------------------------------------------------
    def __exit__(self, exc_type, exc_value, exc_traceback):
        """ Close the tws socket """
        log.info('closing tws')
        self._ibapi.disconnect()
        TwsAdapter._adapterinstance = None
        log.info('tws closed')

    # --------------------------------------------------------------------------------
    def cancel_order(self, order:CoreOrder) -> None:
        """ Cancel an order. """
        log.info(f'cancelling order: {order}')
        self._ibapi.cancelOrder(order.orderid, orderCancel=iboc.OrderCancel())

    # --------------------------------------------------------------------------------
    def cancel_orders(self, orders:Iterable[CoreOrder]):
        """ Cancel a list of orders. """
        for o in orders: self.cancel_order(o)

    # --------------------------------------------------------------------------------
    def place_order(self, coreorder:CoreOrder) -> CoreOrder:
        """ Place an order with IBkrs. """
        ibcontract, iborder = _create_ibcontractorder(coreorder=coreorder)
        orderid = self._submit_singleorder(contract=ibcontract, order=iborder)
        return dc.replace(coreorder, orderid=orderid)
    
    # --------------------------------------------------------------------------------
    def place_orders(self, orders:Iterable[CoreOrder]) -> list[CoreOrder]:
        return [self.place_order(o) for o in orders]

    # --------------------------------------------------------------------------------
    def get_positions(self) -> dict[str,Position]:
        """ Return list of tws positions """
        self._ibapi.reqPositions()
        positionslist:list[Position] = qmgr.read_queue()
        positions = { k:v for (k,v) in map(lambda posn: (posn.contract.localSymbol,posn), positionslist) }
        return positions

    # --------------------------------------------------------------------------------
    def get_openorders(self) -> list[OpenOrder]:
        """ Return list of open orders """
        self._ibapi.reqOpenOrders()
        twsopenorders:list[OpenOrder] = qmgr.read_queue()
        order_state = [ _maporderstate_twstocore(to) for to in twsopenorders ]
        return order_state

    # --------------------------------------------------------------------------------
    def get_executions(self):
        raise NotImplementedError("get_executions not implemented.")

    # --------------------------------------------------------------------------------
    def _submit_singleorder(self, contract:ibcon.Contract, order:ibord.Order) -> ibclnt.OrderId:
        orderid = self._ibapi.get_nextValidOrderId()
        self._ibapi.placeOrder(orderid, contract, order)
        return orderid


###################################################################################

# --------------------------------------------------------------------------------
def make_marketorder(action:OrderAction, qty:int, symbol:str) -> CoreOrder:
    """ order builder - create and return a core order at market order """
    return CoreOrder(action=action, qty=qty, symbol=symbol, ordertype=OrderType.Market)

# --------------------------------------------------------------------------------
def make_limitorder(action:OrderAction, qty:int, symbol:str, limitprice:float) -> CoreOrder:
    """ Return a limit CoreOrder. """
    return CoreOrder(action=action, qty=qty, symbol=symbol, limitprice=limitprice, ordertype=OrderType.Limit)

# --------------------------------------------------------------------------------
def make_stoporder(action:OrderAction, qty:float, symbol:str, stopprice:float) -> CoreOrder:
    """ Return a stop CoreOrder. """
    return CoreOrder(action=action, qty=qty, symbol=symbol, stopprice=stopprice, ordertype=OrderType.Stop)

# --------------------------------------------------------------------------------
def make_oca(orders:Iterable[CoreOrder]) -> list[CoreOrder]:
    """ Mark the orders as OCA with a group id """
    def make_group(order:CoreOrder):
        order.ocagroup = grpid
        order.ocatype=1
        return order

    if len(orders) < 2: return orders
    grpid = "oca-" + str(random.randint(1000,9999))
    grouped_orders = [make_group(o) for o in orders]
    return grouped_orders

# --------------------------------------------------------------------------------
def to_orderaction(action:str) -> str:
    match str.upper(action):
        case 'B': return OrderAction.Buy
        case 'BUY': return OrderAction.Buy
        case 'S': return OrderAction.Sell
        case 'SELL': return OrderAction.Sell
        case _: raise Exception(f"Unknown order action string: {action}")

# --------------------------------------------------------------------------------
def to_ordertype(ordertype:str) -> str:
    match str.upper(ordertype):
        case 'LMT': return OrderType.Limit
        case 'STP': return OrderType.Stop
        case 'MKT': return OrderType.Market
        case _: raise Exception(f"Unknown order type string: {ordertype}")


#######################################################################################
# private api

# --------------------------------------------------------------------------------
def _create_iborder(coreorder:CoreOrder) -> ibord.Order:
    """ Create an IB order based on the provided EO order. """
    order = ibord.Order()
    order.action = _mapaction_coretotws(coreorder.action)
    order.totalQuantity = coreorder.qty
    order.orderType = coreorder.ordertype
    match coreorder.ordertype:
        case OrderType.Limit: order.lmtPrice = _verify_price(coreorder.limitprice)
        case OrderType.Stop: order.auxPrice = _verify_price(coreorder.stopprice)
    if coreorder.ocagroup is not None:
        order.ocaGroup = coreorder.ocagroup
        order.ocaType = coreorder.ocatype
    return order

# --------------------------------------------------------------------------------
def _create_ibcontract(ticker:str) -> ibcon.Contract:
    """ Create an IB contract based on the provided symbol """
    contract = ibcon.Contract()
    contract.symbol = ticker
    contract.secType = 'STK'
    contract.exchange = 'SMART'
    contract.currency = 'USD'
    return contract

# --------------------------------------------------------------------------------
def _create_ibcontractorder(coreorder:CoreOrder):
    """ Create an IB/TWS contract and order and return as contract, order tuple. """
    return _create_ibcontract(coreorder.symbol), _create_iborder(coreorder)

# --------------------------------------------------------------------------------
def _derive_ordertype(order:ibord.Order) -> OrderType:
    is_set = lambda v: True if v > 0.0 and v < ibconst.UNSET_DOUBLE else False
    match is_set(order.lmtPrice), is_set(order.auxPrice):
        #   order of cases is important, test for UNSET_DOUBLEs must be first
        case False, False: return OrderType.Market
        case True, False: return OrderType.Limit
        case False, True: return OrderType.Stop
        case True, True: raise Exception("StopLimit orders not currently supported.")
        case _: raise Exception(f"Unknown ordertype conditions. lmtPrice:{l}, auxPrice:{a}") 
    
# --------------------------------------------------------------------------------
def _maporderstate_twstocore(openorder:OpenOrder) -> tuple[CoreOrder,OrderState]:
    """ Create a core order from a tws order. """
    unset_tonone = lambda v: None if v == ibconst.UNSET_DOUBLE else v
    empty_tonone = lambda v: None if len(v) == 0 else v
    iborder = openorder.order
    ibstate = openorder.orderState
    ibcontract = openorder.contract
    coreorder = CoreOrder(
        orderid=iborder.orderId,
        symbol=ibcontract.symbol,
        qty=iborder.totalQuantity,
        action=_mapaction_twstocore(iborder.action),
        ordertype=_derive_ordertype(iborder),
        limitprice=iborder.lmtPrice,
        stopprice=iborder.auxPrice,
        ocagroup=iborder.ocaGroup,
        ocatype=iborder.ocaType
    )
    corestate = OrderState(
        status=empty_tonone(ibstate.status),
        commission=unset_tonone(ibstate.commission),
        warningtext=empty_tonone(ibstate.warningText),
        completedtime=empty_tonone(ibstate.completedTime),
        completedstatus=empty_tonone(ibstate.completedStatus)
    )
    return coreorder, corestate

def _mapaction_coretotws(coreaction:OrderAction) -> str:
    match coreaction:
        case OrderAction.Sell: return 'SELL'
        case OrderAction.Buy: return 'BUY'
        case _: raise Exception(f"Unknown order action {coreaction}.")

def _mapaction_twstocore(twsaction:str) -> str:
    match twsaction:
        case 'SELL': return OrderAction.Sell
        case 'BUY': return OrderAction.Buy

def _verify_price(price: Optional[float]) -> float:
    if price is None: raise Exception("Invalid application state. Attempt to assign None to a STP or LMT order price.")
    return price

# --------------------------------------------------------------------------------
#   Entry point
LOG_LEVEL = _log.DEBUG
if __name__ == '__main__':
    print("Error - this package cannot be run as a script")
else:
    log = _log.get_log(__name__, LOG_LEVEL)
