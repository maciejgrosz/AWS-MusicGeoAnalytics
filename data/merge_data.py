import json

# Load the first JSON file (saved likes)
with open('saved_likes_PL_small-converted.json', 'r', encoding='utf-8') as json_file:
    saved_likes_data = json.load(json_file)

# Load the second JSON file (user information)
with open('saved_users_PL-converted.json', 'r', encoding='utf-8') as json_file:
    user_info_data = json.load(json_file)

# Iterate through the saved likes data
for username, saved_likes in saved_likes_data.items():
    user_info = None

    # Find the user info in the second JSON by matching the permalink
    for city_data in user_info_data['PL']['Mazowsze']['warsaw']:
        if username in city_data['permalink']:
            user_info = city_data
            break

    # If user info found, add saved likes to it
    if user_info:
        user_info['savedLikes'] = saved_likes

# Save the merged JSON to a new file
with open('merged_data.json', 'w', encoding='utf-8') as json_file:
    json.dump(user_info_data, json_file, ensure_ascii=False, indent=4)

print("Merged JSON saved to 'merged_data.json'.")
