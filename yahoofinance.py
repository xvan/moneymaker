#!/usr/bin/env python3
from urllib.request import build_opener, HTTPCookieProcessor, Request, URLError
from urllib.parse import urlencode, quote_plus, urlunparse, urljoin
from http.cookiejar import MozillaCookieJar, CookieJar

import logging
from datetime import datetime
import re, json, gzip, codecs

class _FinanceUri(object):
    def __init__(self, ticker="", query={}):
        self.scheme="https"
        self.netloc="query1.finance.yahoo.com"
        self.base_path="/v7/finance/download/"
        self.ticker=ticker
        self.segment=""
        self.__query=query
        self.fragment=""
        self.username=None
        self.password=None

    @property
    def query(self):
        return urlencode(self.__query)

    def get_uri(self):
        return urlunparse([self.scheme,self.netloc,urljoin(self.base_path,self.ticker) ,self.segment,self.query,self.fragment])
    

class _QueryParams(object):
    def __init__(self, period1, period2, crumb, interval="1d"):
        self.period1=period1
        self.period2=period2
        self.interval="1d"
        self.events="history"
        self.crumb=crumb



class yahooFinance(object):

    def __init__(self):
        #build the opener
        cookie_jar = CookieJar()
        self._url_opener = build_opener(HTTPCookieProcessor(cookie_jar))
        self._url_opener.addheaders =[
                ('Host', 'finance.yahoo.com'),
                ('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0'),
                ('Accept', '*/*'),
                ('Accept-Language', 'en-US,en;q=0.5'),
                ('Accept-Encoding', 'gzip, deflate, br'),
                ('Referer', 'https://finance.yahoo.com/'),
                ('X-Requested-With', 'XMLHttpRequest'),
                ('Connection', 'keep-alive'),
                ('TE', 'Trailers'),
                ('Pragma', 'no-cache'),
                ('Cache-Control', 'no-cache')
                ]

        #First Request to create cookies and access the CrumbStore
        uri='https://finance.yahoo.com/quote/ALUA.BA/history?p=ALUA.BA'

        with self._url_opener.open(Request(uri)) as response:
            with gzip.GzipFile(fileobj=response) as deflated:
                html=deflated.read().decode('utf-8')
                self._crumb = json.loads(re.search('"CrumbStore":({"[^}]*})',html).group(1))["crumb"]
                



    def get_history(self, ticker, start_date, end_date):
        """Download YahooFinance History daily history for ticker.
        returns an utf8 stream with the CSV

        Response Columns are:
        Date, Open, High, Low, Close, Adj Close, Volume

        start/end date can be a datetime in YYYY/MM/DD format string
        """

        date_fmt="%Y-%m-%d"
        if not isinstance(start_date, datetime):
            start_date=datetime.strptime(start_date, date_fmt)

        if not isinstance(end_date, datetime):
            end_date=datetime.strptime(end_date, date_fmt)

        period1=int(start_date.timestamp())
        period2=int(end_date.timestamp())
        
        qp=_QueryParams(period1,period2,self._crumb)
        query_uri=_FinanceUri(ticker, vars(qp)).get_uri()

        logging.info("requesting: %s" %  query_uri)  # will not print anything
        
        response = self._url_opener.open(query_uri)
        deflated = gzip.GzipFile(fileobj=response)
        return codecs.getreader('utf-8')(deflated)
