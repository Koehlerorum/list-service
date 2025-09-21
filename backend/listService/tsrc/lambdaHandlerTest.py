
import unittest
import logging
from lambdaHandler import handler

#logging.basicConfig(level=logging.DEBUG) 

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

    def testHead(self):
        request = getSimpleTestRequest('head')
        self.assertDictEqual(handler(request, None), 
            {
                "isBase64Encoded": False,
                "statusCode": 200,
                "body": 'value1'
            })

    def testHeadEmpty(self):
        request = getSimpleTestRequest('head', True)
        self.assertDictEqual(handler(request, None), 
            {
                "isBase64Encoded": False,
                "statusCode": 200,
                "body": ''
            })


    def testTail(self):
        request = getSimpleTestRequest('tail')
        self.assertDictEqual(handler(request, None),
            {
                "isBase64Encoded": False,
                "statusCode": 200,
                "body": '["value2", "value3"]'
            })

    def testTailEmpty(self):
        request = getSimpleTestRequest('tail', True)
        self.assertDictEqual(handler(request, None),
            {
                "isBase64Encoded": False,
                "statusCode": 200,
                "body": '[]'
            })

    def testLast(self):
        request = getSimpleTestRequest('last')
        self.assertDictEqual(handler(request, None), 
            {
                "isBase64Encoded": False,
                "statusCode": 200,
                "body": 'value3'
            })


    def testLastEmpty(self):
        request = getSimpleTestRequest('last', True)
        self.assertDictEqual(handler(request, None), 
            {
                "isBase64Encoded": False,
                "statusCode": 200,
                "body": ''
            })

    def testHeadInvalidInput(self):
        request = getSimpleTestRequest('head')
        request['multiValueQueryStringParameters']['strings'] = [1,2,3,4]
        self.assertDictEqual(handler(request, None),
            {
                "isBase64Encoded": False,
                "statusCode": 400,
                "body": 'Invalid input arguments. The input has to given in format "<operation>?strings=string0&strings=string1&..."'
            })


    def testHeadInvalidOperation(self):
        request = getSimpleTestRequest('foo')
        self.assertDictEqual(handler(request, None),
            {
                "isBase64Encoded": False,
                "statusCode": 400,
                "body": 'Unrecognized operation. Available operations are "head", "tail" and "last"'
            })

    
    def testNoQueryParameters(self):
        request = getSimpleTestRequest('head')
        request['multiValueQueryStringParameters'] = None
        self.assertDictEqual(handler(request, None),
            {
                "isBase64Encoded": False,
                "statusCode": 400,
                "body": 'Invalid input arguments. The input has to given in format "<operation>?strings=string0&strings=string1&..."'
            })
    
    def testExtraQueryParameters(self):
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
