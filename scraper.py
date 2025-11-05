import requests
from bs4 import BeautifulSoup
import json
import re

ALVOS_LEGISLACAO = [
    {
        "nome_lei": "LGPD",
        "url": "http://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm"
    },
    {
        "nome_lei": "Marco Civil da Internet",
        "url": "http://www.planalto.gov.br/ccivil_03/_ato2011-2014/2014/lei/l12965.htm"
    },
    {
        "nome_lei": "Lei de Direitos Autorais",
        "url": "http://www.planalto.gov.br/ccivil_03/leis/l9610.htm"
    },
    {
        "nome_lei": "Código Penal",
        "url": "https://www.planalto.gov.br/ccivil_03/decreto-lei/del2848.htm"
    }
]


def extrair_dados_de_url(nome_lei, url):
    """
    Função genérica que acessa UMA URL, extrai os artigos E o texto completo da lei.
    Retorna uma tupla: (objeto_lei_completa, lista_de_artigos_individuais)
    """
    print(f"\n--- Iniciando scraping para: {nome_lei} ---")
    print(f"URL: {url}")

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        response.encoding = 'utf-8'

        soup = BeautifulSoup(response.text, 'html.parser')
        paragrafos = soup.find_all('p')

        lista_artigos_individuais = []
        textos_para_lei_completa = []

        for p in paragrafos:
            texto_paragrafo = p.get_text(strip=True)

            if len(texto_paragrafo) > 15 and (
                    texto_paragrafo.startswith('Art.') or texto_paragrafo.startswith('§') or texto_paragrafo.startswith(
                    'LEI Nº')):

                textos_para_lei_completa.append(texto_paragrafo)

                id_match = re.match(r'^(Art\.\s*\d+[º°]?[A-Z]?)', texto_paragrafo)
                if id_match:
                    id_limpo = id_match.group(1).replace('.', '').replace('º', '').replace('°', '').strip()
                    id_final = f"{nome_lei} - {id_limpo}"
                else:
                    id_final = f"{nome_lei} - {texto_paragrafo[:20]}..."

                artigo_obj = {
                    "id": id_final,
                    "lei": nome_lei,
                    "tipo": "Artigo",
                    "texto": texto_paragrafo
                }
                lista_artigos_individuais.append(artigo_obj)

        if not lista_artigos_individuais:
            print(f"AVISO: Nenhum artigo individual encontrado para {nome_lei}.")
            return None, None

        # 3. CRIA O OBJETO DA LEI COMPLETA
        texto_completo = "\n\n".join(textos_para_lei_completa)
        objeto_lei_completa = {
            "id": nome_lei,
            "lei": nome_lei,
            "tipo": "Lei Completa",
            "texto": texto_completo
        }

        print(f"Sucesso! {len(lista_artigos_individuais)} artigos/parágrafos e 1 lei completa extraídos de {nome_lei}.")
        return objeto_lei_completa, lista_artigos_individuais

    except requests.exceptions.RequestException as e:
        print(f"ERRO ao acessar a página {nome_lei}: {e}")
        return None, None


def orquestrar_scraping(lista_de_alvos):
    """
    Orquestra o processo de scraping, junta todos os resultados
    (leis completas e artigos individuais) e salva em um único arquivo JSON.
    """
    base_de_dados_completa = []

    for alvo in lista_de_alvos:
        nome_lei = alvo["nome_lei"]
        url = alvo["url"]

        lei_completa, artigos_da_lei = extrair_dados_de_url(nome_lei, url)

        if lei_completa and artigos_da_lei:
            base_de_dados_completa.append(lei_completa)
            base_de_dados_completa.extend(artigos_da_lei)

    if not base_de_dados_completa:
        print("\nNenhum dado foi extraído. Verifique os erros acima.")
        return

    nome_arquivo = 'legislacao_completa.json'
    with open(nome_arquivo, 'w', encoding='utf-8') as f:
        json.dump(base_de_dados_completa, f, indent=4, ensure_ascii=False)

    print(f"\n--- PROCESSO FINALIZADO ---")
    print(f"Base de dados unificada salva com sucesso em '{nome_arquivo}'!")
    print(f"Total de objetos na base de dados: {len(base_de_dados_completa)}")


if __name__ == "__main__":
    orquestrar_scraping(ALVOS_LEGISLACAO)