import boto3
import json

def lambda_handler(event, context):
    client = boto3.resource('dynamodb')
    api = boto3.client('apigatewaymanagementapi', 
    endpoint_url='https://2gc6x410ok.execute-api.us-west-2.amazonaws.com/test')
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
    
    if route == 'changeRoom':
        try:
            newRoom = json.loads( event['body'] )['newRoom']
            roomTable.update_item(
                Key = { 'roomName': str(newRoom) },
                UpdateExpression="SET userIds = list_append(userIds, :i)",
                ExpressionAttributeValues={
                    ':i': [str(connectionId)]
                },
                ReturnValues="UPDATED_NEW"
            )
            userRoom = userTable.get_item( Key = { 'userId': str(connectionId) } )['Item']['roomName']
            userIds = roomTable.get_item( Key = { 'roomName': str(userRoom) } )['Item']['userIds']
            userIds.remove( str(connectionId) )
            roomTable.update_item(
                Key = { 'roomName': str(userRoom) },
                UpdateExpression="SET userIds = :u",
                ExpressionAttributeValues={
                    ':u': userIds
                },
                ReturnValues="ALL_NEW"
            )
            userTable.update_item(
                Key = { 'userId': str(connectionId) },
                UpdateExpression="SET roomName = :r",
                ExpressionAttributeValues={
                    ':r': str(newRoom)
                },
            )
            message = f'Success! Room set to: {newRoom}.'
            api.post_to_connection( Data = message.encode('utf-8'), ConnectionId = str(connectionId)) 
        except:
            message = 'Failed changing room, please ensure room exists.'
            api.post_to_connection( Data = message.encode('utf-8'), ConnectionId = str(connectionId)) 
            return { 
                'statusCode': 200,
            }

    return {
        'statusCode': 200,
    }