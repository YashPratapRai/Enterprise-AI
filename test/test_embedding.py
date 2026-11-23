
import boto3
import json
import os
from dotenv import load_dotenv

load_dotenv()

client = boto3.client(
    "bedrock-runtime",
    region_name="ap-south-1"
)

try:
    response = client.invoke_model(
        modelId="amazon.titan-embed-text-v2:0",
        body=json.dumps({
            "inputText": "Testing Amazon Bedrock embeddings",
            "dimensions": 1024,
            "normalize": True
        }),
        contentType="application/json",
        accept="application/json"
    )

    result = json.loads(response["body"].read())

    print("SUCCESS!")
    print("Embedding dimensions:", len(result["embedding"]))

except Exception as e:
    print("ERROR:", type(e).__name__)
    print("MESSAGE:", str(e))
