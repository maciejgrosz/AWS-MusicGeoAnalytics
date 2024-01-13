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

const getAllData = async () => {
    const scanParams = {
      TableName: 'CityGenres',
    };
  
    try {
      const result = await dynamodb.scan(scanParams).promise();
      return result.Items;
    } catch (error) {
      console.error('Error fetching all records from DynamoDB:', error);
      throw new Error('Error fetching all records');
    }
  };
  
// Main Lambda handler
exports.handler = async (event) => {
    try {
      const pathParam = event.pathParameters && event.pathParameters.city;
  
      if (pathParam === "all-data") {
        // Fetch and return all data from the database
        const allData = await getAllData();
        return {
          statusCode: 200,
          headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
          },
          body: JSON.stringify(allData)
        };
      } else {
        // Existing code to handle individual city data
        const city = pathParam;
        const records = await getGenresByCity(city);
        const topGenres = records && records.length > 0 ? getTopGenres(records[0].genres) : [];
  
        return {
          statusCode: 200,
          headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
          },
          body: JSON.stringify(topGenres)
        };
      }
    } catch (error) {
      console.error('Error:', error);
      return {
        statusCode: 500,
        body: JSON.stringify({ message: 'Error processing request' })
      };
    }
  };