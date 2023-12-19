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

// Function to read the contents of the Leaflet script file
const readLeafletScript = async () => {
  return fs.promises.readFile('./leaflet.js', 'utf-8');
};

// Function to query DynamoDB and get a random value
const getRandomValueFromDynamoDB = async () => {
  const getItemParams = {
    TableName: 'soundcloud-data',
    Key: {
      'Id': { S: 'test' }
    }
  };

  const itemResult = await dynamodb.getItem(getItemParams).promise();
  console.log('itemResult: ', itemResult);

  // Check if the item and attribute exist
  const itemExists = itemResult.Item && itemResult.Item.number;

  // Extract the value if it exists, otherwise set a default value
  const randomValue = itemExists ? itemResult.Item.number.N : 'N/A';

  // Log the randomValue
  console.log('Random Value:', randomValue);

  return randomValue;
};

// Function to dynamically include Leaflet script
const includeLeafletScript = (html, leafletScriptContent) => {
  return html.replace('</head>', `${leafletScriptContent}</head>`);
};

// Main Lambda handler
exports.handler = async (event) => {
  try {
    const s3Object = await fetchS3Object();
    const randomValue = await getRandomValueFromDynamoDB();
    const leafletScriptContent = await readLeafletScript();

    // Replace the placeholder with the random value
    let modifiedHtml = s3Object.Body.toString('utf-8').replace('REPLACE_WITH_RANDOM_NUMBER', `Random Value: ${randomValue}`);

    // Include Leaflet script dynamically
    modifiedHtml = includeLeafletScript(modifiedHtml, leafletScriptContent);

    // Log the modified HTML content
    console.log('Modified HTML:', modifiedHtml);

    // Return the modified HTML content with appropriate Content-Type
    const response = {
      statusCode: 200,
      headers: {
        'Content-Type': 'text/html',
      },
      body: modifiedHtml,
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
