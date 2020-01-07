#!/usr/bin/env python3
from sqlalchemy import Column, Integer, Unicode, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Ticker(Base):
    __tablename__ = 'tickers'
    id            =   Column(Unicode, primary_key=True)
    description   =   Column(Unicode)

class Quote(Base):
    __tablename__ = 'quotes'
    ticker_id     =   Column(Unicode,  ForeignKey('tickers.id'), primary_key=True)
    date          =   Column(Date, primary_key=True)
    open          =   Column(Float)
    high          =   Column(Float)
    low           =   Column(Float)
    close         =   Column(Float)
    adj_close     =   Column(Float)
    volume        =   Column(Integer)
    ticker        =   relationship(Ticker)
