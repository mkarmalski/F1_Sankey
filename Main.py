import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv('/home/emkaerr/PycharmProjects/F1_Sankey/F1S.csv')

app.layout = html.Div([
    html.H2('Formula 1 Sankey Diagram'),
    html.Hr(),
    html.Div([
        dcc.Dropdown(
            id='dropdown-1',
            options=[
                {'label': i, 'value': i} for i in df['Year'].unique()
            ],
            value='2020'
        ),
    ],
        style={'width': '20%'}
    ),
    html.Div([
        dcc.Graph(id='graph-1')
    ])

])


@app.callback(
    Output('graph-1', 'figure'),
    [Input('dropdown-1', 'value')]
)
def update_graph(selected_year):
    df2 = df.query(f'Year=={selected_year}')
    trace = go.Scatter(
        x=df2.Driver,
        y=df2.Races
    )
    return {
        'data': [trace]
    }


if __name__ == '__main__':
    app.run_server(debug=True)
