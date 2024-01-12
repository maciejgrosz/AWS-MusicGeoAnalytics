const AWS = require('aws-sdk');
const s3 = new AWS.S3();
const dynamodb = new AWS.DynamoDB();
const fs = require('fs'); // Node.js file system module

// Function to fetch content from S3
const fetchS3Object = async () => {
  return await s3.getObject({
    Bucket: 'tass-musicgeoanalyser',
    Key: 'index.html',
  }).promise();
};

const getUserById = async (userId) => {
  const getItemParams = {
    TableName: 'Users', // Ensure this matches your actual DynamoDB table name
    Key: {
      'id': userId  // Assuming 'id' is the name of your partition key
    }
  };

  try {
    const itemResult = await dynamodb.get(getItemParams).promise();
    console.log('Item Result:', itemResult);

    if (itemResult.Item && itemResult.Item.name) {
      return itemResult.Item.name; // Returns the user's name
    } else {
      return 'User not found';
    }
  } catch (error) {
    console.error('Error fetching user from DynamoDB:', error);
    return 'Error fetching user';
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

// Main Lambda handler
exports.handler = async (event) => {
  try {
    const s3Object = await fetchS3Object();
    const userId = 6522323;  // Replace with the actual user ID you want to query
    const userName = await getUserById(userId);
    const leafletScriptContent = await readLeafletScript();
    // Replace the placeholder with the random value
    let modifiedHtml = s3Object.Body.toString('utf-8').replace('REPLACE_WITH_NAME', `NAME: ${userName}`);
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

