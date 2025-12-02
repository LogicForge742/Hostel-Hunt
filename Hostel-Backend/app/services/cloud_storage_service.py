import boto3
from flask import current_app
from botocore.exceptions import ClientError

class S3Service:
    """Handles interaction with Amazon S3 for file uploads and management."""

    @staticmethod
    def _get_s3_client():
        """Initializes and returns the Boto3 S3 client."""
        # Ensure AWS keys are configured in Flask's config
        return boto3.client(
            's3',
            aws_access_key_id=current_app.config['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=current_app.config['AWS_SECRET_ACCESS_KEY'],
            region_name=current_app.config['AWS_REGION']
        )

    @staticmethod
    def upload_file(file, filename, folder='hostel-images'):
        """
        Uploads a file object to S3.

        :param file: The file object from request.files.
        :param filename: The unique filename (e.g., uuid.jpg).
        :param folder: The subfolder inside the bucket to store the file.
        :return: The public URL of the uploaded file, or None on failure.
        """
        s3_client = S3Service._get_s3_client()
        bucket_name = current_app.config['S3_BUCKET_NAME']
        
        # S3 Key is the path inside the bucket (e.g., 'hostel-images/abc1234.jpg')
        s3_key = f"{folder}/{filename}"
        
        # Move file pointer to the start before reading/uploading
        file.seek(0)

        try:
            # Upload the file object
            s3_client.upload_fileobj(
                file,
                bucket_name,
                s3_key,
                ExtraArgs={
                    # Important: Makes the uploaded file publicly accessible
                    'ACL': 'public-read', 
                    # Set the correct content type for the file
                    'ContentType': file.content_type 
                }
            )
            
            # Construct the public URL
            public_url = f"https://{bucket_name}.s3.{current_app.config['AWS_REGION']}.amazonaws.com/{s3_key}"
            return public_url
            
        except ClientError as e:
            current_app.logger.error(f"S3 Upload Error: {e}")
            return None
        except Exception as e:
            current_app.logger.error(f"General Upload Error: {e}")
            return None