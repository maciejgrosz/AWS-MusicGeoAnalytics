import json

# Load the JSON data
with open('merged_data.json', 'r', encoding='utf-8') as json_file:
    user_info_data = json.load(json_file)

# Create a new list to store the filtered user data
filtered_users = []

# Iterate through the user information data
for city_data in user_info_data['PL']['Mazowsze']['warsaw']:
    if 'savedLikes' in city_data and city_data['savedLikes']:
        filtered_users.append(city_data)

# Update the user information data with the filtered list
user_info_data['PL']['Mazowsze']['warsaw'] = filtered_users

# Save the cleaned JSON data to 'clean-data.json'
with open('clean-data.json', 'w', encoding='utf-8') as json_file:
    json.dump(user_info_data, json_file, ensure_ascii=False, indent=4)

print("Cleaned data saved to 'clean-data.json'.")