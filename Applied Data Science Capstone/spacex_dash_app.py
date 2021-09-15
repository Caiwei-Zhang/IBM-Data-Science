# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
launchsites = spacex_df['Launch Site'].unique().tolist()

def get_options(option, ifall):
    lst = [{'label': x, 'value': x} for x in option]
    if ifall == 1:
        lst.insert(0, {'label':"All Sites", 'value': "All Sites"})
    return lst

[{'label': x, 'value': x} for x in launchsites].insert(0, {'label':"All Sites", 'value': "All Sites"})
# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Div([
                                    dcc.Dropdown(id='site-dropdown', 
                                    options=get_options(launchsites, ifall=1),
                                    value="ALL Sites",
                                    placeholder='Select a Launch Site here',
                                    searchable=True)
                                ]),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                html.Div([
                                    dcc.RangeSlider(id = 'payload-slider', 
                                    min=0, max=10000,step=1000,
                                    value=[min_payload,max_payload],
                                    ) #marks={i: '{}'.format(2500*i) for i in range(5)}
                                ]),
                                html.Br(),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart'))
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback( Output(component_id = 'success-pie-chart', component_property = 'figure'),
                [Input(component_id = 'site-dropdown', component_property = 'value')])

def get_graph1(input_site):
    if input_site == "All Sites":
        pie_fig = px.pie(spacex_df, values='class', names='Launch Site', title='Total Success Launches By Site')
    else:
        # select data based on the input site 
        site_data = spacex_df[spacex_df['Launch Site'] == input_site]
        pie_fig = go.Figure(data=go.Pie(labels=['Success','Failed'],
                            values=site_data['class'].value_counts().values.tolist()))
        #pie_fig = px.pie(site_data, values='class', names='class', title='Total Success Launches for Site ' + input_site) #names='Launch Site',
    return pie_fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback( Output(component_id = 'success-payload-scatter-chart', component_property = 'figure'),
                [Input(component_id = 'site-dropdown', component_property = 'value'),
                 Input(component_id = 'payload-slider', component_property = 'value')])

def get_graph2(input_site, input_payload):
    if input_site == "All Sites":
        sct_data = spacex_df[(spacex_df['Payload Mass (kg)'] >= input_payload[0]) & (spacex_df['Payload Mass (kg)'] <= input_payload[1])]
        sct_fig = px.scatter(sct_data, x='Payload Mass (kg)', y='class', color='Booster Version Category', 
                             title='Correlation between Payload and Success for all Sites')
    else:
        # select data based on the input site 
        sct_data = spacex_df[(spacex_df['Launch Site'] == input_site) & (spacex_df['Payload Mass (kg)'] >= input_payload[0]) & (spacex_df['Payload Mass (kg)'] <= input_payload[1])]
        sct_fig = px.scatter(sct_data, x='Payload Mass (kg)', y='class', color='Booster Version Category', 
                             title='Correlation between Payload and Success for all Sites')
    return sct_fig        

 #go.Figure(data=go.Scatter(x=site_data['Payload Mass (kg)'], y=site_data['class'], 
 #                           color="Booster Version Category", title='Correlation between Payload and Success for all Sites'))
# Run the app
if __name__ == '__main__':
    app.run_server()
