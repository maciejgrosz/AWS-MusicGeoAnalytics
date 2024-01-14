import json
from unidecode import unidecode
import sys
from collections import defaultdict


data_files = ["saved_users", "saved_likes"]
for data_file in data_files:
    # Load your JSON data
    with open(f'{data_file}.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    # Define a function to convert Unicode to ASCII
    def convert_unicode_to_ascii(text):
        return unidecode(text)

    # Iterate through your data and convert Unicode to ASCII
    def convert_data(data):
        if isinstance(data, dict):
            for key, value in data.items():
                data[key] = convert_data(value)
            return data
        elif isinstance(data, list):   
            return [convert_data(item) for item in data]
        elif isinstance(data, str):
            return convert_unicode_to_ascii(data)
        else:
            return data

    # Convert the data
    converted_data = convert_data(data)

    # Save the converted data back to a JSON file
    with open(f'test-{data_file}.json', 'w', encoding='utf-8') as json_file:
        json.dump(converted_data, json_file, ensure_ascii=False, indent=4)


# Load the original users data
with open(f'test-{data_files[0]}.json', 'r') as file:
    users_data = json.load(file)

# Load the additional data
with open(f'test-{data_files[1]}.json', 'r') as file:
    additional_data = json.load(file)

# Function to find a user by permalink in the users data
def find_user(permalink, data):
    for country, regions in data.items():
        for region, cities in regions.items():
            for city, users in cities.items():
                for user in users:
                    if user['permalink'] == permalink:
                        return user
    return None

# Iterate over the additional data and update the users data
for username, saved_likes in additional_data.items():
    permalink = f"https://soundcloud.com/{username}"
    user = find_user(permalink, users_data)
    if user is not None:
        user['savedLikes'] = saved_likes

# Save the merged data to a new file
with open('test-merged_data.json', 'w') as file:
    json.dump(users_data, file, indent=4)

# ------- #

# Load the JSON data
with open('test-merged_data.json', 'r', encoding='utf-8') as json_file:
    user_info_data = json.load(json_file)

# Function to filter users with non-empty 'savedLikes'
def filter_users(city_users):
    return [user for user in city_users if 'savedLikes' in user and user['savedLikes']]

# Iterate through the entire data structure and apply the filter
for country, regions in user_info_data.items():
    for region, cities in regions.items():
        for city, users in cities.items():
            user_info_data[country][region][city] = filter_users(users)

# Save the cleaned JSON data to 'clean-data.json'
with open('test-clean-data.json', 'w', encoding='utf-8') as json_file:
    json.dump(user_info_data, json_file, ensure_ascii=False, indent=4)


# Load the JSON data
with open('test-clean-data.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# Create an empty list to store all user records
all_users = []

# Iterate through each country, region, and city to extract user records
for country, regions in data.items():
    for region, cities in regions.items():
        for city, users in cities.items():
            all_users.extend(users)

# Save the list of all users to a new file
with open('test-all_users.json', 'w', encoding='utf-8') as json_file:
    json.dump(all_users, json_file, ensure_ascii=False, indent=4)


# Load the JSON data
with open('test-all_users.json', 'r', encoding='utf-8') as json_file:
    users = json.load(json_file)

# Function to count genres for a single user, ignoring case
def count_genres(saved_likes):
    genre_counts = {}
    for like in saved_likes:
        genre = like.get('genre')
        if genre:  # Check if genre is not empty
            genre = genre.lower()  # Convert genre to lowercase
            genre_counts[genre] = genre_counts.get(genre, 0) + 1
    return genre_counts

# Transform each user record
for user in users:
    user['genres'] = count_genres(user.get('savedLikes', []))
    user.pop('savedLikes', None)  # Remove the savedLikes field

# Save the transformed data to a new file
with open('test-transformed_data.json', 'w', encoding='utf-8') as json_file:
    json.dump(users, json_file, ensure_ascii=False, indent=4)


# Load the JSON data
with open('test-transformed_data.json', 'r', encoding='utf-8') as json_file:
    users = json.load(json_file)

# Convert city names to lowercase
for user in users:
    if 'city' in user:
        user['city'] = user['city'].lower()

# Save the updated data to a new file
with open('test-final_data.json', 'w', encoding='utf-8') as json_file:
    json.dump(users, json_file, ensure_ascii=False, indent=4)

# Load the original JSON data
with open('test-final_data.json', 'r', encoding='utf-8') as file:
    users_data = json.load(file)

# Initialize a dictionary to store the count of users per genre for each city
city_genres = defaultdict(lambda: defaultdict(int))

# Process each user record and aggregate the genres
for user in users_data:
    city = user.get('city', '').lower()  # Normalize city names to lowercase
    unique_genres = set(user.get('genres', {}).keys())  # Get unique genres for the user
    for genre in unique_genres:
        city_genres[city][genre] += 1  # Count each genre once per user

# Sort genres within each city by count and convert to regular dict
city_genres_sorted = {}
for city, genres in city_genres.items():
    sorted_genres = sorted(genres.items(), key=lambda x: x[1], reverse=True)
    city_genres_sorted[city] = {genre: count for genre, count in sorted_genres}

# Save the transformed data to a new JSON file
with open('test-extracted-data.json', 'w', encoding='utf-8') as file:
    json.dump(city_genres_sorted, file, ensure_ascii=False, indent=4)
