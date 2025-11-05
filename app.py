import streamlit as st
from backend import carregar_modelos_e_indice, obter_resposta_assistente
from leitor_pdf import extrair_texto_de_pdf, quebrar_texto_em_chunks, criar_indice_faiss_para_pdf

st.set_page_config(
    page_title="Veredictum",
    page_icon="⚖️",
    layout="centered"
)

model_emb, index_geral, model_gen, documentos_gerais = carregar_modelos_e_indice()

with st.sidebar:
    st.header("Análise de Documento")
    arquivo_pdf = st.file_uploader("Carregue seu PDF aqui", type="pdf")

    if arquivo_pdf is not None:
        if st.button("Analisar PDF"):
            with st.spinner("Processando o PDF... Isso pode levar um momento."):
                texto_pdf = extrair_texto_de_pdf(arquivo_pdf)
                chunks_pdf = quebrar_texto_em_chunks(texto_pdf)

                index_pdf, chunks_armazenados = criar_indice_faiss_para_pdf(chunks_pdf, model_emb)

                st.session_state.index_pdf = index_pdf
                st.session_state.chunks_pdf = chunks_armazenados
                st.session_state.pdf_carregado = True
                st.success("PDF processado! Agora você pode fazer perguntas sobre ele no chat.")

    if "pdf_carregado" in st.session_state and st.session_state.pdf_carregado:
        if st.button("Voltar para a Base Jurídica Geral"):
            st.session_state.pdf_carregado = False
            st.info("O assistente agora responderá com base na legislação geral.")

st.title("⚖️ - Veredictum")

if "pdf_carregado" in st.session_state and st.session_state.pdf_carregado:
    st.caption("Modo: Conversando com o PDF. As respostas serão baseadas no documento que você carregou.")
    modo_atual = "pdf"
else:
    st.caption("Modo: Base de Conhecimento Jurídica Geral. As respostas serão baseadas na legislação carregada.")
    modo_atual = "geral"

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant",
         "content": "Olá! Posso tirar suas dúvidas sobre Direito Digital ou analisar um documento PDF que você me enviar pela barra lateral."}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Digite sua dúvida aqui..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            if modo_atual == "pdf":
                index_ativo = st.session_state.index_pdf
                documentos_ativos = st.session_state.chunks_pdf
            else:
                index_ativo = index_geral
                documentos_ativos = documentos_gerais

            response = obter_resposta_assistente(prompt, model_emb, index_ativo, model_gen, documentos_ativos,
                                                 modo_atual)

        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})