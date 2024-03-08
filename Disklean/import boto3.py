import boto3
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Add your SNS topic ARN
SNS_TOPIC_ARN = "arn:aws:sns:your-region:your-account-id:your-sns-topic"

def getstsobject(acctid):
    sts_connection = boto3.client('sts')
    sub_acct = sts_connection.assume_role(
        RoleArn="arn:aws:iam::{}:role/OrganizationAccountAccessRole".format(acctid),
        RoleSessionName="enableconfig"
    )
    return sub_acct

def publish_to_sns(account_id):
    sns_client = boto3.client('sns')
    message = f"New AWS account created: {account_id}"
    
    sns_client.publish(
        TopicArn=SNS_TOPIC_ARN,
        Message=message,
        Subject="New AWS Account Created",
    )

# Rest of your existing code...

def lambda_handler(event, context):
    accountId = str(event['createAccountStatus']['accountId'])
    
    sts = getstsobject(accountId)

    # Existing code...

    try:
        # Existing code...

        # Notify the distribution list via SNS
        publish_to_sns(accountId)

    except boto3.exceptions.Boto3Error as e:
        logger.error(e)
        exit(1)
