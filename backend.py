# arquivo: backend.py

import os
import faiss
import json
import numpy as np
import streamlit as st
import google.generativeai as genai
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError("API Key do Google não encontrada. Verifique seu arquivo .env")
genai.configure(api_key=API_KEY)


def carregar_base_conhecimento(caminho_arquivo="legislacao_completa.json"):
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(f"Erro Crítico: O arquivo de dados '{caminho_arquivo}' não foi encontrado.")
        st.stop()
    except json.JSONDecodeError:
        st.error(f"Erro Crítico: O arquivo '{caminho_arquivo}' contém um erro de sintaxe JSON.")
        st.stop()


@st.cache_resource
def carregar_modelos_e_indice():
    """
    Carrega os modelos de IA e a base de conhecimento jurídica geral.
    Retorna os modelos e os dados da base geral para serem usados.
    """
    print("BACKEND: Carregando modelos e base de conhecimento geral...")

    model_emb = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

    documentos_gerais = carregar_base_conhecimento()
    if not documentos_gerais:
        st.error("A base de conhecimento geral está vazia.")
        st.stop()

    textos_puros = [doc["texto"] for doc in documentos_gerais]
    embeddings_documentos = model_emb.encode(textos_puros)

    d = embeddings_documentos.shape[1]
    index_geral = faiss.IndexFlatL2(d)
    index_geral.add(np.array(embeddings_documentos).astype('float32'))

    generation_config = {"temperature": 0.5, "top_p": 1, "top_k": 1, "max_output_tokens": 2048}
    model_gen = genai.GenerativeModel(model_name="gemini-2.5-flash", generation_config=generation_config)

    print("Modelos e base geral carregados com sucesso.")
    return model_emb, index_geral, model_gen, documentos_gerais


def obter_resposta_assistente(query_usuario, model_emb, index, model_gen, documentos, modo):
    """
    Função principal de RAG, agora adaptada para receber a base de dados ativa.
    """
    if not query_usuario or index is None:
        return "Desculpe, não consigo processar a pergunta. A base de dados não parece estar carregada."

    query_embedding = model_emb.encode([query_usuario])
    _, indices = index.search(np.array(query_embedding).astype('float32'), k=3)

    if modo == "pdf":
        contexto_encontrado = [documentos[i] for i in indices[0]]
        contexto_formatado = "\n\n---\n\n".join(contexto_encontrado)
        prompt_template = f"""
        Você é um assistente de análise de documentos. Responda à pergunta do usuário baseando-se estritamente nos trechos 
        do documento PDF fornecidos abaixo.
        Se a resposta não estiver nos trechos, afirme que a informação não foi encontrada no contexto fornecido.

        CONTEXTO DO PDF:
        ---
        {contexto_formatado}
        ---

        PERGUNTA DO USUÁRIO:
        {query_usuario}

        RESPOSTA:
        """
    else:
        contexto_encontrado = [documentos[i] for i in indices[0]]
        contexto_formatado = "\n\n".join(
            [f"Fonte: {doc.get('id', 'N/A')}\nTexto: {doc['texto']}" for doc in contexto_encontrado])
        prompt_template = f"""
        Você é um assistente virtual jurídico focado em somente dar possíveis leis existentes brasileiras, focado no âmbito cibernético 
        e da internet, diante um caso jurídico apresentado, se não for sobre um caso de fato, sinalize que você não foi criada para 
        responder sobre o assunto apresentado.

        Além disso, você analisa a pergunta do usuário. Se for uma pergunta rasa, responda de forma breve e direta, 
        informando somente o ano, número da lei e o nome da lei, porém se a pergunta for bem elaborada, amplie a resposta fornecida 
        com resumo da lei e seus aspectos, mas se limite a fornecer 3 leis, utilize emotes para que o usuário se sinta mais confortável 
        diante a resposta, busque usar os aspectos do processamento de linguagem natural (PLN).

        Sempre faça um adendo, na qual o usuário deve procurar profissionais capacitados do âmbito do direito, para afirmar se o uso 
        dessas leis são de fato coerentes com o caso apresentado e reforce que você é uma assistente virtual.
        CONTEXTO JURÍDICO:
        ---
        {contexto_formatado}
        ---

        PERGUNTA DO USUÁRIO:
        {query_usuario}

        RESPOSTA:
        """

    try:
        response = model_gen.generate_content(prompt_template)
        return response.text
    except Exception as e:
        return f"Ocorreu um erro ao contatar a IA: {e}"
