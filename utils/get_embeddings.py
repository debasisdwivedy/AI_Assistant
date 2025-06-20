
from langchain_openai import OpenAIEmbeddings
import os

def get_embedding():
    if not os.getenv("EMBEDDING_MODEL"):
        from dotenv import load_dotenv
        load_dotenv()

    model = os.getenv("EMBEDDING_MODEL")
    return OpenAIEmbeddings(model=model)
