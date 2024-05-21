import dash
from dash import dcc, html
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import requests
from datetime import datetime, timedelta
from dash.dependencies import Input, Output, State
import pytz


import plotly.express as px
import pandas as pd
import io

# Function to fetch data from ThingSpeak
def fetch_data(start_date, end_date):
    if start_date == 'last_5_values':
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
    api_key = 'your-api-key'

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

    
    # Get weather data from OpenWeather API
    start_wthr = start_date.strftime('%Y-%m-%d') #'2024-03-01'
    end_wthr = end_date.strftime('%Y-%m-%d') #'2024-03-20'
    response = requests.get('https://archive-api.open-meteo.com/v1/archive?latitude=46.90792744378672&longitude=16.83663344133228&start_date='+start_wthr+'&end_date='+end_wthr+'&hourly=temperature_2m&timezone=Europe%2FBerlin')
    data = response.json()
    dates_weather = []
    for item in data['hourly']['time']:
        dates_weather.append(item)
    
    temp = []
    for item in data['hourly']['temperature_2m']:
        temp.append(item)
    
    
    return dates, values, dates_weather, temp

# Create Dash app
app = dash.Dash(__name__)
server = app.server

# Define layout of the app
app.layout = html.Div([
    html.H1("N. Z. - Hive scale's data", style={'textAlign': 'center'}),
    html.Label('Select timeframe:'),
    dcc.Dropdown(
        id='timeframe-dropdown',
        options=[
            {'label': 'Last 5 days', 'value': 'last_5_values'},
            {'label': 'Custom timeframe', 'value': 'custom_timeframe'}
        ],
        value='last_5_values',
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
                title='Last 5 value',
                xaxis={'title': 'Date'},
                yaxis={'title': 'Mass'}
            )
        }
    ),
    html.Div([
    dcc.Markdown('''
        #### Dash and Markdown
        **Descripton to here (in the future)**
    ''')
    ]),
    dcc.Interval(
        id='interval-component',
        interval=5*60*1000,  # in milliseconds # Currently 5 minutes
        n_intervals=0
    ),
    html.Div(
        [
        html.Button("Download last 100 days data in CSV", id="btn-csv"),
        dcc.Download(id="download-csv"),
        ],
        style={'font-size': '12px', 'width': '300px', 'height':'50px'}
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
            return {'data': [], 'layout': {'title': 'Custom timeframe selected'}}
        else:
            dates, values, dates_weather, temp = fetch_data(start_date, end_date)
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            fig.add_scatter(x=dates, y=values, mode='lines', name='Mass', fill='tozeroy',secondary_y=True)
            fig.add_scatter(x=dates_weather, y=temp, mode='lines', name='Temperature',secondary_y=False)
            # Set axes titles
            fig.update_yaxes(title_text="Hive mass", secondary_y=True)
            fig.update_yaxes(title_text="Temperature", secondary_y=False)
            # Set axis ranges
            fig.update_yaxes(range=[30,50], secondary_y=True) # For the scale range
            fig.update_yaxes(range=[0,40], secondary_y=False) # For the temperature range
            return fig
    else:
        dates, values, dates_weather, temp = fetch_data('last_5_values', 'today')
        #values = [x / 9000 for x in values] ##### ONLY FOR TESTING
        # Create figure with secondary y-axis
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_scatter(x=dates, y=values, mode='lines', name='Mass', fill='tozeroy',secondary_y=True)
        fig.add_scatter(x=dates_weather, y=temp, mode='lines', name='Temperature',secondary_y=False)
        # Set axes titles
        fig.update_yaxes(title_text="Hive mass", secondary_y=True)
        fig.update_yaxes(title_text="Temperature", secondary_y=False)
        # Set axis ranges
        fig.update_xaxes(range=[datetime.now() - timedelta(days=5), datetime.now() + timedelta(hours=2)])
        fig.update_yaxes(range=[30,50], secondary_y=True) # For the scale range
        fig.update_yaxes(range=[0,40], secondary_y=False) # For the temperature range
        return fig

# Callback to generate CSV file content (modify data fetching as needed)
@app.callback(
  Output("download-csv", "data"),  # Changed Output target
  [Input('btn-csv', 'n_clicks')],
  prevent_initial_call=True
)

def func(n_clicks):
    dates, values, dates_weather, temp = fetch_data((datetime.now() - timedelta(days=100)).strftime('%Y-%m-%d'), datetime.now().strftime('%Y-%m-%d'))
    df = pd.DataFrame({'Dates':dates,'Mass': values})  # Adjust data as needed
    return dcc.send_data_frame(df.to_csv, "mydf.csv", index = False)

# Your existing callback functions

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
