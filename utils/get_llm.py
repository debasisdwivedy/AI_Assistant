
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

def get_llm():
    model = load_dotenv("MODEL")
    api_key = load_dotenv("OPENAI_API_KEY")
    llm = ChatOpenAI(
        model=model,
        api_key=api_key,
        )
    return llm
