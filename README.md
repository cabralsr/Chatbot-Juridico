## 🧠 Sobre o Projeto

Este projeto foi desenvolvido em contexto **acadêmico** por estudantes da **Universidade Anhembi Morumbi – Unidade Mooca**, dos cursos de **Sistemas de Informação** e **Direito**, com o objetivo de promover maior **acessibilidade jurídica** ao cidadão brasileiro.

Trata-se de um **chatbot jurídico** que utiliza a **API Gemini** para interpretar e responder dúvidas com base em leis brasileiras, aplicando os princípios do **Visual Law** para tornar o conteúdo mais claro, visual e compreensível.

### 📚 Funcionalidades

- Consulta automatizada às leis diretamente do site oficial do Planalto.
- Leitura e interpretação de documentos em PDF para fins de **análise e estudo**.
- Interface acessível e pensada para facilitar o entendimento jurídico por qualquer cidadão.

> ⚠️ **Aviso Importante:** Este sistema tem caráter **educacional e de apoio**. Ele **não substitui a orientação de profissionais da área jurídica**. Para decisões legais concretas, é essencial consultar um advogado ou especialista qualificado.

---

## ⚙️ Configuração Inicial

Para o melhor funcionamento do projeto, crie um arquivo `.env` na raiz e adicione a seguinte linha:

```env
GOOGLE_API_KEY="SUA_CHAVE_API"
```

> 🔐 **Importante:** Troque `"SUA_CHAVE_API"` pela chave gerada no https://aistudio.google.com/api-keys

---

## 🚀 Execução

Após configurar o `.env`, execute o arquivo `scraper.py`. Ele fará a leitura dos links diretamente do site do Planalto, acessando conteúdos relacionados às seguintes legislações:

- 📜 [Lei Geral de Proteção de Dados Pessoais (LGPD) – Lei nº 13.709/2018](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm)  
- 🌐 [Marco Civil da Internet – Lei nº 12.965/2014](https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2014/lei/l12965.htm)  
- 🎨 [Lei de Direitos Autorais – Lei nº 9.610/1998](https://www.planalto.gov.br/ccivil_03/Leis/L9610.htm)  
- ⚖️ [Código Penal – Decreto-Lei nº 2.848/1940](https://www.planalto.gov.br/ccivil_03/decreto-lei/del2848compilado.htm)

---

## 👥 Idealizadores do Projeto

Este projeto foi desenvolvido por estudantes dos cursos de **Sistemas de Informação** e **Direito**, com o objetivo de facilitar o acesso e a análise de legislações brasileiras por meio de tecnologias de IA.

| Nome                             | Curso                 |
|----------------------------------|------------------------|
| Camila Marcely Franzoso          | Direito                |
| Davi Casemiro Silva              | Direito                |
| Eduardo Moraes                   | Sistemas de Informação |
| Elton Lopes de Menezes           | Sistemas de Informação |
| Flávio Tonelotto                 | Direito                |
| Guilherme Albuquerque Duarte     | Sistemas de Informação |
| Guilherme Cabral Mendes Mariano | Sistemas de Informação |
| Julia Teixeira                   | Direito                |
| Nicolas Ribeiro de Holanda       | Sistemas de Informação |
