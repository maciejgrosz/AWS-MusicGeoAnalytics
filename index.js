const AWS = require('aws-sdk');
const dynamodb = new AWS.DynamoDB.DocumentClient();

const getGenresByCity = async (city) => {
  const queryParams = {
    TableName: 'CityGenres',
    KeyConditionExpression: 'city = :city',
    ExpressionAttributeValues: {
      ':city': city,
    },
  };

  try {
    const result = await dynamodb.query(queryParams).promise();
    console.log('Query Result:', result);

    if (result.Items) {
      return result.Items; // Returns an array of records for the specified city
    } else {
      return 'No records found for this city';
    }
  } catch (error) {
    console.error('Error fetching records from DynamoDB:', error);
    return 'Error fetching records';
  }
};


// Function to get top 5 genres from the dictionary
const getTopGenres = (genreDict) => {
  let genres = [];
  
  for (const [genre, count] of Object.entries(genreDict)) {
    // Log to check if count is a number
    
    genres.push({ genre: genre, count: count });
  }
  
  // Sort genres by count in descending order
  genres.sort((a, b) => b.count - a.count);

  // Return the top 5 genres
  return genres.slice(0, 5);
};

// Main Lambda handler
exports.handler = async (event) => {
  try {
    // Extract the city from the path parameter
    const city = event.pathParameters.city;
    const records = await getGenresByCity(city);
    // Process the retrieved records as needed
    // For example, you can convert the records to JSON and include them in the response

    const topGenres = records && records.length > 0 ? getTopGenres(records[0].genres) : [];
   
    // Replace the placeholder with the JSON representation of the records
    
    // Include Leaflet script dynamically
    return {
        statusCode: 200,
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(topGenres)
      };
    } catch (error) {
      console.error('Error:', error);
      return {
        statusCode: 500,
        body: JSON.stringify({ message: 'Error processing request' })
      };
    }
  };
