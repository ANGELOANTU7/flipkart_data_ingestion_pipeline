import json
import boto3
import base64
from io import BytesIO

def lambda_handler(event, context):
    # If it's a CORS preflight request, respond accordingly
    if event['httpMethod'] == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',  # or '*'
                'Access-Control-Allow-Methods': '*',
            },
            'body': ''
        }
    
    # Handle the POST request
    if event['httpMethod'] == 'POST':
        s3_client = boto3.client('s3')
        bucket_name = 'flipkartstore'
        
        try:
            body = json.loads(event['body'])
            video_data = base64.b64decode(body['body'])
            object_name = body.get('object_name', 'default_video')
            file_name = f"{object_name}.mp4"
            file_key = f'{file_name}'
            
            s3_client.put_object(
                Bucket=bucket_name,
                Key=file_key,
                Body=BytesIO(video_data),
                ContentType='video/mp4'
            )
            
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Origin': 'https://frontend.angeloantu.online',
                    'Access-Control-Allow-Methods': 'POST, OPTIONS',
                },
                'body': json.dumps(f'Video uploaded successfully as {file_name}!')
            }
        
        except Exception as e:
            return {
                'statusCode': 500,
                'headers': {
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Origin': 'https://frontend.angeloantu.online',
                    'Access-Control-Allow-Methods': 'POST, OPTIONS',
                },
                'body': json.dumps(f'Error uploading video: {str(e)}')
            }
