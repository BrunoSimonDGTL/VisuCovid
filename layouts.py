# -*- coding: utf-8 -*-
"""
Created on Wed Apr 21 17:00:08 2021

@author: Bruno
"""
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import os
import plotly.graph_objects as go
import numpy as np

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
fig.update_layout(paper_bgcolor='rgba(0,0,0,0)')


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
fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)')


columns = ["location","date", "stringency_index"]
dfSIWorld = df[columns].groupby(['date', 'location']).mean().reset_index()
dfSIWorld = dfSIWorld.groupby('date').mean().reset_index()
fig3 = px.line(dfSIWorld, x="date", y="stringency_index", title='Mean SI in the World')
fig3.update_layout(paper_bgcolor='rgba(0,0,0,0)')

filename = "govDept.csv"
dfDebt = pd.read_csv(rep+filename)
dfDebt.pop("Flag Codes")
dfDebt['TIME']= pd.to_datetime(dfDebt['TIME'], format='%Y')
dfDebt.rename(columns = {"TIME": "Year"}, inplace = True)
np.unique(dfDebt.Year)
fig4 = px.line(dfDebt[dfDebt["LOCATION"]=="USA"], x="Year", y="Value", title='Debt USA')
fig4.update_layout(paper_bgcolor='rgba(0,0,0,0)')


filename = "taux_chomage.csv"
dfChom = pd.read_csv(rep+filename)
dfChom['TIME']= pd.to_datetime(dfChom['TIME'], format='%Y-%m')
dfChom.rename(columns = {"TIME": "Date"}, inplace = True)
dfChom.pop("Flag Codes")
fig5 = px.line(dfChom[dfChom["LOCATION"]=="ESP"], x="Date", y="Value", title='Unemployment  ESP')
fig5.update_layout(paper_bgcolor='rgba(0,0,0,0)')

layout0 = html.Div([
    
    html.H1('Effect of Covid 19 on the economy'),
    html.H3("Introduction Global"),
    html.H4('COVID-19 is not only a global pandemic and public health crisis; it has also severely affected the global economy and financial markets. Significant reductions in income, a rise in unemployment, and disruptions in the transportation, service, and manufacturing industries are among the consequences of the disease mitigation measures that have been implemented in many countries. It has become clear that most governments in the world underestimated the risks of rapid COVID-19 spread and were mostly reactive in their crisis response. As disease outbreaks are not likely to disappear in the near future, proactive international actions are required to not only save lives but also protect economic prosperity.'),
    dbc.CardHeader(
            [
                html.H3("Guide general",className="card-title"),
                html.P("To study the effect of Covid19 on the economy, we have first studied the evaluation of the number of Covid19 cases in France, \nthen the normalized oil price and bourse value variation in terms of time, then we have studied the mean SI in the world, next we have shown the debt USA variation in the Covid pendemic, in the end, we presented the unemployment ESP.",className="card-text"),
            ],
            style={"width": "28rem"},
            
        ),
    
    
    html.Div(id='app-1-display-value'),
    dcc.Link('Number of cases Covid19 in France', href='/apps/app1'),
    html.Div(id='app-2-display-value'),
    dcc.Link('\nNormalized oil price and Bourse value', href='/apps/app2'),
    html.Div(id='app-3-display-value'),
    dcc.Link('\nMean SI in the world', href='/apps/app3'),
    html.Div(id='app-4-display-value'),
    dcc.Link('\nDebt USA', href='/apps/app4'),
    html.Div(id='app-5-display-value'),
    dcc.Link('\nThe unemployment ESP', href='/apps/app5'),
    
    
    
    html.H5("For more infromation,please contact us with LaPlateforme "),
    ],
    
 )
    


layout1 = html.Div([
    html.H1('Number of cases Covid19 in France'),
    html.Div(id='app-1-display-value'),
    dcc.Link('Go to back', href='/apps'),
    dcc.Graph(figure = fig),
    dbc.CardHeader(
            [
                html.H3("Analyse the number of cases Covid19 in France",className="card-title"),
                html.P("The COVID-19 pandemic in France is part of the worldwide pandemic of coronavirus disease 2019 (COVID-19) caused by severe acute respiratory syndrome coronavirus 2 (SARS-CoV-2). The virus was confirmed to have reached France on 24 January 2020, when the first COVID-19 case in both Europe and France was identified in Bordeaux.From August 2020, there was an increase in the rate of infection and on 10 October 2020, France set a record number of new infections in a 24-hour period in Europe with 26,896 recorded. The increase caused France to enter a second nationwide lockdown on 28 October 2020.On 31 March 2021, Macron announced a third national lockdown to commence on 3 April 2021, which mandated for all of April 2021; the closure of non-essential shops, the suspension of school attendance, a ban on all domestic travel and a nationwide curfew from 7pm-6am.",className="card-text"),
            ],
            style={"width": "28rem"},
            
        )


])

