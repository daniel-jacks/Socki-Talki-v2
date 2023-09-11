import boto3
import json

def lambda_handler(event, context):
    client = boto3.resource('dynamodb')
    api = boto3.client('apigatewaymanagementapi', 
    endpoint_url='https://qxjk1x8u4e.execute-api.us-west-2.amazonaws.com/production')
    userTable = client.Table('Socki-Talki-Users')

    try:
        route = event['requestContext']['routeKey']
        connectionId = event['requestContext']['connectionId']
    except:
        return {
            'statusCode': 400,
            'errorMessage': 'Bad Request'
        }
            
    if route == 'setUsername':
        try:
            userName = json.loads( event['body'] )['userName']
            userTable.update_item(
                Key = { 'userId': str(connectionId) },
                UpdateExpression="SET userName = :u",
                ExpressionAttributeValues={
                    ':u': str(userName)
                },
            )
            message = f'Sucess! Username set to: {userName}'
            api.post_to_connection( Data = message.encode('utf-8'), ConnectionId = str(connectionId)) 
        except:
            return {
                'statusCode': 400,
                'errorMessage': 'Error getting response data'
            }
        
    return {
        'statusCode': 200
    }