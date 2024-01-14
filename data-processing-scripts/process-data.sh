#!/bin/bash

# deploy-data.sh

# Check if two arguments are passed
if [ "$#" -ne 2 ]; then
    echo "Usage: bash deploy-data.sh <path_to_saved_likes> <path_to_saved_users>"
    exit 1
fi

# Assign arguments to variables
SAVED_LIKES_SRC=$1
SAVED_USERS_SRC=$2

# Destination paths
SAVED_LIKES_DEST="./saved_likes.json"
SAVED_USERS_DEST="./saved_users.json"

# Copy the files to the destinations
cp "$SAVED_LIKES_SRC" "$SAVED_LIKES_DEST"
cp "$SAVED_USERS_SRC" "$SAVED_USERS_DEST"

echo "Files copied successfully."

# Running the data_cleaning.py script
echo "Running data cleaning script..."
python3 data_cleaning.py

echo "Running map genres script..."
python3 map_genres.py

mv fully-processed-data.json ../processed-data/processed-data.json
# Removing files matching pattern test-*.json
echo "Removing test files..."
rm -rf *.json
