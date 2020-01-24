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
 
 
adj_close_df =sql_DF.groupby(Quote.ticker_id.name)[Quote.adj_close.name]

ADR_RATIO=10.0


GGAL_CCL=(adj_close_df.get_group('GGAL.BA') * ADR_RATIO / adj_close_df.get_group('GGAL'))
plot(GGAL_CCL.iplot(asFigure=True))


