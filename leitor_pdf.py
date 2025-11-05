import fitz
import faiss
import numpy as np


def extrair_texto_de_pdf(arquivo_pdf):
    """
    Extrai o texto de um arquivo PDF carregado pelo Streamlit.
    """
    try:
        documento = fitz.open(stream=arquivo_pdf.read(), filetype="pdf")
        texto_completo = ""
        for pagina in documento:
            texto_completo += pagina.get_text()
        documento.close()
        return texto_completo
    except Exception as e:
        print(f"Erro ao extrair texto do PDF: {e}")
        return None


def quebrar_texto_em_chunks(texto, tamanho_chunk=1500, sobreposicao=150):
    """
    Quebra um texto longo em pedaços (chunks) com alguma sobreposição.
    """
    if not texto:
        return []

    chunks = []
    inicio = 0
    while inicio < len(texto):
        fim = inicio + tamanho_chunk
        chunks.append(texto[inicio:fim])
        inicio += tamanho_chunk - sobreposicao
    return chunks


def criar_indice_faiss_para_pdf(chunks, model_emb):
    """
    Cria embeddings para os chunks de texto e os armazena em um índice FAISS.
    """
    if not chunks:
        return None, None

    print(f"Criando embeddings para {len(chunks)} chunks do PDF...")
    embeddings_pdf = model_emb.encode(chunks)

    d = embeddings_pdf.shape[1]
    index = faiss.IndexFlatL2(d)
    index.add(np.array(embeddings_pdf).astype('float32'))

    print("Índice FAISS para o PDF criado com sucesso.")
    return index, chunks