# -*- coding: utf-8 -*-
"""
Created on Mon May  3 09:04:44 2021

@author: jing

figure de pouvoir d'achat
"""

import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import matplotlib.pyplot as plt 
import pandas as pd
import os
import plotly.graph_objs as go
import numpy as np
from plotly.offline import init_notebook_mode, iplot, plot

cwd = os.getcwd()
rep ="./data/"
filename = "pouvoir d'achat trier.xlsx"

with pd.ExcelFile(rep+filename) as xls:
    #print(xls.sheet_names )
    df = pd.read_excel(xls)
    
    
#print(df.loc["France","2009"])
dffr = df.iloc[11,3:]

x=np.zeros(13)
y=np.zeros(13)

for i in range(13):
    x[i]=dffr.index[i]
    y[i]=dffr.loc[dffr.index[i]]

   
trace1 = go.Scatter(
                    x = x,
                    y = y,
                    mode = "lines",
                    name = "pouvoir d'achat",
                    marker = dict(color = 'rgba(16, 112, 2, 0.8)'),
                    text = "annee")

data = [trace1]

layout = dict(title = 'pourvoir achat France',
              xaxis = dict(title = 'Annee',ticklen = 5,zeroline= False)
)

fig = dict(data = data, layout = layout)

iplot(fig)


#print(dffr.index[0],"\n",dffr.loc['2008'])
# #remove unnamed
# for k in df :
#     if "Unnamed" in k :
#         df = df.drop(columns=[k])
# # Convert to timedata
# df["date"] = pd.to_datetime(df["date"])

# # Replace missing count with 0
# df['total_cases'] = df['total_cases'].fillna(0)
# df['total_deaths'] = df['total_deaths'].fillna(0)

# #convert count to int
# df['total_cases'] = df['total_cases'].astype(int)
# df['total_deaths'] = df['total_deaths'].astype(int)

# dfFR = df[df.iso_code == 'FRA']

# fig = px.line(dfFR, x="date", y="total_cases", title='Number of cases in France')