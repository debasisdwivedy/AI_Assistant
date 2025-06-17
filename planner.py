import sys
sys.path.append("/Volumes/MacintoshDrive/Midships/First_agent_template/AI_Assistant")

from utils.get_llm import get_llm
from langchain_core.prompts import PromptTemplate
import json


PROMPT="""
        Create a detailed plan to achieve the below objective. Make it as detailed as possible with the steps and thought behind those steps.Return the PLAN as a valid JSON ONLY as mentioned below:
        {{
        "1": {{
            "Step": 1,
            "Action": "<DESCRIPTION OF THE ACTION TO BE PERFORMED>",
            "Tool": "<TOOL_NAME>",
            "Args": {{
                <TOOL_ARGS>
            }},
            "Reasoning": ""
        }},
        "2": {{
            "Step": 2,
            "Action": "<DESCRIPTION OF THE ACTION TO BE PERFORMED>",
            "Tool": "<TOOL_NAME>",
            "Args": {{
                <TOOL_ARGS>
            }},
            "Reasoning": ""
        }}
}}
        
The plan would be executed one step at a time. You have access to tools below:

a) Tool: Web Search

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

        result:str = {{'0': {{'URL': 'https://example.com','Content': 'This is a sample example'}},
                       '1': {{'URL': 'https://xyz.com','Content': 'This is a sample example'}}
                     }}
                       
b) Tool: Python virtual environment to execute python code

    Name : python_execute

    Description:
        This tool is used to execute python code and return back the result.
        The result could be of any datatype including Exception string.
        ALWAYS PRINT THE FINAL RESULT.   

    Args:
        execute_code:str = The code that needs to be executed.
        install_pkg:list = The packages that needs to be installed to run the code successfully.

    Usage:
        Call this tool upon receiving a python code and return back the result as a string.

    Output:
        
        result:str = The result from the function call

c) Tool: File reader to read files of any type

    Name : read_file

    Description:
        This tool is used to read files of different format.
        The result return is of type string

    Args:
        file_path:str = The name/path/url of the file to be read.

    Usage:
        Call this tool if you want to read a file present in local or a URL to the file.

    Output:

        result:str = The result from the function call

d) Tool: Visit website to get the content

    Name : visit_website

    Description:
        This tool is used to visit a website and get its content in markdown format.
        The result return is of type string

    Args:
        url:str = The url of the site to visit.

    Usage:
        Call this tool if you need to get the content of a website.

    Output:

        result:str = The content of the website.

e) Tool: Audio/Video reader to read audio/video files

    Name : read_video

    Description:
        This tool is used to read audio/video files like (mp3,mp4,MOV etc) of different format.
        The result return is of type string

    Args:
        url:str = The url of the video file.

    Usage:
        Call this tool if you want to get the content of a audio/video file from a URL.

    Output:

        result:str = The result from the function call

Mention the tools with the arguments that would be used for each step.Each step should use ONLY ONE TOOL at a time.
YOUR SUCCESS DEPENDS ON THE MINIMUM NUMBER OF STEPS YOU TAKE TO ACHIEVE THE OBJECTIVE.
THINK STEP BY STEP AND REASON YOUR OWN LOGIC.

Objective : {question}
        """

llm = get_llm()

prompt_template = PromptTemplate.from_template(PROMPT)
prompt = prompt_template.invoke(
    {
    "question": '''
    Please solve the following crossword:
    
    |1|2|3|4|5|
    |6| | | | |
    |7| | | | |
    |8| | | | |
    |X|9| | | |
    
    I have indicated by numbers where the hints start, so you should replace numbers and spaces by the answers.
    And X denotes a black square that isn't to fill.
    ACROSS
    - 1 Wooden strips on a bed frame
    - 6 _ Minhaj, Peabody-winning comedian for "Patriot Act"
    - 7 Japanese city of 2.6+ million
    - 8 Stopwatch, e.g.
    - 9 Pain in the neck
    DOWN
    - 1 Quick drink of whiskey
    - 2 Eye procedure
    - 3 "Same here," in a three-word phrase
    - 4 Already occupied, as a seat
    - 5 Sarcastically critical commentary. Answer by concatenating the characters you choose to fill the crossword, in row-major order.
    '''
    }
)

resp = llm.invoke(prompt)
content = resp.content

start = content.find("{")
end = content.rfind("}")

if start != -1 and end != -1 and end > start:
    formatted_content = content[start:end+1]
    try:
        print(formatted_content)
        plan = json.loads(formatted_content)
        for step in plan:
            print("=========================")
            print(plan[step])
            print("=========================")
    except ValueError as e:
        raise ValueError("Unable to generate plan") from e
else:
    print("Invalid JSON")

