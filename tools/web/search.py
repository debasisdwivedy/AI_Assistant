import sys
sys.path.append("/Volumes/MacintoshDrive/Midships/First_agent_template/AI_Assistant")

import regex
from utils.get_llm import get_llm
from langchain_core.prompts import PromptTemplate
from visit_website import visit_website


PROMPT="""
        You are a helpful assistance.You are given the following:

        Question: {question}
        Title : {title}
        Summary: {summary}
        Content: {content}

        Your task is to determine whether either the summary or the full content successfully answers the question.

        Instructions:
            1.	Evaluate if the summary or content provides a clear, direct, and factual answer to the question.
            2.	If either the summary or content answers the question clearly, respond YES, and provide the answer explicitly.
            3.	If neither the summary nor the content answers the question clearly, respond NO.

        Your output format should be as below:

        Answer: YES or NO
        If YES, then:
        Answer to the question: [Insert answer here]
        """


def search(query:str,max_results:int):
    __duck_duck_go_search__(query,max_results)
    __google__search__(query,max_results)

def __duck_duck_go_search__(query:str,max_results:int):
    try:
        from duckduckgo_search import DDGS
        ddgs = DDGS(verify=False,timeout=5)
        llm = get_llm()
        results = ddgs.text(query, safesearch='off',max_results=max_results)
        urls = []
        for result in results:
            prompt_template = PromptTemplate.from_template(PROMPT)
            prompt = prompt_template.invoke(
                {
                    "question": query,
                    "title": result["title"],
                    "summary": result["body"],
                    "content": visit_website([result["href"]])

                }
                )
            #print(prompt.to_messages())
            resp = llm.invoke(prompt)
            if "Answer: YES" in resp.content:
                # Extract everything after 'Answer to the question:'
                match = regex.search(r'Answer to the question:\s*(.*)', resp.content,timeout=10)
                if match:
                    answer = match.group(1)
                    print("================================")
                    print(result["href"])
                    print("================================")
                    print(answer)
                

    except ImportError as e:
        raise ImportError("You must install package `duckduckgo_search` to run this tool: for instance run `pip install duckduckgo-search`.") from e
    

def __google__search__(query:str,max_results:int):
    try:
        from googlesearch import search
    except ImportError as e:
        raise ImportError("You must install package `googlesearch-python` to run this tool: for instance run `pip install googlesearch-python`.") from e
    llm = get_llm()
    for result in search(query, num_results=max_results,unique=True,safe=None,advanced=True,ssl_verify=True):
        prompt_template = PromptTemplate.from_template(PROMPT)
        prompt = prompt_template.invoke(
            {
                "question": query,
                "title": result.title,
                "summary": result.description,
                "content": visit_website([result.url])

            }
            )
        #print(prompt.to_messages())
        resp = llm.invoke(prompt)
        if "Answer: YES" in resp.content:
            # Extract everything after 'Answer to the question:'
            match = regex.search(r'Answer to the question:\s*(.*)', resp.content,timeout=10)
            if match:
                answer = match.group(1)
                print("================================")
                print(result.url)
                print("================================")
                print(answer)


query = "What was the actual enrollment count of the clinical trial on H. pylori in acne vulgaris patients from Jan-May 2018 as listed on the NIH website?"
search(query,20)