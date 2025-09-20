from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Tuple, Dict
import json
import torch
from transformers import pipeline
import re

class AnalisadorDeEstilo:
    def __init__(self):
        """
        Inicializa o analisador com uma lista de palavras consideradas sensacionalistas.
        Esta lista é o coração da análise e pode ser facilmente customizada.
        """
        self.palavras_sensacionalistas = set([
            # Impacto / Choque
            "chocante","escândalo","imperdível","urgente","explosivo","bombástico","impactante",
            "revelação","alarmante","polêmico","escabroso","surpreendente","inacreditável",
            "assustador","aterrorizante","arrasador","devastador","trágico","indignante",
            "escandaloso","fatal","desesperador","apocalíptico","catastrófico","choque",
            "horrível","pavoroso","sinistro","terrível","desumano",

            # Intensidade / Emoção Forte
            "espantoso","extraordinário","abominável","surto","drástico","dramático",
            "enlouquecedor","tenebroso","macabro","sanguinário","horripilante","repugnante",
            "hediondo","incrível","fantástico","fenomenal","espetacular","arrasante",
            "urgência","alerta máximo","pânico","medonho","maldito","perigoso","devastação",
            "destruição","massacre","colapso","desastre","tragédia","fim do mundo","ultimato",
            "bomba","caos","explosão","golpe","mistério","reviravolta","conspiração",
            "segredo sombrio","choque total","tumulto","caótico","descontrole","panela de pressão",

            # Ameaça / Perigo
            "ameaçador","perturbador","insuportável","desolador","abrupto","escabrosidade",
            "furioso","intenso","violento","brutal","mortífero","letal","sangrento",
            "infernal","apavorante","espantamento","desespero","terror","medo extremo",
            "catástrofe","colapso total","queda livre","implosão","tempestade perfeita",

            # Fim do Mundo / Tragédias
            "fúria","apoteótico","inevitável","fatalidade","desgraça","tragicidade",
            "apocalipse","fim dos tempos","juízo final","grande tragédia","devastação total",
            "desmoronamento","aniquilação","aniquilador","arrasamento","pestilência",
            "pandemia","epidemia","contágio","pavor coletivo","pânico geral","alarme social"
        ])

    def analisar(self, texto):
        """
        Calcula um score de sensacionalismo de 0 a 10 e destaca os termos problemáticos.
        """
        # --- 1. Preparação do Texto ---
        palavras = re.findall(r'\b\w+\b', texto)
        num_palavras = len(palavras)
        if num_palavras == 0:
            return {"score_sensacionalismo": 0, "termos_destacados": []}

        termos_destacados = []
        score_bruto = 0

        # --- 2. Análise de Componentes ---

        # Componente A: Palavras em Maiúsculas
        palavras_maiusculas = [p for p in palavras if p.isupper() and len(p) > 2]
        ratio_maiusculas = len(palavras_maiusculas) / num_palavras
        score_bruto += ratio_maiusculas * 30 # Peso alto para maiúsculas
        for p in palavras_maiusculas:
            termos_destacados.append({"termo": p, "tipo": "Uso de Maiúsculas"})

        # Componente B: Pontuação Excessiva
        pontuacao_excessiva = re.findall(r'[!?]{2,}', texto) # Encontra '!!', '??', '?!', etc.
        num_exclamacoes_interrogacoes = len(re.findall(r'[!?]', texto))
        ratio_pontuacao = (num_exclamacoes_interrogacoes + len(pontuacao_excessiva)) / num_palavras
        score_bruto += ratio_pontuacao * 20 # Peso médio para pontuação
        
        # Componente C: Palavras Sensacionalistas
        palavras_encontradas = [p for p in palavras if p.lower() in self.palavras_sensacionalistas]
        ratio_sensacionalista = len(palavras_encontradas) / num_palavras
        score_bruto += ratio_sensacionalista * 50 # Peso muito alto para o vocabulário
        for p in palavras_encontradas:
            termos_destacados.append({"termo": p, "tipo": "Palavra Sensacionalista"})

        # --- 3. Normalização do Score ---
        # O score bruto é a soma ponderada dos ratios. Agora, limitamos a 10.
        score_final = min(10, score_bruto)

        return round(score_final, 2)


class AnalisadorDeTomEmocional:
    def __init__(self):
        """
        Inicializa o pipeline do modelo de classificação, configurando-o para usar a GPU se disponível.
        """
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Dispositivo selecionado: {self.device}")

        model_name = "tabularisai/multilingual-sentiment-analysis"
        print(f"Inicializando o pipeline com o modelo ({model_name})...")

        # O pipeline lida com o tokenizer e o modelo, enviando-os para o dispositivo correto.
        self.model_pipeline = pipeline(
            "text-classification",
            model=model_name,
            device=0 if self.device.type == "cuda" else -1  # 0 para primeira GPU, -1 para CPU
        )
        print("Pipeline do modelo carregado com sucesso.")

    def analisar(self, texto: str) -> str:
        """
        Realiza a análise de sentimento e retorna o label do sentimento traduzido para o português.

        Args:
            texto: A string de texto a ser analisada.

        Returns:
            Uma string com a classificação do sentimento em português.
        """
        # A chamada ao pipeline retorna o resultado em inglês.
        resultado_pipeline = self.model_pipeline(texto)[0]
        label_em_ingles = resultado_pipeline['label']

        # Dicionário para traduzir os labels de inglês para português.
        traducao_labels = {
            "Very Positive": "Muito Positivo",
            "Positive": "Positivo",
            "Neutral": "Neutro",
            "Negative": "Negativo",
            "Very Negative": "Muito Negativo"
        }

        # Busca a tradução no dicionário.
        # O .get() retorna o próprio label em inglês caso não encontre uma tradução.
        label_em_portugues = traducao_labels.get(label_em_ingles, label_em_ingles)

        return label_em_portugues

class ChatState(TypedDict):
    post_text: str
    output: str
    tools_info: Dict
    
def get_metrics_node(state: ChatState):
    analisador = AnalisadorDeTomEmocional()
    analisador_estilo = AnalisadorDeEstilo()
    texto = state['post_text']
    label1 = analisador.analisar(texto)
    label2 = analisador_estilo.analisar(texto)
    new_state = state
    new_state["tools_info"]["Metricas"] = [
        {"key": "metric1", "description": "emocionalidade", "value": label1},
        {"key": "metric2", "description": "sensacionalismo", "value": label2}
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