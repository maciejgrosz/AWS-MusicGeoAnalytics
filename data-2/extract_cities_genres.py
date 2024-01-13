import json
from collections import defaultdict

# Load the original JSON data
with open('final_data_GB.json', 'r', encoding='utf-8') as file:
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
with open('data_sorted_GB.json', 'w', encoding='utf-8') as file:
    json.dump(city_genres_sorted, file, ensure_ascii=False, indent=4)

print("Transformed data (sorted by user count per genre) saved to 'data_sorted.json'.")
