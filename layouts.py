# -*- coding: utf-8 -*-
"""
Created on Wed Apr 21 17:00:08 2021

@author: Bruno
"""
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px

import pandas as pd
import os

cwd = os.getcwd()
rep ="./data/"
filename = "data.xlsx"

with pd.ExcelFile(rep+filename) as xls:
    #print(xls.sheet_names )
    df = pd.read_excel(xls, "Sheet2")

#remove unnamed
for k in df :
    if "Unnamed" in k :
        df = df.drop(columns=[k])
# Convert to timedata
df["date"] = pd.to_datetime(df["date"])

# Replace missing count with 0
df['total_cases'] = df['total_cases'].fillna(0)
df['total_deaths'] = df['total_deaths'].fillna(0)

#convert count to int
df['total_cases'] = df['total_cases'].astype(int)
df['total_deaths'] = df['total_deaths'].astype(int)

dfFR = df[df.iso_code == 'FRA']

fig = px.line(dfFR, x="date", y="total_cases", title='Number of cases in France')

layout0 = html.Div([
    html.H3('Root'),

    html.Div(id='app-1-display-value'),
    dcc.Link('Go to App 1', href='/apps/app1'),
    html.Div(id='app-2-display-value'),
    dcc.Link('\nGo to App 2', href='/apps/app2')
])

layout1 = html.Div([
    html.H3('App 1'),
    dcc.Dropdown(
        id='app-1-dropdown',
        options=[
            {'label': 'App 1 - {}'.format(i), 'value': i} for i in [
                'NYC', 'MTL', 'LA'
            ]
        ]
    ),
    html.Div(id='app-1-display-value'),
    dcc.Link('Go to App 2', href='/apps/app2'),
    html.Div(id='app-1-display-value'),
    dcc.Graph(figure = fig)

])

layout2 = html.Div([
    html.H3('App 2'),
    dcc.Dropdown(
        id='app-2-dropdown',
        options=[
            {'label': 'App 2 - {}'.format(i), 'value': i} for i in [
                'NYC', 'MTL', 'LA'
            ]
        ]
    ),
    html.Div(id='app-2-display-value'),
    dcc.Link('Go to App 1', href='/apps/app1')
])