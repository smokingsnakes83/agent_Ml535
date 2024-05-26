import pandas as pd
import numpy as np
import google.generativeai as genai
import textwrap
import streamlit as st
import time
import random

# Used to securely store your API key
#from google.colab import userdata

from IPython.display import Markdown
from IPython.display import display


def to_markdown(text):
    text = text.replace("•", "  *")
    return Markdown(textwrap.indent(text, "> ", predicate=lambda _: True))


# Obtém a chave de API a partir dos dados do usuário
#API_KEY = userdata.get("API_KEY")
API_KEY = 'AIzaSyAed_zI7Kg2_6wrNuXmkFb1lAN85qEVV3g'
# Configura a biblioteca genai com a chave de API obtida
genai.configure(api_key=API_KEY)  # Substitua pela sua API_KEY

# Carrega o arquivo CSV em um dataframe pandas
df = pd.read_csv('documents.csv')
# df

# **Model**

# Definindo o modelo na variável model
embed_model = "models/embedding-001"

# **Função que Gera Embeddings para os Documentos**


def embed_doc(title, content):
    """
    Gera embeddings para documentos usando o modelo especificado.

    Args:
        title: O título do documento.
        content: O corpo do conteúdopdo documento.

    Returns:
        Um vetor de embedding representando o documento.
    """

    return genai.embed_content(
        model=embed_model, 
        content=content, 
        task_type="retrieval_document", 
        title=title)["embedding"]


# Aplica a função embed_doc a cada linha do dataframe
df["Embeddings"] = df.apply(lambda row: embed_doc(row["Title"], row["Content"]), axis=1)

# Exibe o dataframe com a nova coluna 'Embeddings'
# df

# **Função que gera embeddings das consultas**


def embed_querry(query, base, model, limit=0.6):
    """
    Gera uma consulta semântica e retorna a informação correspondente no dataframe.

    Args:
        query: A consulta do usuário.
        base: O dataframe contendo os embeddings e as informações.
        model: O modelo de embedding.
        limite: Limite de similaridade para considerar uma resposta válida.

    Returns:
        A informação correspondente à consulta ou uma mensagem de erro caso a similaridade seja insuficiente.
    """

    query_embed = genai.embed_content(
        model=model, content=query, 
        task_type="retrieval_query")["embedding"]

    dot_products = np.dot(np.stack(df["Embeddings"]), query_embed)
    idx = np.argmax(dot_products)

    # Calcula a similaridade do cosseno
    similarity = dot_products[idx] / (
        np.linalg.norm(query_embed) * np.linalg.norm(base["Embeddings"][idx])
    )

    # Verificar se a maior similaridade está acima do limite
    if similarity >= limit:
        print("\nsimilarity:", similarity)
        return df.iloc[idx]["Content"]
    else:
        print("\nsimilarity:", similarity)


# **Configurações e Parametrização do modelo**

gen_config = {
    "candidate_count": 1,
    "temperature": 0.3,
    # 'top_k':1,
    # 'top_p':1
}

safety_config = {
    "harassment": "block_none",
    "hate": "block_none",
    "sexual": "block_none",
    "dangerous": "block_none",
}

# **Consulta**
st.title('Agent M|535')

def  chat_history(messages):
    for message in messages:
        with st.chat_message(message['role']):
            st.markdown(message['content'])

def input_user_query(user_query, df, gen_model, embed_model):
    passage = embed_querry(user_query, df, embed_model)
    prompt = f'''Voce é M|535 um agente expecialista em Mises e escola Austriaca de economia. Reescreva estes dados. 
                Você responderá sobre {query} com o que você aprendeu com este dados.
                Sua resposta deverá ser de fácil entendimento.  {passage}'''      
    response = gen_model.generate_content(prompt)
    return response.text 

# Inicialização do histórico de mensagens
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Exibe o histórico de mensagens    
chat_history(st.session_state.messages)

# Captura a consulta do usuário
query = st.chat_input('Ask Agent M|535')
if query:
    with st.chat_message('You'):
        st.markdown(query)
    
    # Adiciona a consulta ao histórico    
    st.session_state.messages.append({"role": "user", "content": query})

    # Configura o modelo de geração 
    gen_model = genai.GenerativeModel('gemini-1.5-pro-latest',
                                        generation_config=gen_config,
                                        safety_settings=safety_config)

    # Processa a consulta e obtém a resposta
    response = input_user_query(query, df, gen_model, embed_model)

    # Exibe a resposta
    with st.chat_message('ai'):
        st.markdown(response)
    
    # Adiciona a resposta ao histórico    
    st.session_state.messages.append({"role": "assistant", "content": response})    
