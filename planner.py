import json
from json.decoder import JSONDecodeError

from langchain_core.prompts import PromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage, AIMessage, AnyMessage

from utils.get_llm import get_llm
from Prompts import Prompts

def get_plan(task:str,messages:list)->str:
    llm = get_llm()
    
    if messages is None or len(messages) <= 0:
        messages.append(SystemMessage(content=Prompts.PLANNER_PROMPT.value))
        messages.append(HumanMessage(content=task))

    # prompt_template = PromptTemplate.from_template(Prompts.PLANNER_PROMPT.value)
    # prompt = prompt_template.invoke(
    #     {
    #     "question": {task}
    #     }
    # )
    # print(prompt)
    

    resp = llm.invoke(messages)
    content = resp.content

    start = content.find("{")
    end = content.rfind("}")

    if start != -1 and end != -1 and end > start:
        formatted_content = content[start:end+1]
        try:
            plan = json.loads(formatted_content)
            return formatted_content
        except JSONDecodeError as e:
            #raise ValueError("Unable to generate plan") from e
            return f"{'1':{'STATUS': 'NOT ABLE TO GENERATE A PLAN. GOT INVALID JSON AS RESPONSE.'}}"
    else:
        print("Invalid JSON")
        return f"{'1':{'STATUS': 'NOT ABLE TO GENERATE A PLAN. PLEASE TRY AGAIN LATER!!!'}}"
    

def plan_status(task:str,plan:str)->str:
    messages = [
        SystemMessage(content=Prompts.PLAN_VALIDATION_PROMPT.value),
        AIMessage(content=task),
        AIMessage(content=plan),
        ]
    llm = get_llm()
    resp = llm.invoke(messages)
    
    return resp.content

if __name__ == "__main__":

    task = '''
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
        - 5 Sarcastically critical commentary. 
        Answer by concatenating the characters you choose to fill the crossword, in row-major order.
        '''
    messages = []
    i = 0
    while True:
        i += 1
        plan_str = get_plan(task,messages)
        #print(plan_str)
        messages.append(AIMessage(content=plan_str))
        plan = json.loads(plan_str)
        
        for step in plan:
            print("=========================")
            print(plan[step])
            print("=========================")
        
        status = plan_status(task,plan_str)
        print("=========VERIFICATION STATUS================")
        print(status)
        messages.append(AIMessage(content=status.split("\n")[1]))

        if i > 5:
            break


