"""
    Test IB package functionality
"""
import dataclasses as dc
from dtscore import logging as _log
from dtscore import tws

def main():
    with tws.TwsAdapter() as twsa:
        test_get_positions(twsa)
        test_get_openorders(twsa)
        order = test_submit_order(twsa)
        test_get_openorders(twsa)
        test_cancel_order(twsa,order)
        test_get_openorders(twsa)

        order1 = tws.make_marketorder(action=tws.OrderAction.Buy, qty=100, symbol="AAPL")

        order2 = tws.make_limitorder(action=tws.OrderAction.Buy, qty=100, symbol="IBM", limitprice=231.00)
        order3 = tws.make_stoporder(action=tws.OrderAction.Sell, qty=100, symbol="IBM", stopprice=175.00)

        ocaorders = tws.make_oca( [order2, order3] )
        ocaorders.append(order1)

        updatedorders = twsa.place_orders(ocaorders)

        openorders = twsa.get_openorders()
        for oo,os in openorders: log.info(f"{oo}, {os}")

        positions = twsa.get_positions()
        for p in positions: log.info(p)

        twsa.cancel_orders(updatedorders)

# --------------------------------------------------------------------------------
def test_get_positions(twsa:tws.TwsAdapter) -> list[tws.Position]:
    positions = twsa.get_positions()
    if len(positions) > 0:
        for k,v in positions.items():
            log.info(f"symbol={k}, acct:{v.account}, contract:{v.contract}, position:{v.position}, avgcost:{v.avgcost}")
    else:
        log.info("No positions")
    return positions

# --------------------------------------------------------------------------------
def test_get_openorders(twsa:tws.TwsAdapter) -> list[tws.CoreOrder]:
    openorders = twsa.get_openorders()
    if len(openorders) > 0:
        for oo,os in openorders: log.info(f"{oo}, {os}")
    else:
        log.info("No open orders")
    return openorders

# --------------------------------------------------------------------------------
def test_submit_order(twsa:tws.TwsAdapter) -> tws.CoreOrder:
    order = tws.make_limitorder(action=tws.OrderAction.Buy, qty=100, symbol="AAPL", limitprice=123.33)
    order = twsa.place_order(order)
    return order

# --------------------------------------------------------------------------------
def test_cancel_order(twsa:tws.TwsAdapter, order:tws.CoreOrder) -> bool:
    return twsa.cancel_order(order)

        
# --------------------------------------------------------------------------------
#   Entry point
LOG_FILENAME = 'dtscore_test.log'
LOG_LEVEL = _log.DEBUG
if __name__ == '__main__':
    _log.initialize_log(LOG_FILENAME)
    log = _log.get_log(__name__, LOG_LEVEL)
    main()
else:
    log = _log.get_log(__name__, LOG_LEVEL)
