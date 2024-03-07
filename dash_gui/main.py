"""
### Without automatic refreshing: ###

import dash
from dash import dcc, html
import plotly.graph_objs as go
import requests
from datetime import datetime, timedelta
import pytz

# ThingSpeak read API endpoint for the last 5 entries
url = 'https://api.thingspeak.com/channels/{}/feeds.json'.format('2448118')
# Replace 'CHANNEL_ID' with your ThingSpeak channel ID

# Your ThingSpeak read API key
api_key = 'IXT4T5APCGA3QSMF'

# Query parameters for the API request
params = {'api_key': api_key, 'results': 5}  # Fetch the last 5 entries

# Fetch data from ThingSpeak
response = requests.get(url, params=params)

# Extract data from response
data = response.json()

# Extract values and dates from the last 5 entries
values = [float(entry['field1']) for entry in data['feeds']]

# Adjust for time zone difference
dates = [datetime.strptime(entry['created_at'], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Europe/Budapest')) - timedelta(hours=0) for entry in data['feeds']]
#dates = [datetime.strptime(entry['created_at'], '%Y-%m-%dT%H:%M:%SZ') for entry in data['feeds']]

# Create Dash app
app = dash.Dash(__name__)
server = app.server

# Define layout of the app
app.layout = html.Div([
    html.H1("N. Z. - Kaptármérleg tömeg diagram", style={'textAlign': 'center'}),
    dcc.Graph(
        id='line-chart',
        figure={
            'data': [
                go.Scatter(
                    x=dates,
                    y=values,
                    mode='lines+markers',
                    name='Field Values'
                )
            ],
            'layout': go.Layout(
                title='Utolsó 5 mért érték',
                xaxis={'title': 'Dátum'},
                yaxis={'title': 'Tömeg'}
            )
        }
    )
])

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)



### With automatic refreshing: ###

import dash
from dash import dcc, html, callback_context
import plotly.graph_objs as go
import requests
from datetime import datetime, timedelta
import pytz
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import requests
import pytz

# Function to fetch data from ThingSpeak
def fetch_data():
    # ThingSpeak read API endpoint for the last 5 entries
    url = 'https://api.thingspeak.com/channels/{}/feeds.json'.format('2448118')
    # Replace 'CHANNEL_ID' with your ThingSpeak channel ID

    # Your ThingSpeak read API key
    api_key = 'IXT4T5APCGA3QSMF'

    # Query parameters for the API request
    params = {'api_key': api_key, 'results': 5}  # Fetch the last 5 entries

    # Fetch data from ThingSpeak
    response = requests.get(url, params=params)

    # Extract data from response
    data = response.json()

    # Extract values and dates from the last 5 entries
    values = [float(entry['field1']) for entry in data['feeds']]
    # Adjust for time zone difference
    dates = [datetime.strptime(entry['created_at'], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Europe/Budapest')) - timedelta(hours=0) for entry in data['feeds']]

    return dates, values

# Create Dash app
app = dash.Dash(__name__)

# Define layout of the app
app.layout = html.Div([
    html.H1("N. Z. kaptármérleg tömege", style={'textAlign': 'center'}),
    dcc.Graph(
        id='line-chart',
        figure={
            'data': [
                go.Scatter(
                    x=[],
                    y=[],
                    mode='lines+markers',
                    name='Field Values'
                )
            ],
            'layout': go.Layout(
                title='Utolsó 5 mért érték',
                xaxis={'title': 'Date'},
                yaxis={'title': 'Mass'}
            )
        }
    ),
    dcc.Interval(
        id='interval-component',
        interval=5*60*1000,  # in milliseconds # now 5 minutes
        n_intervals=0
    )
])

# Callback to update the graph data
@app.callback(
    Output('line-chart', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_graph(n):
    dates, values = fetch_data()
    return {
        'data': [
            go.Scatter(
                x=dates,
                y=values,
                mode='lines+markers',
                name='Field Values'
            )
        ],
        'layout': go.Layout(
            title='Utolsó 5 mért érték',
            xaxis={'title': 'Date'},
            yaxis={'title': 'Mass'}
        )
    }

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)


# Then, open a web browser and navigate to http://127.0.0.1:8050/ to see the Dash app.

"""
"""

import dash
from dash import dcc, html
import plotly.graph_objs as go
import requests
from datetime import datetime, timedelta
from dash.dependencies import Input, Output, State
import pytz

# Function to fetch data from ThingSpeak
def fetch_data(start_date, end_date):
    if start_date == 'last_3_days':
        start_date = datetime.now() - timedelta(days=3)
    else:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
    if end_date == 'today':
        end_date = datetime.now()
    else:
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

    # ThingSpeak read API endpoint for the specified timeframe
    url = 'https://api.thingspeak.com/channels/{}/feeds.json'.format('2448118')
    # Replace 'CHANNEL_ID' with your ThingSpeak channel ID

    # Your ThingSpeak read API key
    api_key = 'IXT4T5APCGA3QSMF'

    # Query parameters for the API request
    params = {'api_key': api_key, 'start': start_date.strftime('%Y-%m-%dT%H:%M:%SZ'), 'end': end_date.strftime('%Y-%m-%dT%H:%M:%SZ')} 

    # Fetch data from ThingSpeak
    response = requests.get(url, params=params)

    # Extract data from response
    data = response.json()

    # Extract values and dates from the specified timeframe
    values = [float(entry['field1']) for entry in data['feeds']]
    # Adjust for time zone difference
    dates = [datetime.strptime(entry['created_at'], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Europe/Budapest')) - timedelta(hours=0) for entry in data['feeds']]
    #dates = [datetime.strptime(entry['created_at'], '%Y-%m-%dT%H:%M:%SZ') for entry in data['feeds']]

    return dates, values

# Create Dash app
app = dash.Dash(__name__)

# Define layout of the app
app.layout = html.Div([
    html.H1("N. Z. hive scale app", style={'textAlign': 'center'}),
    html.Label('Select timeframe:'),
    dcc.Dropdown(
        id='timeframe-dropdown',
        options=[
            {'label': 'Last 3 days', 'value': 'last_3_days'},
            {'label': 'Custom timeframe', 'value': 'custom_timeframe'}
        ],
        value='last_3_days',
        clearable=False
    ),
    html.Div(id='date-picker-container', style={'display': 'none'}, children=[
        html.Label('Start date:'),
        dcc.DatePickerSingle(
            id='start-date-picker',
            display_format='YYYY-MM-DD',
            style={'marginBottom': 10}
        ),
        html.Label('End date:'),
        dcc.DatePickerSingle(
            id='end-date-picker',
            display_format='YYYY-MM-DD',
            style={'marginBottom': 10}
        )
    ]),
    dcc.Graph(
        id='line-chart',
        figure={
            'data': [],
            'layout': go.Layout(
                title='Utolsó 5 mért érték',
                xaxis={'title': 'Date'},
                yaxis={'title': 'Mass'}
            )
        }
    ),
])

# Callback to display date pickers based on selected timeframe
@app.callback(
    Output('date-picker-container', 'style'),
    [Input('timeframe-dropdown', 'value')]
)
def display_date_pickers(timeframe):
    if timeframe == 'custom_timeframe':
        return {'display': 'block'}
    else:
        return {'display': 'none'}

# Callback to update the graph data
@app.callback(
    Output('line-chart', 'figure'),
    [Input('timeframe-dropdown', 'value'),
     Input('start-date-picker', 'date'),
     Input('end-date-picker', 'date')]
)
def update_graph(timeframe, start_date, end_date):
    if timeframe == 'custom_timeframe':
        if start_date is None or end_date is None:
            return {'data': [], 'layout': go.Layout(title='Custom timeframe selected')}
        else:
            dates, values = fetch_data(start_date, end_date)
            return {
                'data': [
                    go.Scatter(
                        x=dates,
                        y=values,
                        mode='lines+markers',
                        name='Field Values'
                    )
                ],
                'layout': go.Layout(
                    title='Custom timeframe selected',
                    xaxis={'title': 'Date'},
                    yaxis={'title': 'Mass'}
                )
            }
    else:
        dates, values = fetch_data('last_3_days', 'today')
        return {
            'data': [
                go.Scatter(
                    x=dates,
                    y=values,
                    mode='lines+markers',
                    name='Field Values'
                )
            ],
            'layout': go.Layout(
                title='Last 3 days selected',
                xaxis={'title': 'Date'},
                yaxis={'title': 'Mass'}
            )
        }

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)

"""


