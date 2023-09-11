import boto3

def lambda_handler(event, context):
    client = boto3.resource('dynamodb')
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
          
    if route == "$disconnect":
        try:
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
            userTable.delete_item(
                Key = { 'userId': str(connectionId) }    
            )
            print('Disconnection occured')
        except:
            print('Error disconnecting user')
            return 

    return {
        'statusCode': 200
    }