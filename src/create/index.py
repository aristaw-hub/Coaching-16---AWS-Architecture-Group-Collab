import os
import json
import boto3
from string import ascii_letters, digits
from random import choice, randint
from time import strftime, time
from urllib import parse

# Load environment variables
app_url = os.getenv('APP_URL')  # Should be https://group5-urlshortener.sctp-sandbox.com/
min_char = int(os.getenv('MIN_CHAR', 6))
max_char = int(os.getenv('MAX_CHAR', 10))
region_aws = os.getenv('REGION_AWS', 'ap-southeast-1')
db_tablename = os.getenv('DB_NAME')

string_format = ascii_letters + digits
ddb = boto3.resource('dynamodb', region_name=region_aws).Table(db_tablename)

def generate_timestamp():
    return strftime("%Y-%m-%dT%H:%M:%S")

def expiry_date():
    # Set TTL for 7 days (604800 seconds)
    return int(time()) + 604800

def generate_id():
    """Generates a random ID and checks DynamoDB to ensure it's unique."""
    short_id = "".join(choice(string_format) for _ in range(randint(min_char, max_char)))
    
    # Check if ID already exists
    response = ddb.get_item(Key={'short_id': short_id})
    if 'Item' in response:
        return generate_id()  # Recursive call if collision occurs
    return short_id

def lambda_handler(event, context):
    print(f"Received event: {json.dumps(event)}")
    
    try:
        # Parse the long URL from the request body
        body = json.loads(event.get('body', '{}'))
        long_url = body.get('long_url')
        
        if not long_url:
            return {"statusCode": 400, "body": "Missing long_url"}

        short_id = generate_id()
        short_url = f"{app_url}{short_id}"
        timestamp = generate_timestamp()
        ttl_value = expiry_date()

        # Gather Analytics
        headers = event.get('headers', {})
        analytics = {
            'user_agent': headers.get('User-Agent'),
            'source_ip': headers.get('X-Forwarded-For', event.get('requestContext', {}).get('identity', {}).get('sourceIp')),
            'xray_trace_id': os.getenv('_X_AMZN_TRACE_ID')
        }

        # Parse query parameters from the long URL for additional analytics
        parsed_url = parse.urlsplit(long_url)
        if parsed_url.query:
            url_params = dict(parse.parse_qsl(parsed_url.query))
            analytics.update(url_params)

        # Save to DynamoDB
        ddb.put_item(
            Item={
                'short_id': short_id,
                'created_at': timestamp,
                'ttl': ttl_value,
                'short_url': short_url,
                'long_url': long_url,
                'analytics': analytics,
                'hits': 0
            }
        )

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "text/plain"},
            "body": short_url
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal Server Error"})
        }
