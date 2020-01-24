#!/usr/bin/env python3
from querydispatcher import QueryDispatcher
from datetime import datetime

qd = QueryDispatcher()

#qd.get_history('GGAL.BA', '2010-01-01', datetime.today().strftime('%Y-%m-%d'))



start_date='2010-01-01'
end_date= datetime.today().strftime('%Y-%m-%d')


qd.get_history('GGAL', start_date ,end_date)

with open('tickers_panel.txt') as tf:
    for ticker in ( x.strip() for x in tf ):
        try:
            qd.get_history('%s.BA' % ticker , start_date ,end_date)
            print("Processed %s" % ticker)
        except Exception as e:
                print("Error on ticker %s" % ticker)
                print(e)
    