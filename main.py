from typing import Literal
from PIL import Image
import io

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
from tools.web.visit_website import visit_website
from tools.video_ops.read_video import read_video

from utils.get_llm import get_llm
from planner import get_plan,plan_status

class State(MessagesState):
    query: str
    plan: str
    search_results: list


def planner(state:State):
    print("====================================IN PLANNER==============================================")
    state["plan"]=get_plan()
    return state


def validate_plan(state:State)->Literal["__end__","plan_executor"]:
    print("====================================IN VALIDATE PLAN==============================================")
    status = plan_status(state["plan"])

    if status == "failure":
        return "__end__"
    return "plan_executor"
    
def plan_executor(state:State):
    print("====================================IN EXECUTOR==============================================")
    SYSTEM_PROMPT="""
        You are a helpful assistance named Alfred. Your job is to organize and manage a gala event.
        You need to provide information about the party, including the menu, the guests, the schedule, weather forecasts, and much more!
        """
    llm = get_llm()

    if "plan" in state and state["plan"]:
        state["messages"]=add_messages(state["messages"],[SystemMessage(content=SYSTEM_PROMPT)])
        state["messages"]=add_messages(state["messages"],[AIMessage(content=state["plan"])])
        state["query"]=""

    llm_with_tools = llm.bind_tools([web_search,python_execute,read_file,visit_website,read_video])
    resp = llm_with_tools.invoke(state["messages"])
    state["messages"]=add_messages(state["messages"],[resp])
    return state


builder = StateGraph(State)
builder.add_node("planner",planner)
builder.add_node("plan_executor",plan_executor)
builder.add_node("tools", ToolNode([web_search,python_execute,read_file,visit_website,read_video]))

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

img = agent.get_graph().draw_mermaid_png()
image = (Image.open(io.BytesIO(img)))
image.show()


# config = {"configurable": {"thread_id": "1"}}

# resp = agent.invoke({"query":"What was the actual enrollment count of the clinical trial on H. pylori in acne vulgaris patients from Jan-May 2018 as listed on the NIH website?"},config)
# print(resp["messages"][-1].content)
# for m in resp['messages']:
#     print(m)
#     print("===================================")