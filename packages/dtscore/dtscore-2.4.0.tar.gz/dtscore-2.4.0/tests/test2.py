
from dtscore import tiingo as ti
from dtscore import domain
import datetime as dt

# closeprice = ti.latesteodclose('aapl')
# print(closeprice)

# quote = ti.latesteodquote('aapl')
# print(quote)

# quote = ti.quotefordate('aapl', dt.datetime(2024,1,4).date())
# print(quote)

#   test for known existing symbol
# start = dt.datetime(2024,1,4).date();
# end = dt.datetime(2024,1,10).date()
# quotes = ti.quotesfordaterange('aapl', start, end)
# for q in quotes: print(q)

#   test for unknown symbol
tickers = ['vix','aapl']
start = dt.datetime(2024,1,4).date()
end = dt.datetime(2024,1,10).date()
for ticker in tickers:
    try:
        quotes = ti.quotesfordaterange(ticker, start, end)
        for q in quotes: print(q)
    except Exception as e:
        print(f"Error: {str(e)}")
        