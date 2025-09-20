from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Tuple, Dict

from html_scrapp import scrap

class ChatState(TypedDict):
    url: str
    output: str
    toos_info: Dict
    score: float

def separate_html_text_node(state: ChatState, google_api_key: str):
    url_info = scrap(state['url'])
    llm = ChatGoogleGenerativeAI(temperature=0, model="gemini-flash-lite-2.5", api_key=google_api_key)

def search_related_news_node(state: ChatState):
    pass

def info_check_node(state: ChatState, openai_api_key: str):
    llm = ChatOpenAI(temperature=0, model="gpt-4", api_key=openai_api_key)

def final_answer_node(state: ChatState, openai_api_key: str):
    llm = ChatOpenAI(temperature=0, model="gpt-4", api_key=openai_api_key)

def graph(google_api_key: str, openai_api_key:str) -> StateGraph[ChatState]:
    builder = StateGraph(ChatState)

    builder.add_node("separate_html_text", lambda state: separate_html_text_node(state, google_api_key))
    builder.add_node("search_related_news", search_related_news_node)
    builder.add_node("info_check", lambda state: info_check_node(state, openai_api_key))
    builder.add_node("final_answer", lambda state: final_answer_node(state, openai_api_key))
    builder.set_entry_point("separate_html_text")
    builder.add_edge("separate_html_text", "search_related_news")
    builder.add_edge("search_related_news", "info_check")
    builder.add_edge("info_check", "final_answer")

    return builder.compile()