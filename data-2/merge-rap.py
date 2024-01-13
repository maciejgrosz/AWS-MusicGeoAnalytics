import json

# Load data from the JSON file
with open("data_sorted_mapped.json", "r") as json_file:
    data = json.load(json_file)

# Iterate through the data and merge "rap" and "hip-hop" genres
for city, genres in data.items():
    if "rap" in genres and "hip-hop" in genres:
        merged_value = genres["rap"] + genres["hip-hop"]
        genres["rap/hip-hop"] = merged_value
        del genres["rap"]
        del genres["hip-hop"]

# Save the updated data back to the JSON file
with open("updated_data.json", "w") as json_file:
    json.dump(data, json_file, indent=4)

print("Data has been merged and saved to 'updated_data.json'.")
