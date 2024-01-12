const AWS = require('aws-sdk');
const s3 = new AWS.S3();
const dynamodb = new AWS.DynamoDB.DocumentClient();
const fs = require('fs'); // Node.js file system module
// Function to fetch content from S3
const fetchS3Object = async () => {
  return await s3.getObject({
    Bucket: 'tass-musicgeoanalyser',
    Key: 'index.html',
  }).promise();
};

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

// Function to read the contents of the Leaflet script file
const readLeafletScript = async () => {
  return fs.promises.readFile('./leaflet.js', 'utf-8');
};

// Function to replace the placeholder with Leaflet script
const replaceLeafletScriptPlaceholder = (html, leafletScriptContent) => {
  const placeholder = 'LEAFLET_SCRIPT';
  return html.replace(placeholder, leafletScriptContent);
};

// Function to get top 5 genres from the dictionary
const getTopGenres = (genreDict) => {
  let genres = [];
  
  for (const [genre, count] of Object.entries(genreDict)) {
    // Log to check if count is a number
    
    genres.push({ genre: genre, count: count });
  }
  console.log("genres:", genres);
  
  // Sort genres by count in descending order
  genres.sort((a, b) => b.count - a.count);

  // Return the top 5 genres
  return genres.slice(0, 5);
};

// Main Lambda handler
exports.handler = async (event) => {
  try {
    const s3Object = await fetchS3Object();
    const city = "warsaw";
    const records = await getGenresByCity(city);
    const leafletScriptContent = await readLeafletScript();
    // Process the retrieved records as needed
    // For example, you can convert the records to JSON and include them in the response

    let cityData = [];
    for (const city in cityCoordinates) {
      const records = await getGenresByCity(city);
      const topGenres = records && records.length > 0 ? getTopGenres(records[0].genres) : [];

      cityData.push({
        city: city,
        coordinates: cityCoordinates[city],
        genres: topGenres
      });
    } 
    // Replace the placeholder with the JSON representation of the records
    let modifiedHtml = s3Object.Body.toString('utf-8').replace('REPLACE_WITH_RECORDS', JSON.stringify(topGenres));
    // Include Leaflet script dynamically
    modifiedHtml = replaceLeafletScriptPlaceholder(modifiedHtml, leafletScriptContent);
    console.log('modifiedHtml: ', modifiedHtml);  
    // Return the modified HTML content with appropriate Content-Type
    const response = {
      statusCode: 200,
      headers: {
        'Content-Type': 'text/html',
      },
      body: modifiedHtml
    };

    return response;
  } catch (error) {
    // Handle errors appropriately
    console.error('Error fetching content from S3 or DynamoDB:', error);
    return {
      statusCode: 500,
      body: error,
    };
  }
};
