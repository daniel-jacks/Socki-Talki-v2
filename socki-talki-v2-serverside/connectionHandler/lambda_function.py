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
            
    if route == '$connect':
        try:
            roomTable.update_item(
                Key = { 'roomName': 'global' },
                UpdateExpression="SET userIds = list_append(userIds, :i)",
                ExpressionAttributeValues={
                    ':i': [str(connectionId)]
                },
                ReturnValues="UPDATED_NEW"
            )
            userTable.put_item(
                Item={
                    'userId': str(connectionId),
                    'roomName': 'global',
                    'userName': 'none'
                }
            )
            print( 'Connection occured at:', str(connectionId) )
        except: 
            return {
                'statusCode': 400,
                'errorMessage': 'Error joining room'
            }
            
    return {
        'statusCode': 200
    }