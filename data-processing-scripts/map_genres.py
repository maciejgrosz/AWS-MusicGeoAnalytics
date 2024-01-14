import json
import re 

genre_types = [
    "pop", "rock", "hip-hop", "jazz", "blues", "country", "rnb",
    "electronic", "classical", "folk", "reggae", "punk", "metal", "indie", "soul",
    "funk", "gospel", "alternative", "rap", "edm", "ska",
    "ambient", "dubstep", "techno", "house", "trap", "latin", "disco", 
    "grunge", "book", "podcast", "trance", "dance", "boogie", "beats", "afrobeat", "phonk"
]
jazz_genres = [
    "dixie",
    "swing",
    "bebop",
    "free",
    "fusion",
    "gypsy",
    "ragtime"
    
]

def read_music_genres(file_path):
    try:
        with open(file_path, 'r') as file:
            genres = [line.strip() for line in file.readlines()]
        return genres
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []
    
file_path = 'unique_genres.txt'
music_genres = read_music_genres(file_path)

def clean_genre(genre):
    genre = genre.replace('r&b', 'rnb')
    for j_genre in jazz_genres: 
        genre = genre.replace(j_genre, 'jazz')
    cleaned_genre = ''.join(char if char.isalpha() else ' ' for char in genre)
    cleaned_genre = cleaned_genre.strip() 
    cleaned_genre = re.sub(r'\s+', ' ', cleaned_genre)
    return cleaned_genre

def map_genre(genre, genre_types=genre_types):
    genre = clean_genre(genre)
    genre = genre.split(' ')
    for element in genre: 
        if element in genre_types:
            return element
        elif len(element) >= 3:
            for genre_type in genre_types: 
                if element in genre_type:
                    return genre_type
    for element in genre:
        is_in_how_many = 0
        for genre_type in genre_types:
            if genre_type in element:
                is_in_how_many += 1 
        for genre_type in genre_types:
            if genre_type in element and is_in_how_many == 1:
                return genre_type
    return 'other'   

with open('test-extracted-data.json', 'r') as data_sorted:
    data_sorted = json.load(data_sorted)

def map_data(data):
    data_mapped = {}
    for city in data.keys():
        data_mapped[city] = {}
        for genre_name in data[city].keys():
            genre_num = data[city][genre_name]
            new_name = map_genre(genre_name)
            if new_name in data_mapped[city].keys():
                data_mapped[city][new_name] += genre_num
            else:
                data_mapped[city][new_name] = genre_num
                
    return data_mapped

data_sorted_mapped = map_data(data_sorted)

with open(f"test-mapped-genre.json", "w") as outfile: 
        json.dump(data_sorted_mapped, outfile, indent = 4)

# Load data from the JSON file
with open("test-mapped-genre.json", "r") as json_file:
    data = json.load(json_file)

# Iterate through the data and merge "rap" and "hip-hop" genres
for city, genres in data.items():
    if "rap" in genres and "hip-hop" in genres:
        merged_value = genres["rap"] + genres["hip-hop"]
        genres["rap/hip-hop"] = merged_value
        del genres["rap"]
        del genres["hip-hop"]

# Save the updated data back to the JSON file
with open("fully-processed-data.json", "w") as json_file:
    json.dump(data, json_file, indent=4)

print("Data has been merged and saved to 'Fully-processed-data.json'.")