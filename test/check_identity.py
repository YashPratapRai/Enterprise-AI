import os
import boto3
from dotenv import load_dotenv

load_dotenv()

client = boto3.client(
    "sts",
    region_name=os.getenv("AWS_REGION"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)

identity = client.get_caller_identity()

print("AWS Account ID:", identity["Account"])
print("IAM User/Role:", identity["Arn"])
print("User ID:", identity["UserId"])