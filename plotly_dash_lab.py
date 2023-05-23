import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

app = dash.Dash(__name__)

app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                                  'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                                options=[
                                                    {'label': 'All Sites', 'value': 'ALL'},
                                                    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                                ],
                                                value='ALL',
                                                placeholder="Select a Launch Site here",
                                                searchable=True
                                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(id='output-site'),
                                html.Br(),

                                # TASK 3: Add a slider to select payload range
                                html.P("Payload range (Kg):"),
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0',
                                                        2500: '2500',
                                                        5000: '5000',
                                                        7500: '7500',
                                                        10000: '10000'},
                                                value=[min_payload, max_payload]),
                                html.Div(id='output-container-range-slider'),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(id='output-graph'),
                                ])

# TASK 2:   Add a callback function to render the success-pie-chart
#           success-pie-chart gets data from dropdown, update_graph() and get_pie_chart()
@app.callback(Output(component_id='output-site', component_property='children'),
                Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(site_dropdown):
    if site_dropdown == 'ALL':
        df = spacex_df[spacex_df['class'] == 1]
        fig = px.pie(df, values='class', names='Launch Site', title='Total Success Launches By Site')
        return dcc.Graph(figure=fig)
    else:
        df = spacex_df[spacex_df['Launch Site'] == site_dropdown]
        df = df.groupby(['Launch Site', 'class']).size().reset_index(name='class count')
        fig = px.pie(df, values='class count', names='class', title='Total Success Launches for site '+site_dropdown)
        return dcc.Graph(figure=fig)


# TASK 4: Add a callback function to render the success-payload-scatter-chart scatter plot
@app.callback(Output(component_id='output-graph', component_property='children'),
                [Input(component_id='site-dropdown', component_property='value'),
                Input(component_id='payload-slider', component_property='value')])
def update_graph(site_dropdown, payload_slider):
    low, high = payload_slider
    df = spacex_df[spacex_df['Payload Mass (kg)'].between(low, high)]
    if site_dropdown == 'ALL':
        fig = px.scatter(df, x='Payload Mass (kg)', y='class', color='Booster Version Category', title='Correlation between Payload and Success for all Sites')
        return dcc.Graph(figure=fig)
    else:
        df = df[df['Launch Site'] == site_dropdown]
        fig = px.scatter(df, x='Payload Mass (kg)', y='class', color='Booster Version Category', title='Correlation between Payload and Success for '+site_dropdown)
        return dcc.Graph(figure=fig)


if __name__ == '__main__':
    app.run_server()
