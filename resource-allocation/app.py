import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


import pandas as pd

import streamlit as st

if not firebase_admin._apps:
    # Fetch the credential JSON file from your Firebase project settings
    # and upload it to Google Colab, then provide the path here
    cred = credentials.Certificate("%your-certificate%")

    # Initialize the app with the credentials and your database URL

    firebase_admin.initialize_app(cred, {
        'databaseURL': '{%your-database-url}'
    })

# Reference to your Firebase database
ref = db.reference('/')

# Listen for changes in the database in real-time
def on_change(event):
    st.write('Data changed:', event.path, event.data)

ref.listen(on_change)


import requests





def get_coordinates(location):
    """
    Get latitude and longitude of a location using OpenStreetMap Nominatim API
    """
    # URL for OpenStreetMap Nominatim API
    url = f'https://nominatim.openstreetmap.org/search?format=json&q={location}'

    # Send request to the API
    response = requests.get(url)

    # Parse JSON response
    data = response.json()

    # Check if response is not empty
    if data:
        # Extract latitude and longitude from the first result
        lat = float(data[0]['lat'])
        lon = float(data[0]['lon'])
        return lat, lon
    else:
        st.write("No results found for the location.")
        return None





# Example usage
# location = input("Enter Location: ")
# latitude, longitude = get_coordinates(location)
# if latitude and longitude:
#     st.write(f"Latitude: {latitude}, Longitude: {longitude}")
# else:
#     st.write("Failed to retrieve coordinates for the location.")




crimes = pd.DataFrame(columns=['Name', 'Lat', 'Lon', 'Intensity'])

try:
    query = ""

    ct = 0
    while(query != 'N'):
      location = st.text_area("Enter Location: ", key = ct)
      crime = st.text_area("Enter Crime: ", key = ct+1)
      intensity = int(st.text_area("Enter Intensity: ", key = ct+2))
      latitude, longitude = get_coordinates(location)
      data = [{'Name': crime, 'Lat': latitude, 'Lon': longitude, 'Intensity': intensity}]
      query = st.text_area("Enter Y to continue and N to stop: ", key = ct+3)
      crimes = pd.concat([crimes, pd.DataFrame(data)], ignore_index=True)
      ct+=10
except:
    pass

st.write(crimes)


from math import radians, sin, cos, sqrt, atan2

def Distance(lat1, lon1, lat2, lon2):
    R = 6371.0

    lat1, lon1 = radians(lat1), radians(lon1)
    lat2, lon2 = radians(lat2), radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c

    return distance


import pandas as pd

data = {
    'Lat': [18.474568112919428, 18.465001331251234, 18.48232009436988,18.457105482206185, 18.498722228096053],  # Example latitude values
    'Lon': [73.81397796441247, 73.81511758755751, 73.80204748648526, 73.82016652531969,  73.82653007486627],  # Example longitude values
    'Name': ['Station A', 'Station B', 'Station C', 'Station D', 'Station E'],
    'Capacity': [50, 30, 40, 60, 35],
    'Dist': [0,0,0,0,0]# Example capacity values
}

Police = pd.DataFrame(data)
st.write(Police)


import warnings


warnings.filterwarnings("ignore")
sorted_crimes = crimes.sort_values(by='Intensity', ascending=False)
j=0
while j < (len(sorted_crimes)):
  lat1 = sorted_crimes['Lat'].iloc[j]
  lon1 = sorted_crimes['Lon'].iloc[j]
  crime = sorted_crimes['Name'].iloc[j]
  req = sorted_crimes['Intensity'].iloc[j]


  for i in range(len(Police)):
    lat2 = Police['Lat'][i]
    lon2 = Police['Lon'][i]
    Police['Dist'][i] = Distance(lat1,lon1,lat2,lon2)

  sorted_police = Police.sort_values(by='Dist', ascending=True)

  for i in range(len(Police)):
    if(req <= sorted_police['Capacity'].iloc[i]):
      sorted_police['Capacity'].iloc[i] = sorted_police['Capacity'].iloc[i] - req
      st.write("Required Police Station is ", sorted_police['Name'].iloc[i]," for crime ", crime," at a distance ", sorted_police['Dist'].iloc[i])
      break

  j = j+1
