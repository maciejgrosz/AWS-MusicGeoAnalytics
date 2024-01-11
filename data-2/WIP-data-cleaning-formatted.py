import json
from unidecode import unidecode

# Function to convert Unicode to ASCII
def convert_unicode_to_ascii(text):
    return unidecode(text)

# Function to recursively convert data
def convert_data(data):
    if isinstance(data, dict):
        return {convert_unicode_to_ascii(key): convert_data(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [convert_data(item) for item in data]
    elif isinstance(data, str):
        return convert_unicode_to_ascii(data)
    else:
        return data

# Function to merge user data with saved likes
def merge_data(users_data, likes_data):
    permalink_dict = {f"https://soundcloud.com/{username}": likes for username, likes in likes_data.items()}
    for region in users_data.values():
        for city in region.values():
            for user in city:
                if 'permalink' in user:
                    permalink = user['permalink']
                    user['savedLikes'] = permalink_dict.get(permalink, [])
    return users_data

# Function to filter users with non-empty 'savedLikes' and count genres
def filter_and_transform(users_data):
    def count_genres(saved_likes):
        genre_counts = {}
        for like in saved_likes:
            genre = like.get('genre', '').lower()
            if genre:
                genre_counts[genre] = genre_counts.get(genre, 0) + 1
        return genre_counts

    all_users = []
    for region in users_data.values():
        for city in region.values():
            for user in city:
                if 'savedLikes' in user and user['savedLikes']:
                    user['genres'] = count_genres(user['savedLikes'])
                    user.pop('savedLikes', None)
                    all_users.append(user)
    return all_users

# Load and process the data
with open('saved_users_GB.json', 'r', encoding='utf-8') as file:
    users_data = json.load(file)
users_data = convert_data(users_data)

with open('saved_likes_GB_small.json', 'r', encoding='utf-8') as file:
    likes_data = json.load(file)
likes_data = convert_data(likes_data)

# Merge, filter, and transform data
merged_data = merge_data(users_data, likes_data)
transformed_users = filter_and_transform(merged_data)

# Save the final transformed data
with open('transformed_users_GB.json', 'w', encoding='utf-8') as file:
    json.dump(transformed_users, file, ensure_ascii=False, indent=4)

print("Transformed data saved to 'transformed_users_GB.json'.")
