from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Tuple, Dict
import json
from GoogleNews import GoogleNews

class ChatState(TypedDict):
    post_text: str
    output: str
    tools_info: Dict

# def search_related_news_node(state: ChatState, google_api_key: str):
#     llm = ChatGoogleGenerativeAI(temperature=0, model="gemini-2.5-flash-lite", api_key=google_api_key)
#     prompt = ChatPromptTemplate.from_messages([
#         ("system", "You are a helpful assistant that synthesizes information from posts on twitter."),
#         ("user", """Return only the synthesis, no comments.
#         Twitter post: {post_text}.""")
#     ])
#     response = llm.invoke(prompt.format_messages(post_text=state['post_text']))
#     googlenews = GoogleNews(lang='pt-br')
#     googlenews.search(response.content)

#     for entry in googlenews.result()[:5]:
#         print(entry['title'], "-", entry['link'])
#     new_state = state
#     new_state = state
#     new_state['tools_info'] = {
#     "similar_articles": [entry['link'] for entry in googlenews.result()[:5]]
#     }
#     return new_state
    #print("search_related_news_node")

def get_metrics_node(state: ChatState, openai_api_key: str):
    print("metrics_node")

def final_answer_node(state: ChatState, openai_api_key: str):
    metrics = state['tools_info'].get('metrics', {})
    #llm = ChatOpenAI(temperature=0, model="gpt-4o-mini", api_key=openai_api_key)
    print("final_answer_node")

def graph(openai_api_key) -> StateGraph[ChatState]:
    builder = StateGraph(ChatState)

    builder.add_node("get_metrics", lambda state: get_metrics_node(state, openai_api_key))
    builder.add_node("final_answer", lambda state: final_answer_node(state, openai_api_key))
    builder.set_entry_point("get_metrics")
    builder.add_edge("get_metrics", "final_answer")

    return builder.compile()