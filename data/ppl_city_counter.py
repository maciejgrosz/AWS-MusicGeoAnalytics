import json

# Load the JSON data
with open('all_users.json', 'r', encoding='utf-8') as json_file:
    users = json.load(json_file)

# Initialize an empty dictionary to store city counts
city_counts = {}

# Iterate through each user and count the occurrences of each city (ignoring case)
for user in users:
    city = user.get('city', 'Unknown').lower()  # Convert city to lowercase
    city_counts[city] = city_counts.get(city, 0) + 1

# Print the city counts
for city, count in city_counts.items():
    print(f"{city.capitalize()}: {count}")  # Capitalize the city name for display

# Optionally, save the city counts to a file
with open('city_counts_case_insensitive.json', 'w', encoding='utf-8') as json_file:
    json.dump(city_counts, json_file, ensure_ascii=False, indent=4)

print("City counts (case insensitive) saved to 'city_counts_case_insensitive.json'.")
#saved_users_PL-test.json

