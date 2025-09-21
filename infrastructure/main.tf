locals {
  backend_code_path = "${path.module}/../backend"
  lambda_function_name = "list_service"
  environment = "prod"
}


terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.14.0"
    }
  }
}

provider "aws" {
  region = "eu-north-1"
}

## Trust policy for the Lambda role that allows Lambda function to assume the role.
data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

## Allows Lambda function to log to Cloudwatch
resource "aws_iam_policy" "lambda_logging_policy" {
  name   = "function-logging-policy"
  policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        Action : [
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        Effect : "Allow",
        Resource : "arn:aws:logs:*:*:*"
      }
    ]
  })
}


## The actual Lambda function IAM role using the above policies.
resource "aws_iam_role" "list_service_lambda_role" {
  name               = "list_service_lambda_role"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}


resource "aws_iam_role_policy_attachment" "lambda_logging_policy_attachment" {
  role       = aws_iam_role.list_service_lambda_role.id
  policy_arn = aws_iam_policy.lambda_logging_policy.arn
}


## Package the Lambda function code
data "archive_file" "list_service_lambda_code" {
  type        = "zip"
  source_file = "${local.backend_code_path}/listService/src/lambdaHandler.py"
  output_path = "${local.backend_code_path}/listService/lambdaHandler.zip"
}

## Create cloudwatch log group for the Lambda function.
resource "aws_cloudwatch_log_group" "lambda_log_group" {
  name              = "/aws/lambda/${local.lambda_function_name}"
  retention_in_days = 1
  lifecycle {
    prevent_destroy = false
  }
}

# Lambda function
resource "aws_lambda_function" "list_service_lambda_function" {
  filename         = data.archive_file.list_service_lambda_code.output_path
  function_name    = local.lambda_function_name
  role             = aws_iam_role.list_service_lambda_role.arn
  handler          = "lambdaHandler.handler"
  depends_on       = [aws_cloudwatch_log_group.lambda_log_group]
  source_code_hash = data.archive_file.list_service_lambda_code.output_base64sha256

  runtime = "python3.13"

  environment {
    variables = {
      ENVIRONMENT = local.environment
      LOG_LEVEL   = "DEBUG"
    }
  }
}


### API Gateway
###
resource "aws_api_gateway_rest_api" "list_service_api" {
  name        = "list-service-api"
  description = "API Gateway for List Service"
}


### API Gateway resource
###
resource "aws_api_gateway_resource" "root" {
  rest_api_id = aws_api_gateway_rest_api.list_service_api.id
  parent_id   = aws_api_gateway_rest_api.list_service_api.root_resource_id
  path_part   = "{proxy+}"
}


### GET methods for the resource
resource "aws_api_gateway_method" "root_get" {
  rest_api_id   = aws_api_gateway_rest_api.list_service_api.id
  resource_id   = aws_api_gateway_resource.root.id
  http_method   = "GET"
  authorization = "NONE"
}

### Lambda integrations for the resource.
resource "aws_api_gateway_integration" "root_get_integration" {
  rest_api_id = aws_api_gateway_rest_api.list_service_api.id
  resource_id = aws_api_gateway_resource.root.id
  http_method = aws_api_gateway_method.root_get.http_method

  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.list_service_lambda_function.invoke_arn
}

# Allows API Gateway to invoke our Lambda function
resource "aws_lambda_permission" "list_service_api_permission" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.list_service_lambda_function.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.list_service_api.execution_arn}/*/GET/*"
}

# API Gateway deployment
resource "aws_api_gateway_deployment" "list_service_api_deployment" {
  depends_on = [
    aws_api_gateway_integration.root_get_integration
  ]

  rest_api_id = aws_api_gateway_rest_api.list_service_api.id
}

# API Gateway stage
resource "aws_api_gateway_stage" "list_service_api_stage" {
  deployment_id = aws_api_gateway_deployment.list_service_api_deployment.id
  rest_api_id   = aws_api_gateway_rest_api.list_service_api.id
  stage_name    = local.environment
}

# Output the API Gateway URL
output "api_url" {
  value = "${aws_api_gateway_stage.list_service_api_stage.invoke_url}/"
}


