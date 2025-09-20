from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Tuple, Dict
import json
import urllib.request

class ChatState(TypedDict):
    post_text: str
    output: str
    toos_info: Dict
    score: float

#def search_related_news_node(state: ChatState):
    # apikey = "API_KEY"
    # url = f"https://gnews.io/api/v4/search?q=example&lang=en&max=10&apikey={apikey}"

    # with urllib.request.urlopen(url) as response:
    #     data = json.loads(response.read().decode("utf-8"))
    #     articles = data["articles"]

    #     for i in range(len(articles)):
    #         print(f"Title: {articles[i]['title']}")
    #         print(f"Description: {articles[i]['description']}")
    #         # You can replace {property} below with any of the article properties returned by the API.
    #         # articles[i].{property}
    #         # print(f"{articles[i]['{property}']}")

    #         # Delete this line to display all the articles returned by the request. Currently only the first article is displayed.
    #         break
    #print("search_related_news_node")

def get_metrics_node(state: ChatState, openai_api_key: str):
    #llm = ChatOpenAI(temperature=0, model="gpt-4o-mini", api_key=openai_api_key)
    print("info_check_node")

def final_answer_node(state: ChatState, openai_api_key: str):
    #llm = ChatOpenAI(temperature=0, model="gpt-4o-mini", api_key=openai_api_key)
    print("final_answer_node")

def graph(google_api_key = '', openai_api_key =  '') -> StateGraph[ChatState]:
    builder = StateGraph(ChatState)

    #builder.add_node("search_related_news", search_related_news_node)
    builder.add_node("get_metrics", lambda state: get_metrics_node(state, openai_api_key))
    builder.add_node("final_answer", lambda state: final_answer_node(state, openai_api_key))
    #builder.set_entry_point("search_related_news")
    #builder.add_edge("search_related_news", "info_check")
    builder.set_entry_point("get_metrics")
    builder.add_edge("get_metrics", "final_answer")

    return builder.compile()