import json

# Load the JSON data
with open('merged_data.json', 'r', encoding='utf-8') as json_file:
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
with open('clean-data.json', 'w', encoding='utf-8') as json_file:
    json.dump(user_info_data, json_file, ensure_ascii=False, indent=4)

print("Cleaned data saved to 'clean-data.json'.")
