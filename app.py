# -*- coding: utf-8 -*-
"""
Created on Wed Apr 21 17:01:42 2021

@author: Bruno
"""
import dash



app = dash.Dash(__name__, suppress_callback_exceptions=False)
server = app.server