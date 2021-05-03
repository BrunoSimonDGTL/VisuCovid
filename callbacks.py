# -*- coding: utf-8 -*-
"""
Created on Wed Apr 21 17:01:05 2021

@author: Bruno
"""
from dash.dependencies import Input, Output

from app import app

@app.callback(
    Output('app-1-display-value',
          'children'),
    Input('app-1-dropdown',
          'value'))
def display_value(value):
    return 'You have selected "{}"'.format(value)

@app.callback(
    Output('app-2-display-value',
          'children'),
    Input('app-2-dropdown',
          'value'))
def display_value(value):
    return 'You have selected "{}"'.format(value)