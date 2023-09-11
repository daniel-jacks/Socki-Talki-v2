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

    if route == 'createRoom':
        try:
            roomName = json.loads( event['body'] )['newRoom']
            autoJoin = json.loads( event['body'] )['autoJoin']
            userIds = [str(connectionId)] if  autoJoin else []
            if roomTable.get_item( Key = { 'roomName': str(roomName) }):
                message = f'Unsuccessful! Room: "{roomName}" already exists. Try the *changeRoom command instead!'
                api.post_to_connection( Data = message.encode('utf-8'), ConnectionId = str(connectionId)) 
                return {
                    'statusCode': 200,
                }

            roomTable.put_item(
                Item={
                    'roomName': str(roomName),
                    'messages': [],
                    'userIds': userIds
                }
            )
            if autoJoin:
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
                userTable.put_item(
                    Item={
                        'userId': str(connectionId),
                        'roomName': str(roomName)
                    }
                )
        except:
            return {
                'statusCode': 400,
                'errorMessage': 'Error creating room'
            }

    return {
        'statusCode': 200,
    }