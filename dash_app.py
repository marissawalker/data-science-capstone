# Import required libraries
import pandas as pd
import dash
# import dash_html_components as html
# import dash_core_components as dcc
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
from matplotlib import pyplot as plt

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
sites=spacex_df['Launch Site'].unique().tolist()
sites.append('All Sites')
# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                html.P('Select launch site:'),
                                dcc.Dropdown(options=sites, 
                                             value='All Sites',id='site-dropdown'),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(min_payload,max_payload,id='payload-slider',value=[min_payload,max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart',component_property='figure'),
              Input(component_id='site-dropdown',component_property='value'))
def get_pie(site):
    labels = {0:'Failure', 1:'Success'}
    if site=='All Sites':
        fig = px.pie(names = spacex_df['class'].map(labels))
    else:
        fig = px.pie(names = spacex_df[spacex_df['Launch Site']==site]['class'].map(labels))
    return(fig)
    
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart',component_property='figure'),
              Input(component_id='site-dropdown',component_property='value'),
              Input(component_id='payload-slider',component_property='value'))
def get_scatter(site, payload_range):
    if site=='All Sites':
        df = spacex_df[(spacex_df['Payload Mass (kg)']>payload_range[0]) 
        & (spacex_df['Payload Mass (kg)']< payload_range[1])].reset_index()
    else:
        df = spacex_df[(spacex_df['Launch Site']==site) & (spacex_df['Payload Mass (kg)']>payload_range[0]) 
        & (spacex_df['Payload Mass (kg)']< payload_range[1])].reset_index()
    fig = go.Figure(go.Scatter(x=df['Payload Mass (kg)'],y=df['class'],mode='markers'))
    
    fig.update_layout(
        title={
            'text': "Launch Outcomes from %s with Payload between %s and %s kg" %(site,payload_range[0],payload_range[1]),
            'y':0.9, 'x':0.5,'xanchor': 'center','yanchor': 'top'},
        xaxis_title = "Payload Mass (kg)",
        font=dict(size=18),
        yaxis = dict(
            tickmode = 'array',
            tickvals = [0,1],
            ticktext = ['Failure','Success']
        )
    )

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
