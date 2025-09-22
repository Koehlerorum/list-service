
# Basic Architecture

The architecture of this sample is very simple. REST API request are received by AWS API gateway that triggers a Lambda function for each GET request. 

The Lambda function examines the path in the request URL and selects the desired operation based on that. The string array is passed to the service using HTTP query parameters.

# Source Tree Structure

## backend

backend directory contains the backend source code and their associated unit tests. In this case the backend contains only one Lambda function called *listService*

## infrastructure

infrastructure directory contains all the required Terraform definitions to deploy the Lambda function and the API Gateway to AWS.

# How to Run The Unit Test

The unit tests have been developed and tested using **Python 3.13**.

In directory **backend/listService/** issue command:

``$ PYTHONPATH=src/ python -m unittest tsrc/lambdaHandlerTest.py``

# Deployment to AWS

It is assumed here that you have working *terraform* and *aws* cli installation with working AWS credentials. All of the following commands has to be issues at directory **infrastructure**.

If you are first time deploying the infrastructure, you must start with command:

``$ terraform init``

After the *init* command it is recommended, but not strictly necessary, to run the following commands:

``$ terraform validate``

and

``$ terraform plan``

After resolving possible errors, you can deploy the code to AWS using command:

``$ terraform apply``

At the end of the apply process Terraform prints out the API gateway URL that can be used in testing.

After you are done with the service, it can be removed with command:

``$ terraform destroy``

# Usage

You can test the service using e.g. curl:


``$ curl "https://<api gateway id>.execute-api.eu-north-1.amazonaws.com/prod/head?strings=foo&strings=bar"``

``$ curl "https://<api gateway id>.execute-api.eu-north-1.amazonaws.com/prod/tail?strings=foo&strings=bar"``

``$ curl "https://<api gateway id>.execute-api.eu-north-1.amazonaws.com/prod/last?strings=foo&strings=bar"``

For full API documentation see file **apiSpecification.yml**
