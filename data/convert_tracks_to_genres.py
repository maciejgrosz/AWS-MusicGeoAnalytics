import json

# Load the JSON data
with open('all_users.json', 'r', encoding='utf-8') as json_file:
    users = json.load(json_file)

# Function to count genres for a single user, ignoring case
def count_genres(saved_likes):
    genre_counts = {}
    for like in saved_likes:
        genre = like.get('genre')
        if genre:  # Check if genre is not empty
            genre = genre.lower()  # Convert genre to lowercase
            genre_counts[genre] = genre_counts.get(genre, 0) + 1
    return genre_counts

# Transform each user record
for user in users:
    user['genres'] = count_genres(user.get('savedLikes', []))
    user.pop('savedLikes', None)  # Remove the savedLikes field

# Save the transformed data to a new file
with open('transformed_users.json', 'w', encoding='utf-8') as json_file:
    json.dump(users, json_file, ensure_ascii=False, indent=4)

print("Transformed data (case insensitive genres) saved to 'transformed_users.json'.")
