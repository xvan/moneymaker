#!/usr/bin/env python3
from financedb import Base, Ticker, Quote
from yahoofinance import yahooFinance
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

import csv


class QueryDispatcher(object):
    def __init__(self):
        self.__yahooFinance = None
        self._session = self._initDB()

    @property
    def _yahooFinance(self):
        if self.__yahooFinance is None :
            self.__yahooFinance = yahooFinance()
        return self.__yahooFinance

    def _initDB(self):
        self.engine = create_engine('sqlite:///test.db')
        Base.metadata.create_all(self.engine)  # issues DDL to create tables
        return sessionmaker(bind=self.engine)()
    

    def get_or_create_ticker(self, ticker):
        _ticker = self._session.query(Ticker).get(ticker)
        if _ticker is None:
           #TODO: Deberia descargar la descripcion del ticker
           _ticker = Ticker(id=ticker)
           self._session.add(_ticker)
        return _ticker
    
    def get_history(self, ticker, start_date, end_date):
        _ticker = self.get_or_create_ticker(ticker)

        fs = self._yahooFinance.get_history(ticker,start_date,end_date)
        for row in csv.DictReader(fs):
            #print(row)
            _quote = Quote( ticker_id = _ticker.id,
                            date  = datetime.strptime( row['Date'], "%Y-%m-%d"),
                            open  = self._parse_check( row['Open']),
                            high  = self._parse_check( row['High']),
                            low   = self._parse_check(row['Low']),
                            close = self._parse_check(row['Close']),
                            adj_close = self._parse_check(row['Adj Close']),
                            volume = self._parse_check(row['Volume'] )
                            )

            self._session.add(_quote)

        self._session.commit()

    def _parse_check(self, _str):
        return _str if _str != 'null' else None
