import requests
#  Imports the KMeans clustering algorithm from the sklearn library, used to group attractions based on similarity.
from sklearn.cluster import KMeans
# Imports the pandas library, useful for data manipulation, especially with data tables.
import pandas as pd
# Imports datetime and timedelta classes from the datetime module. These are used to handle dates and date calculations.
from datetime import datetime, timedelta

api_key='AIzaSyCVvS3wpd8Lm1tm7NyTsIBMF-DWqTZIWN8'

# Define the function to get travel time
def get_travel_time(origin_place_id, destination_place_id, api_key):
    url = f"https://maps.googleapis.com/maps/api/distancematrix/json"
    params = {
        'origins': f'place_id:{origin_place_id}',
        'destinations': f'place_id:{destination_place_id}',
        'key': api_key,
        'mode': 'driving'  # Set to driving, walking, etc. as needed
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    # Return travel time if available
    if data['rows'][0]['elements'][0]['status'] == 'OK':
        return data['rows'][0]['elements'][0]['duration']['text']
    return "Unavailable"

def generate_itinerary(city, user_budget, min_rating, start_date, end_date):
    # Calculate the number of days in the trip
    trip_days = (datetime.strptime(end_date, '%Y-%m-%d') - datetime.strptime(start_date, '%Y-%m-%d')).days + 1

    # Loads datasets for attractions, hotels, and restaurants using pandas and stores them as dataframes.
    attractions_df = pd.read_csv(r'C:\Itinerary\backend\dataset\filtered_tourist_data copy.csv')
    hotels_df = pd.read_csv(r'C:\Itinerary\backend\dataset\filtered_hotels_temp.csv')
    restaurants_df = pd.read_csv(r'C:\Itinerary\backend\dataset\filtered_restaurants copy.csv')

    # Filters the datasets to include only entries for the specified city.
    city_attractions = attractions_df[attractions_df['City'].str.lower() == city.lower()]
    city_hotels = hotels_df[hotels_df['City'].str.lower() == city.lower()]
    city_restaurants = restaurants_df[restaurants_df['City'].str.lower() == city.lower()]

    # Applies budget and rating filters to recommend hotels and restaurants that fit within the user's criteria.
    recommended_hotels = city_hotels[(city_hotels['Hotel_Price'] <= user_budget) & (city_hotels['Hotel_Rating'] >= min_rating)]
    recommended_restaurants = city_restaurants[(city_restaurants['Cost'] <= user_budget) & (city_restaurants['Rating'] >= min_rating)]

    # Randomly selects a single hotel from the filtered list if available; otherwise, sets chosen_hotel to None.
    chosen_hotel = recommended_hotels.sample(1).iloc[0] if not recommended_hotels.empty else None

    # Encodes the Type column as numeric values and uses it along with ratings to create clusters of attractions, with a maximum of 5 clusters. Each attraction is assigned to a cluster.
    city_attractions['Type'] = city_attractions['Type'].astype('category').cat.codes
    X = city_attractions[['Type', 'Google review rating']] 
    kmeans = KMeans(n_clusters=min(5, len(city_attractions)), random_state=42)
    city_attractions['Cluster'] = kmeans.fit_predict(X)

    # Retrieves the unique cluster identifiers and groups attractions by these clusters.
    clusters = city_attractions['Cluster'].unique()
    attractions_by_cluster = city_attractions.groupby('Cluster')

    # Initializes an empty dictionary, itinerary, and begins looping over the trip days.
    itinerary = {}
        # Update the itinerary generation loop
    for day in range(trip_days):
        day_date = datetime.strptime(start_date, '%Y-%m-%d') + timedelta(days=day)
        cluster_id = clusters[day % len(clusters)]
        day_attractions = attractions_by_cluster.get_group(cluster_id)

        lunch_restaurant = recommended_restaurants.sample(1) if not recommended_restaurants.empty else None
        dinner_restaurant = recommended_restaurants.sample(1) if not recommended_restaurants.empty else None

        itinerary[day_date.strftime('%Y-%m-%d')] = {
            'Hotel': {
                'Name': chosen_hotel['Hotel_Name'] if chosen_hotel is not None else "No hotel available",
                'Place_ID': chosen_hotel['Place_ID'] if chosen_hotel is not None else None,
                'Photo_Reference': chosen_hotel['Photo_Reference'] if chosen_hotel is not None else None
            },
            'Lunch Restaurant': {
                'Name': lunch_restaurant['Name'].values[0] if lunch_restaurant is not None else "No available restaurant",
                'Place_ID': lunch_restaurant['Place_ID'].values[0] if lunch_restaurant is not None else None,
                'Photo_Reference': lunch_restaurant['Photo_Reference'].values[0] if lunch_restaurant is not None else None,
                'Travel_Time': get_travel_time(chosen_hotel['Place_ID'], lunch_restaurant['Place_ID'].values[0], api_key) if lunch_restaurant is not None and chosen_hotel is not None else "Unavailable"
            },
            'Dinner Restaurant': {
                'Name': dinner_restaurant['Name'].values[0] if dinner_restaurant is not None else "No available restaurant",
                'Place_ID': dinner_restaurant['Place_ID'].values[0] if dinner_restaurant is not None else None,
                'Photo_Reference': dinner_restaurant['Photo_Reference'].values[0] if dinner_restaurant is not None else None,
                'Travel_Time': get_travel_time(chosen_hotel['Place_ID'], dinner_restaurant['Place_ID'].values[0], api_key) if dinner_restaurant is not None and chosen_hotel is not None else "Unavailable"
            },
            'Attractions': [
                {
                    'Name': attraction['Name'],
                    'Place_ID': attraction['Place_ID'],
                    'Photo_Reference': attraction['Photo_Reference'],
                    'Travel_Time': get_travel_time(chosen_hotel['Place_ID'], attraction['Place_ID'], api_key) if chosen_hotel is not None else "Unavailable"
                }
                for _, attraction in day_attractions.iterrows()
            ]
        }

    return itinerary
