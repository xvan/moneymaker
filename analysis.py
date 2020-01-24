#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 15:14:44 2020

@author: jzuloaga
"""

import pandas as pd
#import matplotlib.pyplot as plt

import plotly.graph_objs as go
import cufflinks as cf
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

init_notebook_mode(connected=True)
cf.go_offline()
cf.set_config_file(offline=False, world_readable=True)



from querydispatcher import QueryDispatcher
from financedb import Quote


qd = QueryDispatcher()

sql_DF = pd.read_sql_table(Quote.__tablename__, con=qd.engine)
sql_DF.set_index(Quote.date.name, inplace=True)
 
 
GGAL_BA=sql_DF[sql_DF[Quote.ticker_id.name]=='GGAL.BA'][Quote.adj_close.name]
GGAL=sql_DF[sql_DF[Quote.ticker_id.name]=='GGAL'][Quote.adj_close.name]

ADR_RATIO=10.0
GGAL_CCL=(GGAL_BA * ADR_RATIO / GGAL)
#plot(GGAL_CCL.iplot(asFigure=True))


#TODO FIXME:
PANEL_DF=sql_DF[sql_DF[Quote.ticker_id.name].str[-3:] == '.BA']


normalized=PANEL_DF.groupby(Quote.ticker_id.name)[Quote.adj_close.name].apply(lambda x: x/GGAL_CCL)

data=[]
for k,v in normalized.groupby(Quote.ticker_id.name):
   data += v.iplot(asFigure=True).data
 
print(data)
figure=go.Figure(data=data)
iplot(figure)

#plot(normalized.i plot(asFigure=True))
#df.groupby('ticker')['adj_close'].plot(legend=True)

#PANEL_DF['adj_closed_usd']=PANEL_DF[Quote.adj_close.name]/ GGAL_CCL

#normalized= PANEL_DF.groupby(Quote.ticker_id.name)[Quote.adj_close.name] 




