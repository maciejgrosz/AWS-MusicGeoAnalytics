import json

# Load the JSON data from the file
with open('all_users.json', 'r', encoding='utf-8') as json_file:
    users = json.load(json_file)

# Calculate the number of users
number_of_users = len(users)

print(f"Total number of users: {number_of_users}")
