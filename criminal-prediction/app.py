import pandas as pd 
import numpy as np
import requests
import streamlit as st

data = pd.read_csv("final.csv")

data['Lat'] = 0
data['Lon'] = 0


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
        print("No results found for the location.")
        return None



df = pd.DataFrame(data)

# Group by crime and criminal, and count occurrences
crime_counts = df.groupby(['crime group', 'name']).size().reset_index(name='Count')

# Find the criminal with the maximum count for each crime
max_criminals = crime_counts.loc[crime_counts.groupby('crime group')['Count'].idxmax()]

# Extract the columns for the final DataFrame
result_df = max_criminals[['crime group', 'name']]

# print(result_df)



for i in range(len(data)):
  # data['Lat'][i], data['Lon'][i] = get_coordinates(data['location'][i])
  temp = data['locations new'][i]
  lat, lon = temp.split(", ")
  data['Lat'][i], data['Lon'][i] = float(lat), float(lon)


print(data.head(5))


df = pd.DataFrame(data)

# Group by criminal and calculate mean latitude and longitude
df['time'] = pd.to_datetime(df['time'])

# mean_location = df.groupby('name').agg({'Lat': 'mean', 'Lon': 'mean'}).reset_index()
# mean_location = df.groupby('name').agg({'Lat': 'mean', 'Lon': 'mean'}).reset_index()

mean_location = df.groupby('name').agg({'Lat': 'mean', 'Lon': 'mean', 'time': 'mean'}).reset_index()

mean_location['Mean time'] = mean_location['time'].dt.strftime('%H:%M')

# Drop the original 'Time' column as it's no longer needed
mean_location.drop('time', axis=1, inplace=True)

# Rename columns for clarity
mean_location.columns = ['name', 'Mean Latitude', 'Mean Longitude', 'Mean Time']

print(mean_location)
# Rename columns for clarity
# mean_location.columns = ['name', 'Mean Latitude', 'Mean Longitude']

# print(mean_location


from geopy.distance import geodesic

def dist(lat1,lon1,lat2,lon2):

  # Calculate distance using geodesic
  distance = geodesic((lat1, lon1), (lat2, lon2)).kilometers
  return distance




# print(data['crime group'].unique())

# Define the crime group options
crime_groups = ['ROBBERY', 'CYBERCRIME', 'MURDER', 'KIDNAPPING AND ABDUCTION', 'MOLESTATION', 'POCSO', 'CRPC', 'THEFT', 'ARSON', 'RAPE']

try:
    crime = st.selectbox("Select crime group", crime_groups).upper()  # Use lowercase for consistency
    location = st.text_input("Enter location of crime: ")
    time = st.text_input("Enter the time of the crime ")
except:
    pass


# st.write(crime, location, time)
print(crime, location, time)

result_df = result_df.reset_index()
result_df = result_df.drop(columns = ['index'])

try:
    lat1, lon1 = get_coordinates(location)
    dist1 = np.zeros(len(mean_location))
    for i in range(len(mean_location)):
      lat2, lon2 = mean_location['Mean Latitude'][i], mean_location['Mean Longitude'][i]
      dist1[i] = dist(lat1,lon1,lat2,lon2)
except:
    pass




import pandas as pd

input_time_str = time
input_time = pd.to_datetime(input_time_str)

mean_location['Time Difference'] = abs(pd.to_datetime(mean_location['Mean Time']) - input_time)

nearest_names = mean_location.sort_values(by='Time Difference')['name'].head(5).reset_index(drop=True)

if not nearest_names.empty:
    rank = pd.Series(range(1, len(nearest_names) + 1))
    nearest_names_with_rank = pd.DataFrame({'Rank': rank, 'Name': nearest_names})
    
    # Highlighting the top name
    nearest_names_with_rank['Name'] = nearest_names_with_rank.apply(
        lambda row: f'<span style="color: {"red" if row["Rank"] == 1 else "white"};">{row["Name"]}</span>',
        axis=1
    )
    
    st.write("Most Probable Name according to time:")
    st.write(nearest_names_with_rank.loc[0, 'Name'], unsafe_allow_html=True)  # Display the most probable name
    
    st.write("The 5 names with the nearest mean time are:")
    
    # Convert DataFrame to HTML for styling
    nearest_names_html = nearest_names_with_rank.to_html(escape=False, index=False)
    
    # Display HTML in Streamlit
    st.write(nearest_names_html, unsafe_allow_html=True)
else:
    st.write("No names found in the DataFrame.")






try:
    idx = np.where(dist1 == min(dist1))[0]
    st.write("Criminal according to distance: ",mean_location['name'][idx])
    print(mean_location['name'][idx])
    idx2 = np.where(result_df['crime group'] == crime)[0]
    st.write("Criminal according to crime: ",result_df['name'][idx2])
    print(result_df['name'][idx2])
except:
    pass

