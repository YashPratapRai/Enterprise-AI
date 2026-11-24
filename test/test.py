
import os
from dotenv import load_dotenv
from groq import Groq
from sentence_transformers import SentenceTransformer

load_dotenv()

# -----------------------------------
# Test 1: BGE Small Embeddings
# -----------------------------------

print("\nTesting BGE Embedding Model...")

embedding_model = SentenceTransformer(
    os.getenv(
        "BEDROCK_EMBED_MODEL",
        "BAAI/bge-small-en-v1.5"
    )
)

embedding = embedding_model.encode(
    "Hello Enterprise AI",
    normalize_embeddings=True
)

print("Embedding dimension:", len(embedding))
print("Embedding successful!")


# -----------------------------------
# Test 2: Groq Chat Model
# -----------------------------------

print("\nTesting Groq Chat Model...")

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

chat_response = client.chat.completions.create(
    model=os.getenv(
        "BEDROCK_CHAT_MODEL",
        "openai/gpt-oss-120b"
    ),
    messages=[
        {
            "role": "user",
            "content": "Explain RAG in one sentence."
        }
    ],
    temperature=0.1,
    max_tokens=200
)

print(
    "Groq Response:",
    chat_response.choices[0].message.content
)

print("\nAll model tests completed successfully!")
