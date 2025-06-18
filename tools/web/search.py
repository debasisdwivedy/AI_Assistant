import regex,os,json

import sys
sys.path.append(os.getcwd())

from utils.get_llm import get_llm
from langchain_core.prompts import PromptTemplate
from tools.web.visit_website import visit_website
from Prompts import Prompts

def web_search(query:str,max_results:int=10,verbose:bool = False)->str:
    """
    Tool: Web Search

        Name : web_search

        Description:
            This tool performs a search operation for a given user query.
            It should be invoked whenever a user makes a request, asks a question, or provides any input that requires information retrieval.
            Always use this tool to fetch relevant information before attempting to answer the user's query.

        Args:
            query:str = The user's query or question that needs to be searched.

        Usage:
            Call this tool immediately upon receiving a user query to ensure that the LLM has the most accurate and updated context for generating a response.

        Output:
            A dictionary of results as below:

            result:str = {{'<URL1>': <ANSWER1>,
                        '<URL2>': <ANSWER2>,
                        }}
    
    """

    duck_duck_go_search_results={}
    google_search_results = {}
    try:
        duck_duck_go_search_results = __duck_duck_go_search__(query,max_results,verbose)
    except Exception as e:
        print(f"Unable to search using Duck Duck GO {e}")
    try:
       google_search_results =  __google__search__(query,max_results,verbose)
    except Exception as e:
        print(f"Unable to search using Google Search {e}")
    
    final_result = duck_duck_go_search_results | google_search_results

    if verbose:
        print(final_result)

    return json.dumps(final_result)

def __duck_duck_go_search__(query:str,max_results:int,verbose:bool):
    search_results = {}
    try:
        from duckduckgo_search import DDGS
        ddgs = DDGS(verify=False,timeout=5)
        llm = get_llm()
        results = ddgs.text(query, safesearch='off',max_results=max_results)
        for result in results:
            prompt_template = PromptTemplate.from_template(Prompts.SEARCH_PROMPT.value)
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
                    if verbose:
                        print("+++++++++++++++++++++++++++++++++++++++++++++++++++")
                        print(result["href"])
                        print("\n")
                        print(answer)
                        print("+++++++++++++++++++++++++++++++++++++++++++++++++++")
                    search_results[result["href"]]=answer
                
    except ImportError as e:
        raise ImportError("You must install package `duckduckgo_search` to run this tool: for instance run `pip install duckduckgo-search`.") from e
    
    return search_results
    

def __google__search__(query:str,max_results:int,verbose:bool):
    search_results = {}
    try:
        from googlesearch import search
        llm = get_llm()
        for result in search(query, num_results=max_results,unique=True,safe=None,advanced=True,ssl_verify=True):
            prompt_template = PromptTemplate.from_template(Prompts.SEARCH_PROMPT.value)
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
                    if verbose:
                        print("+++++++++++++++++++++++++++++++++++++++++++++++++++")
                        print(result.url)
                        print("\n")
                        print(answer)
                        print("+++++++++++++++++++++++++++++++++++++++++++++++++++")
                    search_results[result.url]=answer
    except ImportError as e:
        raise ImportError("You must install package `googlesearch-python` to run this tool: for instance run `pip install googlesearch-python`.") from e
    
    return search_results


if __name__ == "__main__":
    query = "Pain in the neck crossword clue"
    web_search(query,20)