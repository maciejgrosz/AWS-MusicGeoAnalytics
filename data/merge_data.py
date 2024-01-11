import json

# Load the original users data
with open('saved_users_PL-converted.json', 'r') as file:
    users_data = json.load(file)

# Load the additional data
with open('saved_likes_PL_small-converted.json', 'r') as file:
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
with open('merged_data.json', 'w') as file:
    json.dump(users_data, file, indent=4)

print("Merging complete. Merged data saved in 'merged_data.json'.")