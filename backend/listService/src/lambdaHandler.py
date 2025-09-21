
import logging
import os
import json

# Sets the desired log level
logger = logging.getLogger()
log_level = os.environ.get('LOG_LEVEL')
if log_level:
    logger.setLevel(log_level)


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
def generate_response(status_code, payload):

    if not type(payload) == str:
        payload = json.dumps(payload)

    return {
        "isBase64Encoded": False,
        "statusCode": status_code,
        "body": payload
    }

# Lambda handler function.
def handler(event, _context):

    PARAMETER_KEY = 'strings'

    logger.debug('# Event')
    logger.debug(event)
    
    ## Retrieves the list of strings passed in by the caller.
    ## Retrieve fails, if there are unknown query parameters.
    input_strings = None
    multiValueQueryStringParameters = event.get('multiValueQueryStringParameters')
    if (multiValueQueryStringParameters):
        ## Ensure that there are no unexpected arguments.
        parameterKeys = list(multiValueQueryStringParameters.keys())
        if len(parameterKeys) == 1 and parameterKeys[0] == PARAMETER_KEY:
            input_strings = multiValueQueryStringParameters.get(PARAMETER_KEY)


    logger.debug("# Input strings")
    logger.debug(input_strings)

    # Validate the inputs:
    pathParameters = event.get('pathParameters', {})
    if not pathParameters or pathParameters.get('proxy') not in operations:
        ## For some reason proxy parameter is missing. (We have been called in some other way than intended.)
        response = generate_response(400, 'Unrecognized operation. Available operations are "head", "tail" and "last"')
    elif type(input_strings) != list or not all(isinstance(item, str) for item in input_strings):
        ## Input string array is missing.
        response = generate_response(400, 'Invalid input arguments. The input has to given in format "<operation>?strings=string0&strings=string1&..."')
    else:
        response = generate_response(200, operations[pathParameters.get('proxy')](input_strings))

    logger.debug("Response:")
    logger.debug(response)
    return response
    