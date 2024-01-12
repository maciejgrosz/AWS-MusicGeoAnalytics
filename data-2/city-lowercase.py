import json

# Load the JSON data
with open('transformed_users_GB.json', 'r', encoding='utf-8') as json_file:
    users = json.load(json_file)

# Convert city names to lowercase
for user in users:
    if 'city' in user:
        user['city'] = user['city'].lower()

# Save the updated data to a new file
with open('final_data_GB.json', 'w', encoding='utf-8') as json_file:
    json.dump(users, json_file, ensure_ascii=False, indent=4)

print("Updated data saved to 'users_data_lowercase_cities.json'.")
