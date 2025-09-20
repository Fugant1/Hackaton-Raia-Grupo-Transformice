from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Tuple, Dict
import json

class ChatState(TypedDict):
    post_text: str
    output: str
    tools_info: Dict
    
def get_metrics_node(state: ChatState):
    new_state = state
    new_state["tools_info"]["Metricas"] = [
        {"key": "metric1", "description": "emocionalidade", "value": 0.9},
        {"key": "metric2", "description": "credibility", "value": 0.7},
        {"key": "metric3", "description": "bias", "value": 0.4}
    ]
    return new_state

def highlights_node(state: ChatState, openai_api_key: str):
    metrics = state['tools_info'].get("Metricas", [])
    #llm = ChatOpenAI(temperature=0, model="gpt-4o-mini", api_key=openai_api_key)
    llm = ChatGoogleGenerativeAI(temperature=0, model="gemini-2.5-flash-lite", api_key=openai_api_key)
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Você é um jornalista experiente que identifica pontos críticos em posts do Twitter baseado em métricas fornecidas."),
        ("user", """Retorne apenas os textos que são pontos críticos separados por '/', sem comentários.
        Twitter post: {post_text}
        Metricas: {metrics}.""")
    ])
    response = llm.invoke(prompt.format_messages(post_text=state['post_text'], metrics=json.dumps(metrics)))
    new_state = state
    new_state['tools_info']["Pontos_de_destaque"]=response.content.split('/')
    return new_state

def final_answer_node(state: ChatState, openai_api_key: str):
    metrics = state['tools_info'].get("Metricas", [])
    #llm = ChatOpenAI(temperature=0, model="gpt-4o-mini", api_key=openai_api_key)
    llm = ChatGoogleGenerativeAI(temperature=0.5, model="gemini-2.5-flash-lite", api_key=openai_api_key)
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Você é um jornalista experiente que sintetiza a credibilidade de posts no Twitter baseado em métricas fornecidas e trechos destacados considerados pontos críticos"),
        ("user", """Responda de forma resumida e objetiva
        Twitter post: {post_text}
        Métricas: {metrics}
        Pontos de destaque: {highlights}.""")
    ])
    response = llm.invoke(prompt.format_messages(post_text=state['post_text'], metrics=json.dumps(metrics), highlights=", ".join(state['tools_info'].get("Pontos_de_destaque", []))))
    new_state = state
    new_state['output'] = response.content
    return new_state

def graph(openai_api_key) -> StateGraph[ChatState]:
    builder = StateGraph(ChatState)

    builder.add_node("get_metrics", get_metrics_node)
    builder.add_node("highlights", lambda state: highlights_node(state, openai_api_key))
    builder.add_node("final_answer", lambda state: final_answer_node(state, openai_api_key))
    builder.set_entry_point("get_metrics")
    builder.add_edge("get_metrics", "highlights")
    builder.add_edge("highlights", "final_answer")

    return builder.compile()