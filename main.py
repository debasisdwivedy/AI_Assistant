from langgraph.graph import MessagesState
from typing import Literal
from langgraph.graph import StateGraph,START,END
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage, AIMessage, AnyMessage

from tools.code.code_agent import python_execute
from tools.web.search import search
from tools.file_ops.read_file import read_file
from tools.web.visit_website import visit_website
from tools.video_ops.read_video import read_video

from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langchain.tools import Tool

from utils import get_llm
from PIL import Image
import io

class State(MessagesState):
    query: str
    search_results: list


def query_refiner(state:State):
    print("====================================IN QUERY REFINER==============================================")
    
    
    SYSTEM_PROMPT="""
        You are a english language teacher.Given the question please fix any spelling mistakes and typos.
        If unsure please DO NOTHING
        DO NOT MODIFY THE QUESTION. 
        IF THERE ARE NO MISTAKES RETURN BACK THE QUESTION AS IS AND IF THERE ARE ANY MISTAKES MODIFY THE QUESTION
        AND RETURN BACK ONLY THE CORRECTED QUESTION
        """
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=state["query"]),
        ]
    llm = get_llm.get_llm()
    resp = llm.invoke(messages)
    state["query"]=resp.content
    return state


def guardrails_node(state:State):
    print("====================================IN GUARDRAILS==============================================")
    
    SYSTEM_PROMPT="""
        You are a content moderator.Given the content please classify if the content is related to RELIGION and POLITICS.
        If the content is related to RELIGION and POLITICS and is OFFENSIVE respond with the string 'failure' else respond with the string 'success'.
        It needs to be a fun party without conflicts related to beliefs and ideals
        DO NOT RESPOND WITH ANYTHING APART FROM 'failure' OR 'success'.
        """
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=state["query"]),
        ]
    llm = get_llm.get_llm()
    resp = llm.invoke(messages)
    state["status_guardrail"]=resp.content

    if resp.content == "failure":
        state["messages"] = add_messages(state["messages"],["Unable to answer question related to RELIGION and POLITICS "])
    
    return state

def validate_guardrails(state:State)->Literal["__end__","event_planner"]:
    print("====================================IN VALIDATE GUARDRAIL==============================================")
    if state["status_guardrail"] == "failure":
        return "__end__"
    return "event_planner"
    
def event_planner(state:State):
    print("====================================IN THE EVENT PLANNER==============================================")
    SYSTEM_PROMPT="""
        You are a helpful assistance named Alfred. Your job is to organize and manage a gala event.
        You need to provide information about the party, including the menu, the guests, the schedule, weather forecasts, and much more!
        """
    llm = get_llm.get_llm()

    if "query" in state and state["query"]:
        state["messages"]=add_messages(state["messages"],[SystemMessage(content=SYSTEM_PROMPT)])
        state["messages"]=add_messages(state["messages"],[HumanMessage(content=state["query"])])
        state["query"]=""

    llm_with_tools = llm.bind_tools([search,weather])
    resp = llm_with_tools.invoke(state["messages"])
    state["messages"]=add_messages(state["messages"],[resp])
    return state


builder = StateGraph(State)
builder.add_node("query_refiner",query_refiner)
builder.add_node("guardrail",guardrails_node)
builder.add_node("event_planner",event_planner)
builder.add_node("tools", ToolNode([search,weather]))

builder.add_edge(
    START,
    "query_refiner"
)

builder.add_edge(
    "query_refiner",
    "guardrail"
)

builder.add_conditional_edges(
    "guardrail",
    validate_guardrails
)
builder.add_conditional_edges(
    "event_planner",
    tools_condition
)
builder.add_edge("tools","event_planner")

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