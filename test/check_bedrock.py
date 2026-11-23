
import os
import boto3
import json
from dotenv import load_dotenv

load_dotenv()

client = boto3.client(
    "bedrock",
    region_name=os.getenv("AWS_REGION"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)

try:
    response = client.get_foundation_model_availability(
        modelId="amazon.titan-embed-text-v2:0"
    )

    print(json.dumps(response, indent=4, default=str))

except Exception as e:
    print(type(e).__name__, ":", str(e))
