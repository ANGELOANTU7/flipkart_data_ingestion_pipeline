import json
import boto3

def lambda_handler(event, context):
    # Initialize the S3 client
    s3_client = boto3.client('s3')
    
    # Specify the bucket name and object key
    bucket_name = 'flipkartprocessedpreview'
    object_key = 'dataset_details/class_counts.json'
    
    try:
        # Fetch the object from S3
        s3_response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
        
        # Read the object's content
        content = s3_response['Body'].read().decode('utf-8')
        
        # Parse the JSON content
        json_content = json.loads(content)
        
        # Return the JSON content in the response
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': '*'
            },
            'body': json.dumps(json_content)
        }
    
    except Exception as e:
        # Handle any exceptions that occur
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error fetching or parsing S3 object: {str(e)}')
        }
