import json
from unidecode import unidecode

data_file = "saved_users_GB"
# Load your JSON data
with open(f'{data_file}.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# Define a function to convert Unicode to ASCII
def convert_unicode_to_ascii(text):
    return unidecode(text)

# Iterate through your data and convert Unicode to ASCII
def convert_data(data):
    if isinstance(data, dict):
        for key, value in data.items():
            data[key] = convert_data(value)
        return data
    elif isinstance(data, list):   
        return [convert_data(item) for item in data]
    elif isinstance(data, str):
        return convert_unicode_to_ascii(data)
    else:
        return data

# Convert the data
converted_data = convert_data(data)

# Save the converted data back to a JSON file
with open(f'{data_file}-converted.json', 'w', encoding='utf-8') as json_file:
    json.dump(converted_data, json_file, ensure_ascii=False, indent=4)

print("Conversion completed. The data is saved in 'converted_data.json'.")