
import logging
import os
import json

# Sets the desired log level
logger = logging.getLogger()
logLevel = os.environ.get('LOG_LEVEL')
if logLevel:
    logger.setLevel(logLevel)


# Implementations of the actual string list operations.
def head(inputStrings):
    if len(inputStrings) > 0:
        return inputStrings[0]
    
    return ""

def tail(inputStrings):
    if len(inputStrings) > 1:
        return inputStrings[1:]
    
    return []


def last(inputStrings):
    if len(inputStrings) > 0:
        return inputStrings[-1]
    
    return ""

# Maps the operation strings to functions.
operations = {
    'head': head,
    'tail': tail,
    'last': last,
}

# Transforms to the response to the format API gateway expects.
def generateResponse(statusCode, payload):

    if not type(payload) == str:
        payload = json.dumps(payload)

    return {
        "isBase64Encoded": False,
        "statusCode": statusCode,
        "body": payload
    }

# Lambda handler function.
def handler(event, _context):

    PARAMETER_KEY = 'strings'

    logger.debug('# Event')
    logger.debug(event)
    
    ## Retrieves the list of strings passed in by the caller.
    ## Retrieve fails, if there are unknown query parameters.
    inputStrings = None
    multiValueQueryStringParameters = event.get('multiValueQueryStringParameters')
    if (multiValueQueryStringParameters):
        ## Ensure that there are no unexpected arguments.
        parameterKeys = list(multiValueQueryStringParameters.keys())
        if len(parameterKeys) == 1 and parameterKeys[0] == PARAMETER_KEY:
            inputStrings = multiValueQueryStringParameters.get(PARAMETER_KEY)


    logger.debug("# Input strings")
    logger.debug(inputStrings)

    # Validate the inputs:
    pathParameters = event.get('pathParameters', {})
    if not pathParameters or pathParameters.get('proxy') not in operations:
        ## For some reason proxy parameter is missing. (We have been called in some other way than intended.)
        response = generateResponse(400, 'Unrecognized operation. Available operations are "head", "tail" and "last"')
    elif type(inputStrings) != list or not all(isinstance(item, str) for item in inputStrings):
        ## Input string array is missing.
        response = generateResponse(400, 'Invalid input arguments. The input has to given in format "<operation>?strings=string0&strings=string1&..."')
    else:
        response = generateResponse(200, operations[pathParameters.get('proxy')](inputStrings))

    logger.debug("Response:")
    logger.debug(response)
    return response
    