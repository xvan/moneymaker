#!/usr/bin/env python3
from querydispatcher import QueryDispatcher

qd = QueryDispatcher()
qd.get_history('ALUA.BA', '2010-01-01', '2020-01-01')

