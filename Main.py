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

ind = pd.read_csv('/home/emkaerr/PycharmProjects/F1_Sankey/indexy.csv')

app.layout = html.Div([
    html.H2('Formula 1 Sankey Diagram'),
    html.Hr(),
    html.Div([
        html.H4('Choose Season'),
        html.Br(),
        dcc.Slider(
            id='slider-1',
            min=df['Year'].min(),
            max=df['Year'].max(),
            step=1,
            value=2020,
            marks={i: str(i) for i in range(df['Year'].min(),df['Year'].max()+1,5)},
            tooltip={'placement':'bottom'}
        ),
    ],
        style={'width': '80%','textAlign':'center','margin':'0 auto'}
    ),
    html.Div([
        dcc.Graph(id='graph-1')
    ],
        style={'height': '100%'})

], style={
    'textAlign': 'center'
})


@app.callback(
    Output('graph-1', 'figure'),
    [Input('slider-1', 'value')]
)
def update_graph(selected_year):
    df2 = df.query(f'Year=={selected_year}')
    trace = go.Sankey(
        arrangement='snap',
        node=dict(
            pad=5,
            label=ind['O'],
            x=ind['in']

        ),
        link=dict(
            source=df2['Source'],
            target=df2['Target'],
            value=df2['Value'],
        )
    )
    return {
        'data': [trace],
        'layout': go.Layout(
            height=1000
        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)
