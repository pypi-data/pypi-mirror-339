import asyncio
from typing import Literal, Tuple, Iterable
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph, MessagesState
from langchain_core.messages import ToolMessage, AIMessage

from langgraph.prebuilt import ToolNode
from langchain_core.tools import tool
from lightrag import LightRAG, QueryParam
from lightrag.llm.openai import openai_embed, gpt_4o_mini_complete

WORKING_DIR = "./graphrag_index"
async def initialize_rag():
    rag = LightRAG(
        working_dir=WORKING_DIR,
        embedding_func=openai_embed,
        llm_model_func=gpt_4o_mini_complete
    )

    await rag.initialize_storages()
    return rag

rag = asyncio.run(initialize_rag())

@tool
def lightrag_query(query: str) -> Tuple[Iterable[str], str]:
    """
    You are a legal assistant. Query is the direct user question.
    Copy user question directly to this query. Do not try to make any change.",
    You help user to understand the document materials. 
    Do not try to answer any question outside of the documents what are indexed to the Knowledge Base.
    """

    # TODO: merge these two query, also add kg_context
    references: str = rag.query(
        query, 
        param=QueryParam(
            mode="mix", 
            only_need_context=True),   
        )["vector_context"] # type: ignore
    
    response =  rag.query(
        query, 
        param=QueryParam(mode="mix")
    )
    return (response, references)

tools = [lightrag_query]
tool_node = ToolNode(tools)
model = ChatOpenAI(model="gpt-4o-mini", temperature=0).bind_tools(tools)


# Define the function that determines whether to continue or not
def should_continue(state: MessagesState) -> Literal["tools", END]: # type: ignore
    messages = state['messages']
    last_message = messages[-1]
    # If the LLM makes a tool call, then we route to the "tools" node
    if last_message.tool_calls:
        return "tools"
    # Otherwise, we stop (reply to the user)
    return END


# Define the function that calls the model
def call_model(state: MessagesState):
    messages = state['messages']
    last_message = messages[-1]
    if isinstance(last_message, ToolMessage):
        # rag_resp, reference = last_message.content
        response = AIMessage(last_message.content)
    else:
        response = model.invoke(messages)
    
    # We return a list, because this will get added to the existing list
    return {"messages": [response]}


def create_graph():
    # Define a new graph
    workflow = StateGraph(MessagesState)

    # Define the two nodes we will cycle between
    workflow.add_node("legal_doc", call_model)
    workflow.add_node("tools", tool_node)

    # Set the entrypoint as `agent`
    # This means that this node is the first one called
    workflow.add_edge(START, "legal_doc")

    # We now add a conditional edge
    workflow.add_conditional_edges(
        # First, we define the start node. We use `agent`.
        # This means these are the edges taken after the `agent` node is called.
        "legal_doc",
        # Next, we pass in the function that will determine which node is called next.
        should_continue,
    )

    # We now add a normal edge from `tools` to `agent`.
    # This means that after `tools` is called, `agent` node is called next.
    workflow.add_edge("tools", 'legal_doc')

    # Initialize memory to persist state between graph runs
    checkpointer = MemorySaver()

    # Finally, we compile it!
    # This compiles it into a LangChain Runnable,
    # meaning you can use it as you would any other runnable.
    # Note that we're (optionally) passing the memory when compiling the graph
    app = workflow.compile(checkpointer=checkpointer)
    return app

graph = create_graph()