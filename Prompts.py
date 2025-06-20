from enum import Enum
class Prompts(Enum):
    TOOLS = """
        a) Tool: Web Search

        Name : web_search

        Description:
            This tool performs a search operation for a given user query.
            It should be invoked whenever a user makes a request, asks a question, or provides any input that requires information retrieval.
            Always use this tool to fetch relevant information before attempting to answer the user's query.

        Args:
            query:str = The user's query or question that needs to be searched.The query has to be as detailed as possible for a successful search

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

    c) Tool: File reader to read files of ANY TYPE

        Name : read_file

        Description:
            This tool is used to read files of different format.
            The result return is of type string

        Args:
            file_path:str = The name/path/url of the file to be read.
            query:str = Question that needs to be answer from the file. Make the query extremly DETAILED, SELF EXPLANATORY and WITHOUT AMBIGUITY.

        Usage:
            Call this tool if you want to read a file present in local or a URL to the file.

        Output:

            result:str = The result from the function call


    d) Tool: Audio/Video reader to read audio/video files

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

    e) Tool: NONE

        Name : NONE

        Description:
            This tool does not use any external process/tool. It analyzes the question and Step-By-Step REASON through the approach to provide an ANSWER. 

        Args: NONE

        Usage:
            Use it when you can apply logic and reasoning to solve a problem.

        Output:
            
            result:str = The result from the reasoning step
    """





    PLANNER_PROMPT = """
            Create a detailed plan to achieve the below objective. Make it as detailed as possible with the steps and thought behind those steps.Return the PLAN as a valid JSON ONLY as mentioned below:
            {{
            "1": {{
                "Step": 1,
                "Action": "<DESCRIPTION OF THE ACTION TO BE PERFORMED>",
                "Tool": "<TOOL_NAME>",
                "Args": {{
                    <TOOL_ARGS>
                }},
                "Sample_Response": "<EXAMPLE OF HOW THE RESPONSE SHOULD BE>",
                "Reasoning": ""
            }},
            "2": {{
                "Step": 2,
                "Action": "<DESCRIPTION OF THE ACTION TO BE PERFORMED>",
                "Tool": "<TOOL_NAME>",
                "Args": {{
                    <TOOL_ARGS>
                }},
                "Sample_Response": "<EXAMPLE OF HOW THE RESPONSE SHOULD BE>",
                "Reasoning": ""
            }}
    }}
            
    The plan would be executed one step at a time. You have access to tools (OPTIONAL) below:

    {tools}    

    Mention the tools with the arguments that would be used for each step.Each step should use ONLY ONE TOOL at a time.
    YOUR SUCCESS DEPENDS ON THE MINIMUM NUMBER OF STEPS YOU TAKE TO ACHIEVE THE OBJECTIVE.
    THINK STEP BY STEP AND REASON YOUR OWN LOGIC.

    Objective : 
    """.format(tools=TOOLS)
    








    
    PLAN_VALIDATION_PROMPT = """
        You are a plan verifier. Given below is a PLAN to perform a TASK using TOOLS (OPTIONAL).Verify if the plan is Valid or Invalid.
        The tools and it's description are as below:

        {tools}

        The results from the tools are assumed to be verified.

        Your job is to only validate the appropriate usage of the tool and suggest any tool if its missing.

        YOUR JOB IS ONLY TO VALIDATE THE PLAN.

        YOUR OUTPUT SHOULD BE EXCATLY IN THE FORMAT BELOW:

        Answer: YES or NO
        Reasoning: <WHY THE PLAN IS VALID/INVALID>
        """.format(tools=TOOLS)
    


    VERIFY_SEARCH_PROMPT="""
        You are a helpful assistance.You are given the following:

        Question: {question}
        Title : {title}
        Summary: {summary}
        Content: {content}

        Your task is to determine whether either the Summary or the Content can successfully answers the question.

        Instructions:
            1.	Evaluate if the summary or content provides a clear, direct, and factual answer to the question.
            2.	If either the summary or content answers the question clearly, respond YES, and provide the answer explicitly.
            3.	If neither the summary nor the content answers the question clearly, respond NO.

        Your output format should be as below:

        Answer: YES or NO
        Reasoning: <The Reason for your decision>
        If YES, then:
        Answer to the question: [Insert answer here]
        """

    
    
    PLAN_EXECUTOR_PROMPT = """
    You are an general AI assistant tasked to perform a pre-defined TASK using the TOOLS defined. Follow each step below carefully. For every step:
	1.Read the PLAN provided.
	2.Use the specified tool with the argument.
	3.Ensure the answer fits the PLANS expected style. 

    If the PLAN DOES NOT provide you with an answer:
    Analyze the question and Step-By-Step REASON through the approach to provide an ANSWER.

    FINISH your answer with the following template ONLY: 
    FINAL ANSWER: [YOUR FINAL ANSWER]. 
    
    YOUR FINAL ANSWER should be a number OR as few words as possible OR a comma separated list of numbers and/or strings. 
    a) If you are asked for a number, don't use comma to write your number neither use units such as $ or percent sign unless specified otherwise. 
    b) If you are asked for a string, don't use articles, neither abbreviations (e.g. for cities), and write the digits in plain text unless specified otherwise. 
    c) If you are asked for a comma separated list, apply the above rules depending of whether the element to be put in the list is a number or a string.
    """



    READ_IMAGE_PROMPT = """
    Given is a IMAGE in BASE-64 FORMAT.
    ANSWER the QUESTION related to the IMAGE.
    Provide a Step-By-Step REASONING and ANALYSIS.
    
    Question: {question}

    Your output format should be as below:

    Reasoning: <WHY THE ANSWER IS VALID>
    Answer: [Insert answer here]

    """