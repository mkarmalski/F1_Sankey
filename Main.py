import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df_driver = pd.read_csv('/home/emkaerr/PycharmProjects/F1_Sankey/Drivers.csv')
df_team = pd.read_csv('/home/emkaerr/PycharmProjects/F1_Sankey/Teams.csv')
ind_driver = pd.read_csv('/home/emkaerr/PycharmProjects/F1_Sankey/Driver_index.csv')
ind_team = pd.read_csv('/home/emkaerr/PycharmProjects/F1_Sankey/Team_index.csv')

app.layout = html.Div([
    html.H2('Formula 1 Sankey Diagram'),
    html.Hr(),
    html.Div([
        html.H4('Choose Season'),
        html.Br(),
        dcc.Slider(
            id='slider-1',
            min=df_driver['Year'].min(),
            max=df_driver['Year'].max(),
            step=1,
            value=2020,
            marks={i: str(i) for i in range(df_driver['Year'].min(), df_driver['Year'].max() + 1, 5)},
            tooltip={'placement': 'bottom'}
        ),
        html.Br(),
        dcc.Tabs(
            id='tabs_1',
            children=[
                dcc.Tab(label='Drivers', value='tab1'),
                dcc.Tab(label='Teams', value='tab2'),

            ],
            value='tab1'),
    ],
        style={'width': '80%', 'textAlign': 'center', 'margin': '0 auto'}
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
    [Input('slider-1', 'value'),
     Input('tabs_1', 'value')]
)
def update_graph(selected_year,tab):

    if tab == 'tab1':
        df2 = df_driver.query(f'Year=={selected_year}')
        trace = go.Sankey(
            arrangement='snap',
            node=dict(
                pad=5,
                thickness=100,
                label=ind_driver['Code'],
                customdata=ind_driver['Name'],
                hovertemplate='%{customdata} (%{label})'
            ),
            link=dict(
                source=df2['Source'],
                target=df2['Target'],
                value=df2['Value'],
                customdata=df2['Driver'],
                hovertemplate='%{customdata} has %{value} positions %{target.customdata}'
            ),
            orientation='v',
            valueformat='.'

        )
    else:
        df2 = df_team.query(f'Year=={selected_year}')
        trace = go.Sankey(
            arrangement='snap',
            node=dict(
                pad=5,
                thickness=100,
                label=ind_team['Name'],
                customdata=ind_team['Name'],
                hovertemplate='%{customdata} (%{label})'
            ),
            link=dict(
                source=df2['Source'],
                target=df2['Target'],
                value=df2['Value'],
                customdata=df2['Team'],
                hovertemplate='%{customdata} has %{value} positions %{target.customdata}'
            ),
            orientation='v',
            valueformat='.'

        )
    return {
        'data': [trace],
        'layout': go.Layout(
            height=800,

        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)
