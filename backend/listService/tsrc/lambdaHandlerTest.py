
import unittest
import logging
from lambdaHandler import handler

logging.basicConfig(level=logging.DEBUG) 

def getSimpleTestRequest(operation, empty = False):

    simpleRequest = {
        "resource": f'/{operation}',
        "path": f'/{operation}',
        "httpMethod": "GET",
        "multiValueQueryStringParameters": {
            "strings": ["value1", "value2", "value3"]
        },
        "pathParameters": {
            'proxy': operation
        }
    }

    if empty:
        simpleRequest["multiValueQueryStringParameters"]["strings"] = []

    return simpleRequest



class TestLambdaHandler(unittest.TestCase):

    def test_head(self):
        request = getSimpleTestRequest('head')
        self.assertDictEqual(handler(request, None), 
            {
                "isBase64Encoded": False,
                "statusCode": 200,
                "body": 'value1'
            })

    def test_head_empty(self):
        request = getSimpleTestRequest('head', True)
        self.assertDictEqual(handler(request, None), 
            {
                "isBase64Encoded": False,
                "statusCode": 200,
                "body": ''
            })


    def test_tail(self):
        request = getSimpleTestRequest('tail')
        self.assertDictEqual(handler(request, None),
            {
                "isBase64Encoded": False,
                "statusCode": 200,
                "body": '["value2", "value3"]'
            })

    def test_tail_empty(self):
        request = getSimpleTestRequest('tail', True)
        self.assertDictEqual(handler(request, None),
            {
                "isBase64Encoded": False,
                "statusCode": 200,
                "body": '[]'
            })

    def test_last(self):
        request = getSimpleTestRequest('last')
        self.assertDictEqual(handler(request, None), 
            {
                "isBase64Encoded": False,
                "statusCode": 200,
                "body": 'value3'
            })


    def test_last_empty(self):
        request = getSimpleTestRequest('last', True)
        self.assertDictEqual(handler(request, None), 
            {
                "isBase64Encoded": False,
                "statusCode": 200,
                "body": ''
            })

    def test_head_invalid_input(self):
        request = getSimpleTestRequest('head')
        request['multiValueQueryStringParameters']['strings'] = [1,2,3,4]
        self.assertDictEqual(handler(request, None),
            {
                "isBase64Encoded": False,
                "statusCode": 400,
                "body": 'Invalid input arguments. The input has to given in format "<operation>?strings=string0&strings=string1&..."'
            })


    def test_head_invalid_operation(self):
        request = getSimpleTestRequest('foo')
        self.assertDictEqual(handler(request, None),
            {
                "isBase64Encoded": False,
                "statusCode": 400,
                "body": 'Unrecognized operation operation. Available operations are "head", "tail" and "last"'
            })

    
    def test_no_query_parameters(self):
        request = getSimpleTestRequest('head')
        request['multiValueQueryStringParameters'] = None
        self.assertDictEqual(handler(request, None),
            {
                "isBase64Encoded": False,
                "statusCode": 400,
                "body": 'Invalid input arguments. The input has to given in format "<operation>?strings=string0&strings=string1&..."'
            })
    
    def test_extra_query_parameters(self):
        request = getSimpleTestRequest('head')
        request['multiValueQueryStringParameters']['strin'] = "foo"
        self.assertDictEqual(handler(request, None),
            {
                "isBase64Encoded": False,
                "statusCode": 400,
                "body": 'Invalid input arguments. The input has to given in format "<operation>?strings=string0&strings=string1&..."'
            })

if __name__ == '__main__':
    unittest.main()