import dash
from dash import dcc, html
import plotly.graph_objs as go
import requests
from datetime import datetime, timedelta
from dash.dependencies import Input, Output, State
import pytz

# Function to fetch data from ThingSpeak
def fetch_data(start_date, end_date):
    if start_date == 'last_3_values':
        start_date = datetime.now() - timedelta(days=5)
    else:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
    if end_date == 'today':
        end_date = datetime.now()
    else:
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

    # ThingSpeak read API endpoint for the specified timeframe
    url = 'https://api.thingspeak.com/channels/{}/feeds.json'.format('2448118')
    # Replace 'CHANNEL_ID' with your ThingSpeak channel ID

    # Your ThingSpeak read API key
    api_key = 'IXT4T5APCGA3QSMF'

    # Query parameters for the API request
    params = {'api_key': api_key, 'start': start_date.strftime('%Y-%m-%dT%H:%M:%SZ'), 'end': end_date.strftime('%Y-%m-%dT%H:%M:%SZ')} 

    # Fetch data from ThingSpeak
    response = requests.get(url, params=params)

    # Extract data from response
    data = response.json()

    # Extract values and dates from the specified timeframe
    values = [float(entry['field1']) for entry in data['feeds']]
    # Adjust for time zone difference
    dates = [datetime.strptime(entry['created_at'], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Europe/Budapest')) - timedelta(hours=0) for entry in data['feeds']]
    #dates = [datetime.strptime(entry['created_at'], '%Y-%m-%dT%H:%M:%SZ') for entry in data['feeds']]

    return dates, values

# Create Dash app
app = dash.Dash(__name__)

# Define layout of the app
app.layout = html.Div([
    html.H1("N. Z. kaptármérleg tömege", style={'textAlign': 'center'}),
    html.Label('Select timeframe:'),
    dcc.Dropdown(
        id='timeframe-dropdown',
        options=[
            {'label': 'Last 3 days', 'value': 'last_3_values'},
            {'label': 'Custom timeframe', 'value': 'custom_timeframe'}
        ],
        value='last_3_values',
        clearable=False
    ),
    html.Div(id='date-picker-container', style={'display': 'none'}, children=[
        html.Label('Start date:'),
        dcc.DatePickerSingle(
            id='start-date-picker',
            display_format='YYYY-MM-DD',
            style={'marginBottom': 10}
        ),
        html.Label('End date:'),
        dcc.DatePickerSingle(
            id='end-date-picker',
            display_format='YYYY-MM-DD',
            style={'marginBottom': 10}
        )
    ]),
    dcc.Graph(
        id='line-chart',
        figure={
            'data': [],
            'layout': go.Layout(
                title='Utolsó 5 mért érték',
                xaxis={'title': 'Date'},
                yaxis={'title': 'Mass'}
            )
        }
    ),
    dcc.Interval(
        id='interval-component',
        interval=5*60*1000,  # in milliseconds # Currently 5 minutes
        n_intervals=0
    )
])

# Callback to display date pickers based on selected timeframe
@app.callback(
    Output('date-picker-container', 'style'),
    [Input('timeframe-dropdown', 'value')]
)
def display_date_pickers(timeframe):
    if timeframe == 'custom_timeframe':
        return {'display': 'block'}
    else:
        return {'display': 'none'}

# Callback to update the graph data
@app.callback(
    Output('line-chart', 'figure'),
    [Input('timeframe-dropdown', 'value'),
     Input('start-date-picker', 'date'),
     Input('end-date-picker', 'date'),
     Input('interval-component', 'n_intervals')]
)
def update_graph(timeframe, start_date, end_date, n_intervals):
    if timeframe == 'custom_timeframe':
        if start_date is None or end_date is None:
            return {'data': [], 'layout': go.Layout(title='Custom timeframe selected')}
        else:
            dates, values = fetch_data(start_date, end_date)
            return {
                'data': [
                    go.Scatter(
                        x=dates,
                        y=values,
                        mode='lines+markers',
                        name='Field Values'
                    )
                ],
                'layout': go.Layout(
                    title='Custom timeframe selected',
                    xaxis={'title': 'Date'},
                    yaxis={'title': 'Mass'}
                )
            }
    else:
        dates, values = fetch_data('last_3_values', 'today')
        return {
            'data': [
                go.Scatter(
                    x=dates,
                    y=values,
                    mode='lines+markers',
                    name='Field Values'
                )
            ],
            'layout': go.Layout(
                title='Last 3 days selected',
                xaxis={'title': 'Date'},
                yaxis={'title': 'Mass'}
            )
        }

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
