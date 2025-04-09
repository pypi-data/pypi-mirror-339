import boto3

from loguru import logger
from .decorators import execution_time


s3_client = boto3.client('s3')


@execution_time
def download_file(
    bucket_name: str,
    object_key: str,
    file_path: str
) -> bool:
    """
    Download a file from an S3 bucket

    Args:
        bucket_name (str): Bucket name
        object_key (str): S3 object key
        file_path (str): Local file path where the file will be downloaded

    Returns:
        bool: True if file was downloaded successfully, else False
    """
    try:
        s3_client.download_file(bucket_name, object_key, file_path)
        return True
    except ClientError as e:
        logger.error(f"Error downloading file {object_key} from bucket {bucket_name}: {str(e)}")
        return False


@execution_time
def generate_presigned_url(
    bucket_name: str,
    object_key: str,
    expires_in: int = 3600,
    content_type: str = 'text/csv'
) -> str:
    """
    Generate a presigned URL for an S3 object

    Args:
        bucket_name (str): Bucket name
        object_key (str): S3 object key
        expires_in (int): Time in seconds for the presigned URL to expire
        content_type (str): Content type of the file

    Returns:
        str: Presigned URL for downloading the file via HTTP
    """
    res = s3_client.generate_presigned_url(
        'get_object',
        Params={
            'Bucket': bucket_name,
            'Key': object_key,
            'ResponseContentType': content_type,
            'ResponseContentDisposition': f'attachment; filename="{object_key}"'
        },
        ExpiresIn=expires_in
    )
    logger.info(f"Presigned URL: {res}")
    return res


@execution_time
def upload_file(
    bucket_name: str,
    body: str,
    filename: str,
    content_type: str = 'text/csv'
) -> str:
    """Upload a CSV string to S3 and generate a presigned URL for download.

    Args:
        bucket_name (str): Bucket name
        body (str): CSV string to upload
        filename (str): Name of the file to be created in S3
        content_type (str): Content type of the file

    Returns:
        str: Name of the file uploaded to S3
    """
    try:
        s3_client.put_object(
            Bucket=bucket_name,
            Key=filename,
            Body=body,
            ContentType=content_type
        )
        return filename
    except Exception as e:
        logger.error(f"Error uploading file to S3: {str(e)}")
        raise
