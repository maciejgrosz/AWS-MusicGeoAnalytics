import json

# Load your JSON data
with open('saved_users_PL-converted.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# Count records with "likeCount" below 10
count_below_10 = 0

def count_records(data):
    global count_below_10
    if isinstance(data, list):
        for item in data:
            count_records(item)
    elif isinstance(data, dict):
        if "likeCount" in data and isinstance(data["likeCount"], int) and data["likeCount"] == 0:
            count_below_10 += 1
        for key, value in data.items():
            count_records(value)

count_records(data)

print(f"Number of records with 'likeCount' below 10: {count_below_10}")
