from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Tuple, Dict

class ChatState(TypedDict):
    link: str
    ouput: str
    toos_info: List[Tuple[str,str]]

def separate_html_text_node(state: ChatState):
    pass

def search_related_news_node(state: ChatState):
    pass

def info_check_node(state: ChatState):
    pass

def final_answer_node(state: ChatState):
    pass

def graph(llm):
    builder = StateGraph(ChatState)

    builder.add_node("separate_html_text", separate_html_text_node)
    builder.add_node("search_related_news", search_related_news_node)
    builder.add_node("info_check", info_check_node)
    builder.add_node("final_answer", final_answer_node)
    builder.set_entry_point("separate_html_text")
    builder.add_edge("separate_html_text", "search_related_news")
    builder.add_edge("search_related_news", "info_check")
    builder.add_edge("info_check", "final_answer")

    return builder.compile()