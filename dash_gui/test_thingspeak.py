"""

import requests

# ThingSpeak read API endpoint
url = 'https://api.thingspeak.com/channels/{}/feeds/last.json'.format('2448118')
# Replace 'CHANNEL_ID' with your ThingSpeak channel ID

# Your ThingSpeak read API key
api_key = 'IXT4T5APCGA3QSMF'

# Query parameters for the API request
params = {'api_key': api_key}

try:
    # Send GET request to ThingSpeak API
    response = requests.get(url, params=params)
    
    # Check if request was successful (status code 200)
    if response.status_code == 200:
        # Extract data from response
        data = response.json()
        
        # Accessing the field of interest (assuming you have only one field)
        field_value = data['field1']
        
        print("Value of the field:", field_value)
    else:
        print("Failed to fetch data from ThingSpeak. Status code:", response.status_code)

except Exception as e:
    print("An error occurred:", e)
    
    """
    


import requests

# ThingSpeak read API endpoint for the last 5 entries
url = 'https://api.thingspeak.com/channels/{}/feeds.json'.format('2448118')
# Replace 'CHANNEL_ID' with your ThingSpeak channel ID

# Your ThingSpeak read API key
api_key = 'IXT4T5APCGA3QSMF'

# Query parameters for the API request
params = {'api_key': api_key, 'results': 5}  # Fetch the last 5 entries

try:
    # Send GET request to ThingSpeak API
    response = requests.get(url, params=params)
    
    # Check if request was successful (status code 200)
    if response.status_code == 200:
        # Extract data from response
        data = response.json()
        
        # Iterate through each entry
        for entry in data['feeds']:
            # Accessing the field of interest (assuming you have only one field)
            field_value = entry['field1']
            print("Value of the field:", field_value)
    else:
        print("Failed to fetch data from ThingSpeak. Status code:", response.status_code)

except Exception as e:
    print("An error occurred:", e)

