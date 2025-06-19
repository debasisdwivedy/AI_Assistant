from typing import Literal
from PIL import Image
import io,json
from dotenv import load_dotenv
from argparse import ArgumentParser

from langgraph.graph import MessagesState
from langgraph.graph import StateGraph,START,END
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage, AIMessage, AnyMessage
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langchain.tools import Tool

from tools.code.code_agent import python_execute
from tools.web.search import web_search
from tools.file_ops.read_file import read_file
from tools.video_ops.read_video import read_video

from utils.get_llm import get_llm
from planner import get_plan,plan_status
from Prompts import Prompts

class State(MessagesState):
    query: str
    plan: str
    execution_status: bool
    plan_counter: int
    plan_messages: list
    verbose: bool


def planner(state:State):
    print("====================================IN PLANNER==============================================")
    state["plan"]=get_plan(state["query"],state["plan_messages"])
    state["plan_messages"].append(AIMessage(content=state["plan"]))
    state["plan_counter"] = state["plan_counter"] + 1
    return state


def validate_plan(state:State)->Literal["planner","plan_executor","__end__"]:
    print("====================================IN VALIDATE PLAN==============================================")
    if state["plan_counter"] > 5:
        return "__end__"
    status = plan_status(state["query"],state["plan"])
    message_status = status.split("\n")

    if state["verbose"]:
        print("=========VERIFICATION STATUS================")
        print(status)

    if len(message_status) > 1:
        state["plan_messages"].append(AIMessage(content=message_status[1]))
        if "Answer: NO" in status:
            AIMessage(content=message_status)
            return "planner"
    else:
        state["plan_messages"].append(AIMessage(content=status))
        if "Answer: NO" in status:
            AIMessage(content=status)
            return "planner"
    
    return "plan_executor"
    
def plan_executor(state:State):
    print("====================================IN EXECUTOR==============================================")
    llm = get_llm()
    

    if "plan" in state and state["plan"] and not state["execution_status"]:
        plan_str=state["plan"]
        if state["verbose"]:
            print("+++++++++++++++++++++++++++++PLAN+++++++++++++++++++++++++++++++++++++")
            plan = json.loads(plan_str)
            
            for step in plan:
                print("=========================")
                print(plan[step])
                print("=========================")

            print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

            
            state["plan"]="""
                ===================PLAN TO BE EXCUTED IN THE STEPS BELOW===================================
                        {PLAN}
                """.format(PLAN=plan_str)
            
        state["messages"]=add_messages(state["messages"],[SystemMessage(content=Prompts.PLAN_EXECUTOR_PROMPT)])
        state["messages"]=add_messages(state["messages"],[HumanMessage(content=state["query"])])
        state["messages"]=add_messages(state["messages"],[AIMessage(content=state["plan"])])
        state["execution_status"] = True
        state["query"]=""

    llm_with_tools = llm.bind_tools([web_search,python_execute,read_file,read_video])
    resp = llm_with_tools.invoke(state["messages"])
    # print("============RESPONSE=======================")
    # print(resp)
    state["messages"]=add_messages(state["messages"],[resp])
    return state

def main(task:str,verbose=False):
    builder = StateGraph(State)
    builder.add_node("planner",planner)
    builder.add_node("plan_executor",plan_executor)
    builder.add_node("tools", ToolNode([web_search,python_execute,read_file,read_video]))

    builder.add_edge(
        START,
        "planner"
    )

    builder.add_conditional_edges(
        "planner",
        validate_plan
    )
    builder.add_conditional_edges(
        "plan_executor",
        tools_condition
    )
    builder.add_edge("tools","plan_executor")

    mem = MemorySaver()
    agent = builder.compile(checkpointer=mem)

    # img = agent.get_graph().draw_mermaid_png()
    # image = (Image.open(io.BytesIO(img)))
    # image.show()


    config = {"configurable": {"thread_id": "1"}}


    resp = agent.invoke({"query":task,"plan_messages": [],"plan_counter": 0,"plan": "","execution_status": False,"verbose": verbose},config)
    if verbose:
        for m in resp['messages']:
            print(m)
            print("===================================")

    print("=====================FINAL RESPONSE=====================================")
    if resp["messages"]:
        print(resp["messages"][-1].content)
    else:
        print("FINAL ANSWER: Unable to perform the operation")

if __name__=="__main__":
    load_dotenv()
    parser = ArgumentParser(description="AI Assistant")
    #parser.add_argument("task",help="The task you want the agent to perform")
    parser.add_argument("--verbose",help="Verbose",action='store_true',default=False,required=False)
    args = parser.parse_args()
    VERBOSE = args.verbose
    #task = args.task
    task = '''
            Of the authors (First M. Last) that worked on the paper \"Pie Menus or Linear Menus, Which Is Better?\" in 2015, what was the title of the first paper authored by the one that had authored prior papers?
            '''
    main(task,verbose=VERBOSE)