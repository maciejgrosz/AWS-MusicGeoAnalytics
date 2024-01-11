import json

# Load the JSON data
with open('clean-data.json', 'r', encoding='utf-8') as json_file:
    user_info_data = json.load(json_file)

# Initialize a counter for users with "savedLikes" field
users_with_saved_likes = 0

# Iterate through the user information data
for city_data in user_info_data['PL']['Mazowsze']['warsaw']:
    if 'savedLikes' in city_data:
        users_with_saved_likes += 1

print(f"Number of users with 'savedLikes' field: {users_with_saved_likes}")
