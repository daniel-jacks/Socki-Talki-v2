import boto3
import json

def lambda_handler(event, context):
    client = boto3.resource('dynamodb')
    api = boto3.client('apigatewaymanagementapi', 
    endpoint_url='https://qxjk1x8u4e.execute-api.us-west-2.amazonaws.com/production')
    roomTable = client.Table('Socki-Talki-Rooms')
    userTable = client.Table('Socki-Talki-Users')

    try:
        route = event['requestContext']['routeKey']
        connectionId = event['requestContext']['connectionId']
    except:
        return {
            'statusCode': 400,
            'errorMessage': 'Bad Request'
        }
            
    if route == 'message':
        try:
            message = json.loads( event['body'] )['message']
            user = userTable.get_item( Key = { 'userId': str(connectionId) } )
            userRoom = user['Item']['roomName']
            userName = user['Item']['userName']
            payload = f'{userName}?{message}'
            userIds = roomTable.get_item( Key = {'roomName': userRoom} )['Item']['userIds']
            print( 'Message attempt from:', str(connectionId) )
            for userId in userIds:
                if userId != connectionId:
                    api.post_to_connection( Data = payload.encode('utf-8'), ConnectionId = str(userId) )
            print( 'Message success from:', str(connectionId) )
        except:
            return {
                'statusCode': 400,
                'errorMessage': 'Error getting response data'
            }
        
    return {
        'statusCode': 200
    }