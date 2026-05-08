import os
import boto3
import json

region_aws = os.getenv('REGION_AWS', 'ap-southeast-1')
db_tablename = os.getenv('DB_NAME')
ddb = boto3.resource('dynamodb', region_name=region_aws).Table(db_tablename)

def lambda_handler(event, context):
    # This expects {"short_id": "..."} from the API Gateway Mapping Template
    short_id = event.get('short_id')
    
    if not short_id:
        return {
            'statusCode': 400,
            'body': 'Missing short_id in request.'
        }

    try:
        # Get the item from DynamoDB
        response = ddb.get_item(Key={'short_id': short_id})
        
        if 'Item' not in response:
            return {
                'statusCode': 404,
                'body': 'Short URL not found.'
            }

        item = response.get('Item')
        long_url = item.get('long_url')

        # Increment hit counter
        ddb.update_item(
            Key={'short_id': short_id},
            UpdateExpression='set hits = hits + :val',
            ExpressionAttributeValues={':val': 1}
        )

        # Return the location for the 302 redirect
        return {
            "statusCode": 302,
            "location": long_url
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': 'Internal Server Error'
        }
