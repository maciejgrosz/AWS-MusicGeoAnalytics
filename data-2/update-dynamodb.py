import json
import boto3

# Set up a session with the sandbox profile
session = boto3.Session(profile_name='sandbox')

# Initialize a DynamoDB client using the specified session
dynamodb = session.resource('dynamodb', region_name='eu-west-1')
table = dynamodb.Table('Users')

# Load the JSON data
with open('final_data_PL.json', 'r', encoding='utf-8') as file:
    users_data = json.load(file)

# Function to upload a batch of items
def batch_write(items):
    with table.batch_writer() as batch:
        for item in items:
            batch.put_item(Item=item)

# Process the data in batches of 25 items
batch_size = 25
for i in range(0, len(users_data), batch_size):
    batch = users_data[i:i + batch_size]
    batch_write(batch)

print("Data upload completed.")
