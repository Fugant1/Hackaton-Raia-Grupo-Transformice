from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Tuple, Dict

class ChatState(TypedDict):
    post_text: str
    output: str
    toos_info: Dict
    score: float

def search_related_news_node(state: ChatState):
    print("search_related_news_node")

def info_check_node(state: ChatState, openai_api_key: str):
    #llm = ChatOpenAI(temperature=0, model="gpt-4", api_key=openai_api_key)
    print("info_check_node")

def final_answer_node(state: ChatState, openai_api_key: str):
    #llm = ChatOpenAI(temperature=0, model="gpt-4", api_key=openai_api_key)
    print("final_answer_node")

def graph(google_api_key = '', openai_api_key =  '') -> StateGraph[ChatState]:
    builder = StateGraph(ChatState)

    builder.add_node("search_related_news", search_related_news_node)
    builder.add_node("info_check", lambda state: info_check_node(state, openai_api_key))
    builder.add_node("final_answer", lambda state: final_answer_node(state, openai_api_key))
    builder.set_entry_point("search_related_news")
    builder.add_edge("search_related_news", "info_check")
    builder.add_edge("info_check", "final_answer")

    return builder.compile()