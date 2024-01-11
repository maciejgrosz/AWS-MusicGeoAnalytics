import json

# Load the JSON data
with open('all_users.json', 'r', encoding='utf-8') as json_file:
    users = json.load(json_file)

# Function to count genres for a single user
def count_genres(saved_likes):
    genre_counts = {}
    for like in saved_likes:
        genre = like.get('genre', 'Unknown')
        genre_counts[genre] = genre_counts.get(genre, 0) + 1
    return genre_counts

# List to store the final data
users_top_genres = []

# Process each user
for user in users:
    user_data = {
        'username': user.get('name', 'Unknown'),
        'top_genre': count_genres(user.get('savedLikes', []))
    }
    users_top_genres.append(user_data)

# Save the result to a new JSON file
with open('users_top_genres.json', 'w', encoding='utf-8') as json_file:
    json.dump(users_top_genres, json_file, ensure_ascii=False, indent=4)

print("Data saved to 'users_top_genres.json'.")
