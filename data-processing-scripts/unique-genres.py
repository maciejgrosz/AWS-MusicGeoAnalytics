import json

# Load the JSON data
with open('final_data_PL.json', 'r', encoding='utf-8') as json_file:
    user_info_data = json.load(json_file)

# Create a set to store unique genres
unique_genres = set()

# Iterate through the user information data and extract genres
for user_data in user_info_data:
    if 'genres' in user_data:
        for genre in user_data['genres']:
            unique_genres.add(genre)

# Sort the unique genres alphabetically
sorted_genres = sorted(unique_genres)

# Save the sorted genres to a file
with open('unique_genres.txt', 'w', encoding='utf-8') as output_file:
    for genre in sorted_genres:
        output_file.write(genre + '\n')

print("Unique genres saved to 'unique_genres.txt'.")
