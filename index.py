import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from layouts import layout0, layout1, layout2,layout3,layout4,layout5
import callbacks

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/apps/app1':
        return layout1
    elif pathname == '/apps/app2':
        return layout2
    elif pathname == '/apps/app3':
        return layout3
    elif pathname == '/apps/app4':
        return layout4
    elif pathname == '/apps/app5':
        return layout5
    else:
        return layout0

if __name__ == '__main__':
    app.run_server(debug=False, use_reloader=True)
    #app.run_server(debug=True)