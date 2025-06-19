
from langchain_openai import ChatOpenAI
import os

def get_llm():
    if not os.getenv("MODEL"):
        from dotenv import load_dotenv
        load_dotenv()

    model = os.getenv("MODEL")
    api_key = os.getenv("OPENAI_API_KEY")
    llm = ChatOpenAI(
        model=model,
        api_key=api_key,
        )
    return llm
