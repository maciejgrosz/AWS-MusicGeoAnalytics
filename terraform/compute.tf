# Configure AWS provider
provider "aws" {
  region = "eu-west-1"
  profile = "sandbox"
}


# Create DynamoDB table
resource "aws_dynamodb_table" "soundcloud-data" {
  name         = "soundcloud-data"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "Id"

  attribute {
    name = "Id"
    type = "S" 
  }
}

# Create Lambda function
resource "aws_lambda_function" "soundcloud-backend" {
  filename      = "function.zip"
  function_name = "app"
  role          = aws_iam_role.lambda.arn
  handler       = "index.handler"
  runtime       = "nodejs16.x"

  }

# Create IAM role for Lambda - add s3 permission - readonlyAccess i pewnie dynamodb
resource "aws_iam_role" "lambda" {
  name = "lambda"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

# Create API Gateway REST API
resource "aws_api_gateway_rest_api" "soundcloud-api" {
  name = "soundcloud-api"
}

# Create Lambda permission for API Gateway 
resource "aws_lambda_permission" "apigw" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.soundcloud-backend.arn
  principal     = "apigateway.amazonaws.com"

  # The "/*/*" portion grants access from any method on any resource
  # within the API Gateway REST API.
  source_arn = "${aws_api_gateway_rest_api.soundcloud-api.execution_arn}/*/*"
}

# Create API Gateway resource and method for Lambda
resource "aws_api_gateway_resource" "proxy" {
  rest_api_id = aws_api_gateway_rest_api.soundcloud-api.id
  parent_id   = aws_api_gateway_rest_api.soundcloud-api.root_resource_id
  path_part   = "{proxy+}"
}

resource "aws_api_gateway_method" "proxy" {
  rest_api_id   = aws_api_gateway_rest_api.soundcloud-api.id
  resource_id   = aws_api_gateway_resource.proxy.id
  http_method   = "ANY"
  authorization = "NONE"
}

# Create API Gateway deployment
resource "aws_api_gateway_deployment" "soundcloud-api-deployment" {
  depends_on = [
    aws_api_gateway_integration.lambda
  ]

  rest_api_id = aws_api_gateway_rest_api.soundcloud-api.id
  stage_name  = "test"
}

resource "aws_api_gateway_integration" "lambda" {
  rest_api_id = aws_api_gateway_rest_api.soundcloud-api.id 
  resource_id = aws_api_gateway_method.proxy.resource_id
  http_method = aws_api_gateway_method.proxy.http_method

  integration_http_method = "POST"
  type                    = "AWS_PROXY" 
  uri                     = aws_lambda_function.soundcloud-backend.invoke_arn
}

# Create S3 bucket
resource "aws_s3_bucket" "website" {
  bucket = "tass-musicgeoanalyser"
}
