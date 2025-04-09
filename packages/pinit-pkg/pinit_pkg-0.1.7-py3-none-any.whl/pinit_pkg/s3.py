import boto3

from loguru import logger
from .decorators import execution_time


s3_client = boto3.client('s3')


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
