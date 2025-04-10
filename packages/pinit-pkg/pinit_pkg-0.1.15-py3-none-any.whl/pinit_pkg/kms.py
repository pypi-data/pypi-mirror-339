import boto3

from loguru import logger

from .decorators import execution_time


kms_client = boto3.client('kms')

@execution_time
def kms_new_key(alias: str) -> str:
    """Create a new asymmetric KMS key for digital signatures.

    Args:
        alias (str): The alias name for the key. Will be prefixed with 'alias/'.

    Returns:
        str: The key ID of the created KMS key
    """

    # Create the KMS key
    try:
        response = kms_client.create_key(
            Description=f'Asymmetric signing key for {alias}',
            KeyUsage='SIGN_VERIFY',
            CustomerMasterKeySpec='RSA_4096',
            Origin='AWS_KMS',
            Tags=[{
                'TagKey': 'Purpose',
                'TagValue': 'DigitalSignature'
            }]
        )

        key_id = response['KeyMetadata']['KeyId']

        # Create an alias for the key
        kms_client.create_alias(
            AliasName=f'alias/{alias}',
            TargetKeyId=key_id
        )

        return key_id
    except Exception as e:
        logger.error(f"Error creating KMS key with alias {alias}: {e}")
        raise
