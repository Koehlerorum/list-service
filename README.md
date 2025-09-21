
# Basic Architecture

The architecture of this sample is very simple. REST API request are received by AWS API gateway that triggers a Lambda function for each GET request. 

The Lambda function examines the path of the request URL and selects the desired operation based on that. The string array is passed to the service using HTTP query parameters.

# Source Tree Structure

## backend

backend directory contains all the backend source code and their associated unittest. In this case there is only one Lambda function called *listService*

## infrastructure

infrastructure directory contains all the required Terraform definitions to deploy the Lambda function and the API Gateway


# How to run unittest

In directory *backend/listService/* issue commands:

``$ PYTHONPATH=src/ python -m unittest tsrc/lambdaHandlerTest.py``

# Deployment

It is assumed here that you have working *terraform* and *aws* cli installation and that you known how to configure and use your AWS credentials. All of the following commands has to be issues at directory *infrastructure*.

If you are first time deploying the infrastructure, you must start with command:

``infrastructure $ terraform init``

After the *init* command it is recommended, but not strictly necessary, to run the following commands:

``infrastructure $ terraform validate``

and

``infrastructure $ terraform plan``

After running all possible errors have been resolved, you can deploy the code to AWS using command:

``infrastructure $ terraform apply``

At the end of the apply process Terraform prints out the API gateway URL that can be used in testing.


When you are done with the service, it can be removed with command:

``infrastructure $ terraform destroy``

# Usage

You can test the service using e.g. curl:


``$ curl "https://<api gateway id>.execute-api.eu-north-1.amazonaws.com/prod/head?strings=foo&strings=bar"``

``$ curl "https://<api gateway id>.execute-api.eu-north-1.amazonaws.com/prod/tail?strings=foo&strings=bar"``

``$ curl "https://<api gateway id>.execute-api.eu-north-1.amazonaws.com/prod/last?strings=foo&strings=bar"``

For full API documentation see file **apiSpecification.yml**
