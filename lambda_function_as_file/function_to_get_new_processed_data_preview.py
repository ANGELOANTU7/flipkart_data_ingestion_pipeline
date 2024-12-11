import json
import boto3
import random
from botocore.exceptions import ClientError

# Initialize S3 client
s3 = boto3.client('s3')

def lambda_handler(event, context):
    # Input parameters
    bucket_name = 'flipkartprocessedpreview'  # Replace with your bucket name
    number_of_images = event.get('number_of_images', 10)  # Default to 10 if not specified

    try:
        # List the objects in the S3 bucket
        response = s3.list_objects_v2(Bucket=bucket_name)

        # Check if the bucket contains any objects
        if 'Contents' not in response:
            return {
                'statusCode': 400,
                'body': json.dumps('No images found in the S3 bucket.')
            }

        # Extract the image keys (file names) and sort by LastModified (latest first)
        objects = response['Contents']
        sorted_objects = sorted(objects, key=lambda obj: obj['LastModified'], reverse=True)

        # Extract sorted keys
        sorted_image_keys = [obj['Key'] for obj in sorted_objects]

        # Ensure we do not request more images than available
        number_of_images = min(number_of_images, len(sorted_image_keys))

        # Select the top images based on the sorted list
        selected_images = sorted_image_keys[:number_of_images]

        # Construct the image URIs
        base_uri = f'https://{bucket_name}.s3.amazonaws.com/'
        image_uris = [base_uri + image_key for image_key in selected_images]

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': '*'
            },
            'body': json.dumps({
                'image_uris': image_uris
            })
        }

    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error retrieving images from S3: {e.response['Error']['Message']}")
        }