layout2 = html.Div([
    html.H1('Normalized oil price and Bourse value'),
    html.Div(id='app-2-display-value'),
    dcc.Link('Go to back', href='/apps'),
    dcc.Graph(figure = fig2),
    dbc.CardHeader(
            [
                html.H3("Analyse the oil price and Bourse value in Covid19 pandemic",className="card-title"),
                html.P("The crash caused a short-lived bear market, and in April 2020 global stock markets re-entered a bull market, though U.S. market indices did not return to January 2020 levels until November 2020.The crash signaled the beginning of the COVID-19 recession. The 2020 stock market crash followed a decade of economic prosperity and sustained global growth after recovery from the financial crisis of 2007–2008. Global unemployment was at its lowest in history, whilst quality of life was generally improving across the world. However, in 2020, the COVID-19 pandemic, the most impactful pandemic since the Spanish flu, began, decimating the economy.",className="card-text"),
            ],
            style={"width": "28rem"},
            
        )
])

layout3 = html.Div([
    html.H1('Mean SI in the world'),
    html.Div(id='app-3-display-value'),
    dcc.Link('Go to back', href='/apps'),
    dcc.Graph(figure = fig3),
    dbc.CardHeader(
            [
                html.H3("Analyse the Mean SI in the world in Covid19 pandemic",className="card-title"),
                html.P("The analysis of the Covid stringency index during the steady-state period in particular shows patterns of multi-modal curves,which signals an attempt by governments to adjust their decrees of social distancing in the face of the evolution of Covid-19 and also to economic pressures that imposed reopening of certain commercial activities in spite of the level of contagion of the disease, as has been reportd in low and middle income countries.",className="card-text"),
            ],
            style={"width": "28rem"},
            
        )
])

layout4 = html.Div([
    html.H1('Debt USA'),
    html.Div(id='app-4-display-value'),
    dcc.Link('Go to back', href='/apps'),
    dcc.Graph(figure = fig4),
    dbc.CardHeader(
            [
                html.H3("Analyse the Debt USA",className="card-title"),
                html.P("Due to the COVID-19 pandemic, Congress and President Trump enacted the $2.2 trillion Coronavirus Aid, Relief, and Economic Security Act (CARES) on March 18, 2020. The Congressional Budget Office estimated that the budget deficit for fiscal year 2020 would increase to $3.3 trillion or 16% GDP, more than triple that of 2019 and the largest deficit since 1945 (measured as percentage of GDP). CBO also forecast the debt held by the public would rise to 98% GDP in 2020, compared with 79% in 2019 and 35% in 2007 before the Great Recession",className="card-text"),
            ],
            style={"width": "28rem"},
            
        )
])
            
            
layout5 = html.Div([
    html.H1('The unemployment ESP'),
    html.Div(id='app-5-display-value'),
    dcc.Link('Go to back', href='/apps'),
    dcc.Graph(figure = fig5),
    dbc.CardHeader(
            [
                html.H3("Analyse unemployment ESP",className="card-title"),
                html.P("A number of OECD countries modified their access to, and the duration of, unemployment benefits, with some changes likely to benefit migrants in particular as these often have less stable contracts and a lower contribution history. Belgium, for example, included the COVID‑19 pandemic within its “temporary unemployment due to force majeure” regime. As a result, workers do not need to prove a sufficient number of days as an employed worker in order to receive support. Similarly, in Spain, the minimum duration of work required to qualify for unemployment benefits, 360 working days during the last 6 years, was suspended. In Ireland, any person who lost their job due to the pandemic can receive COVID‑19 unemployment benefits. France modified the regulations for partial unemployment to employees affected by the lockdown. Sweden extended the period of subsidised jobs by one year; a measure that particularly benefits migrants – especially recent arrivals – as these are a main target group.",className="card-text"),
            ],
            style={"width": "28rem"},
            
        )
])