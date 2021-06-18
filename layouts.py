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
import plotly.graph_objects as go

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


with pd.ExcelFile(rep+filename) as xls:
    print(xls.sheet_names )
    df = pd.read_excel(xls, "Sheet2")

filename = "SPGlobal1200.xls"
with pd.ExcelFile(rep+filename) as xls:
    print(xls.sheet_names )
    dfBourse = pd.read_excel(xls, skiprows = 6)
dfBourse.rename(columns = {"Effective date ": "Date", "S&P GLOBAL 1200" : "Global 1200" }, inplace = True)
mask_date= dfBourse.Date > pd.Timestamp(2018, 1, 1) #Year, month, day

filename = "RWTCd.xls"
with pd.ExcelFile(rep+filename) as xls:
    print(xls.sheet_names )
    dfOil = pd.read_excel(xls, "Data 1", skiprows = 2)

dfOil.rename(columns = {"Cushing, OK WTI Spot Price FOB (Dollars per Barrel)": "Price [$]"}, inplace = True)

mask_date_Oil= dfOil.Date > pd.Timestamp(2018, 1, 1)
mask_date_B= dfBourse.Date > pd.Timestamp(2018, 1, 1) #Year, month, day
selected_country = "United States"
# selected_country = "France"
#display(df[df["location"]==selected_country])

trace1 = go.Scatter(
                    x=(dfOil[mask_date_Oil])["Date"],
                    y=(dfOil[mask_date_Oil])["Price [$]"]/max((dfOil[mask_date_Oil])["Price [$]"]),
                    mode = "lines",
                    name = "Oil, WTI Spot Price",
                    #line = dict(color = 'red'),
                    #marker = dict(color = 'red'),
                    )

trace2 = go.Scatter(
                    x=(dfBourse[mask_date])["Date"],
                    y=(dfBourse[mask_date])["Global 1200"]/max((dfBourse[mask_date])["Global 1200"]),
                    mode = "lines",
                    name = "Bourse Global 1200",
                    )


trace3 = go.Scatter(
                    x=(df[df["location"]==selected_country])["date"],
                    y=(df[df["location"]==selected_country])["stringency_index"]/100,
                    mode = "lines",
                    name = "stringency_index " + selected_country,
                    )
data = [trace1, trace2, trace3]

layout = dict(title = 'Normalized oil price and Bourse value',
               xaxis = dict(title = 'Date',ticklen = 5,zeroline= False),
             )

fig2 = go.Figure(dict(data = data, layout = layout))

layout0 = html.Div([
    html.H3('Root'),

    html.Div(id='app-1-display-value'),
    dcc.Link('Go to App 1', href='/apps/app1'),
    html.Div(id='app-2-display-value'),
    dcc.Link('\nGo to App 2', href='/apps/app2')
])

layout1 = html.Div([
    html.H1('App 1'),
    dcc.Dropdown(
        id='app-1-dropdown',
        options=[
            {'label': 'App 1 - {}'.format(i), 'value': i} for i in [
                'NYC', 'MTL', 'LA' ] ]
    ),
    html.Div(id='app-1-display-value'),
    dcc.Link('Go to App 2', href='/apps/app2'),
    dcc.Graph(figure = fig),


])

layout2 = html.Div([
    html.H3('App 2'),
    dcc.Dropdown(
        id='app-2-dropdown',
        options=[
            {'label': 'App 2 - {}'.format(i), 'value': i} for i in [
                'NYC', 'MTL', 'LA' ] ]
    ),
    html.Div(id='app-2-display-value'),
    dcc.Link('Go to App 1', href='/apps/app1'),
    dcc.Graph(figure = fig2)
])