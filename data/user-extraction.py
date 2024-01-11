import json

# Load the JSON data
with open('clean-data.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# Create an empty list to store all user records
all_users = []

# Iterate through each country, region, and city to extract user records
for country, regions in data.items():
    for region, cities in regions.items():
        for city, users in cities.items():
            all_users.extend(users)

# Save the list of all users to a new file
with open('all_users.json', 'w', encoding='utf-8') as json_file:
    json.dump(all_users, json_file, ensure_ascii=False, indent=4)

print("All user data has been extracted to 'all_users.json'.")