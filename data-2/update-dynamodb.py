import json
import boto3

# Initialize a DynamoDB client with the 'sandbox' profile
session = boto3.Session(profile_name='sandbox')
dynamodb = session.resource('dynamodb')

# Specify the DynamoDB table name
table_name = 'CityGenres'
table = dynamodb.Table(table_name)

# Load the JSON data from the file
file_name = 'data_sorted-pl-uploaded.json'
with open(file_name, 'r', encoding='utf-8') as file:
    city_genres_data = json.load(file)

# Function to upload data to DynamoDB
def upload_to_dynamodb(city, genres):
    try:
        response = table.put_item(
            Item={
                'city': city,
                'genres': genres
            }
        )
        return response
    except Exception as e:
        print(f"Error uploading {city}: {str(e)}")
        return None

# Upload each city's data to DynamoDB
for city, genres in city_genres_data.items():
    result = upload_to_dynamodb(city, genres)
    if result:
        print(f"Uploaded data for city: {city}")

print("Data upload process completed.")
