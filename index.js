const AWS = require('aws-sdk');
const s3 = new AWS.S3();
const dynamodb = new AWS.DynamoDB();

// Function to fetch content from S3
const fetchS3Object = async () => {
  return await s3.getObject({
    Bucket: 'tass-musicgeoanalyser',
    Key: 'index.html',
  }).promise();
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

// Main Lambda handler
exports.handler = async (event) => {
  try {
    const s3Object = await fetchS3Object();
    const randomValue = await getRandomValueFromDynamoDB();

    // Replace the placeholder with the random value
    const modifiedHtml = s3Object.Body.toString('utf-8').replace('REPLACE_WITH_RANDOM_NUMBER', `Random Value: ${randomValue}`);

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
