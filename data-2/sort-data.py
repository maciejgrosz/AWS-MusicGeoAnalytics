import json

def sort_genres_in_file(input_file_path, output_file_path):
    try:
        # Read JSON data from the input file
        with open(input_file_path, 'r') as file:
            data = json.load(file)

        # Sort the genres for each city
        sorted_data = {city: dict(sorted(genres.items(), key=lambda item: item[1], reverse=True))
                       for city, genres in data.items()}

        # Write the sorted data to the output file
        with open(output_file_path, 'w') as file:
            json.dump(sorted_data, file, indent=4)

        print(f"Data sorted successfully. Check the output file: {output_file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
input_file_path = 'data_sorted_mapped.json'  # Replace with the path to your JSON file
output_file_path = 'just-for-test.json'  # Replace with the desired output path

sort_genres_in_file(input_file_path, output_file_path)

