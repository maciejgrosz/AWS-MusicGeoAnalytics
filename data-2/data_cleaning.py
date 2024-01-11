import json
from unidecode import unidecode

data_files = ["saved_users_GB", "saved_likes_GB_small"]
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
    with open(f'{data_file}-converted-test.json', 'w', encoding='utf-8') as json_file:
        json.dump(converted_data, json_file, ensure_ascii=False, indent=4)

    print("Conversion completed. The data is saved in 'converted_data.json'.")

#saved_users_PL-converted-test.json



# Load the original users data
with open(f'{data_files[0]}-converted-test.json', 'r') as file:
    users_data = json.load(file)

# Load the additional data
with open(f'{data_files[1]}-converted-test.json', 'r') as file:
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
with open('merged_data-test.json', 'w') as file:
    json.dump(users_data, file, indent=4)

print("Merging complete. Merged data saved in 'merged_data.json'.")

# ------- #

# Load the JSON data
with open('merged_data-test.json', 'r', encoding='utf-8') as json_file:
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
with open('clean-data-test.json', 'w', encoding='utf-8') as json_file:
    json.dump(user_info_data, json_file, ensure_ascii=False, indent=4)

print("Cleaned data saved to 'clean-data.json'.")

import json

# Load the JSON data
with open('clean-data-test.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# Create an empty list to store all user records
all_users = []

# Iterate through each country, region, and city to extract user records
for country, regions in data.items():
    for region, cities in regions.items():
        for city, users in cities.items():
            all_users.extend(users)

# Save the list of all users to a new file
with open('all_users-test.json', 'w', encoding='utf-8') as json_file:
    json.dump(all_users, json_file, ensure_ascii=False, indent=4)

print("All user data has been extracted to 'all_users.json'.")


# Load the JSON data
with open('all_users-test.json', 'r', encoding='utf-8') as json_file:
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
with open('transformed_users_GB.json', 'w', encoding='utf-8') as json_file:
    json.dump(users, json_file, ensure_ascii=False, indent=4)

print("Transformed data (case insensitive genres) saved to 'transformed_users-test.json'.")