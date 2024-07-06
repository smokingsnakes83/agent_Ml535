import pandas as pd
import numpy as np
import google.generativeai as genai
import streamlit as st
import os
import random
from dotenv import load_dotenv

# Configures the genai library with the obtained API key
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")  # 'REPLACE_BY_YOUR_API_HERE'
genai.configure(api_key=API_KEY)

# Load the CSV file into a pandas dataframe
knowledge_base = pd.read_csv("knowledge_base.csv")


# Defining the model in the model variable
embed_model = "models/embedding-001"

# Load the embeddings
embeddings = np.load("embeddings.npy", allow_pickle=True)


# Function that generates query embeddings
def embed_query(query, limit=0.7):
    """
    Generates a semantic query and returns the corresponding information in the dataframe.

    Args:
        query: The user's query.
        base: The dataframe containing the embeddings and information.
        model: The embedding model.
        threshold: Similarity threshold to consider a valid answer.

    Returns:
        The information corresponding to the query or an error message if the similarity is insufficient.
    """

    query_embedding = genai.embed_content(
        model=embed_model, content=query, task_type="retrieval_query"
    )["embedding"]

    dot_products = np.dot(np.stack(embeddings), query_embedding)
    idx = np.argmax(dot_products)

    # Calculate cosine similarity
    similarity = dot_products[idx] / (
        np.linalg.norm(query_embedding) * np.linalg.norm(embeddings[idx])
    )

    # Check if the highest similarity is above the limit
    if similarity >= limit:
        print(f"\nsimilarity: {similarity}")
        return knowledge_base.iloc[idx]["Content"]

    elif similarity > 0.65:
        print(f"\nsimilarity: {similarity}")
        prompt = f"""Responda sobre {query} pela ótica de Mises e da Escola Austriaca de Economia.
                    Sugira perguntas relacionadas a Escola Austriaca de Economia"""
        return prompt

    else:
        print(f"\nsimilarity: {similarity}")
        prompt = f"""Diga que o assunto sobre {query} está alem do seu conhecimento.
                    Sugira perguntas relacionadas a Escola Austriaca de Econoima"""
        return prompt


# Model configurations
gen_config = {"candidate_count": 1, "temperature": 0.5, "top_p": 0.7, "top_k": 25}

safety_config = {
    "harassment": "block_none",
    "hate": "block_none",
    "sexual": "block_none",
    "dangerous": "block_none",
}

#######################################################################
# Agent M|535

# Function that displays a chat history in a Streamlit application.
def chat_history(messages):
    """
    Displays a chat history in a Streamlit application.

    Args:
        messages (list): A list of dictionaries, where each dictionary represents a message.
            Each dictionary should have the following keys:
                * role (str): The role of the sender (e.g., "You", "Agent M|535").
                * content (str): The content of the message.
    """

    for message in messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


# Function that processes a user query and embeds it
def input_user_query(user_query, gen_model):
    """
    Processes a user query, embeds it, generates a response using a language model, and returns the response.

    Args:
    user_query: The user's input query as a string.
    gen_model: A language model object capable of generating text.

    Returns:
    A string representing the generated response to the user query.
    """
    passage = embed_query(user_query)

    # Conditional for kids mode activation
    if on:
        st.caption(":boy: :green[Kids mode activated]")

        prompt = f"""Este conteúdo é o seu conhecimento sobre Mises e a Escola Austríaca de Economia.
            Você deve elaborar suas respostas sobre {query} baseadas nos conhecimentos adiquiridos
            Utilize uma linguagem acessível.
            De exemplos para concretizar a informação.
            Você responderá sobre {query} com base em seus conhecimentos como se estivesse explicando para uma criança de 10 anos de idade.
            Sua resposta deverá ser de fácil entendimento. {passage}"""
    else:
        prompt = f"""Este conteúdo é o seu conhecimento sobre Mises e a Escola Austríaca de Economia.
            Você deve elaborar suas respostas sobre {query} baseadas nos conhecimentos adiquiridos
            Utilize uma linguagem acessível.
            De exemplos para concretizar a informação.

            {passage}"""

    response = gen_model.generate_content(prompt)
    return response.text


# Defining the page title and icon
st.set_page_config(
    page_title="Agent M|535", page_icon="assets/badge.png", layout="centered"
)

# Sidebar's definition
with st.sidebar:

    # Agent badge image
    st.image("assets/badge.png", caption="Agent Mi535")

    # Kids mode button
    on = st.toggle("Kids mode", help="Active the kids mode")

    # Page footer
    footer = """
        <footer style="position: fixed; right: 0; bottom: 0; width: 100%; height: 5%; background-color: #171717; padding: 4px; text-align: left;">
            <div class="footer-content">
                <p style="font-size: 0.875em; color: #4c5666; text-align: center;">Agent M|535 by SmokingSnakes83</p>
            </div>
        </footer>
            """
    st.markdown(footer, unsafe_allow_html=True)

# Message history initialization
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display message history
chat_history(st.session_state.messages)

# Capture user query
query = st.chat_input("Ask Agent Mi535:")

if query:
    with st.chat_message(name="You"):
        st.markdown(query)

    # Add the query to the history
    st.session_state.messages.append({"role": "You", "content": query})

    # Configure the generative model
    gen_model = genai.GenerativeModel(
        "gemini-1.5-flash",
        generation_config=gen_config,
        safety_settings=safety_config,
        system_instruction="""Voce é um agente expecialista em Mises e escola Austriaca de economia, seu nome é M|535
                            Este conteúdo é o seu conhecimento sobre Mises e a Escola Austríaca de Economia.
                            Você sempre deve saudar o usuário""",
    )

    # Process the query and get the response
    response = input_user_query(query, gen_model)

    # Display the response
    with st.chat_message(avatar="assets/bot.png", name="Agent M|535"):
        st.markdown(response)
    # Add the answer to the history
    st.session_state.messages.append({"role": "M|535", "content": response})
    
#########################################################
#Start screen

questions_list_1 = [
    "O que distingue a ação humana do comportamento animal, de acordo com Mises?",
    "Quais são os pré-requisitos para a ação humana?",
    "Qual a relação entre a praxeologia e a psicologia?",
    "O que é o apriorismo e por que Mises o considera fundamental para a economia?",
    "Explique o princípio do individualismo metodológico.",
    "Qual o papel da razão na ação humana?",
    "Como o polilogismo contesta a lógica e a razão?",
    "Por que a teoria do cálculo econômico é crucial para Mises?",
    "Quais as principais características da economia de mercado?",
    "O que é cataláxia?",
    "Qual a diferença entre bens livres e bens econômicos?",
    "O que define a utilidade marginal?",
    "Explique a lei dos rendimentos decrescentes.",
    "O que distingue o trabalho introvertido do trabalho extrovertido?",
    "Quais são as fontes de prazer no trabalho?",
    "Como a economia de mercado funciona em relação ao tempo?",
    "O que é preferência temporal e qual a sua importância?",
    "Quais as diferentes formas de poupança e como elas se relacionam com o capital?",
    "Explique a natureza do juro originário.",
    "Quais os principais componentes da taxa bruta de juros do mercado?",
    "Como a expansão do crédito afeta a taxa de juros?",
    "Como Mises explica a relação entre a oferta de moeda e o poder aquisitivo?",
    "O que é o teorema da regressão e qual a sua importância?",
    "Quais os diferentes tipos de moeda e quais as suas características?",
    "Como Mises analisa o surgimento da moeda fiduciária?",]
questions_list_2 = [
    "O que é o padrão-ouro e quais suas vantagens?",
    "Explique o conceito de ""entesouramento"" e por que Mises o considera um mito.",
    "Como a intervenção governamental no sistema monetário gera caos?",
    "O que é o problema do cálculo econômico no socialismo?",
    "Quais as principais falhas do planejamento centralizado?",
    "Qual o papel do governo em uma sociedade livre, segundo Mises?",
    "Explique a falácia da ""economia mista"".",
    "Quais as consequências do controle de preços?",
    "Como o intervencionismo leva ao socialismo?",
    "Quais os diferentes tipos de intervenção fiscal?",
    "Explique a natureza e os efeitos das medidas restritivas à produção.",
    "Por que a busca por preços ""justos"" é uma ilusão?",
    "Quais as características dos preços monopolísticos?",
    "Qual a diferença entre lucro empresarial e ganho monopolístico?",
    "Por que Mises considera o sindicalismo um sistema ineficaz e prejudicial?",
    "Como a doutrina do ""efeito de Ricardo"" é equivocada?",
    "Qual o papel da especulação em uma economia de mercado?",
    "Qual o significado do conceito de ""capital"" para Mises?",
    "Explique a importância da propriedade privada para o funcionamento do livre mercado.",
    "Por que Mises considera a guerra e o socialismo como sistemas incompatíveis com a liberdade e a prosperidade?",
    "Quais os principais problemas da ""economia de guerra""?",
    "Como o intervencionismo governamental gera a mentalidade anticapitalista?",
    "Quais os principais argumentos em favor da ""estabilização"" e por que Mises os considera falaciosos",
    "Qual o papel da educação na difusão do pensamento econômico?",
    "Por que Mises acredita que o estudo da economia é crucial para o futuro da liberdade?"
    ]
    
question_sample_1 = random.choice(questions_list_1)
question_sample_2 = random.choice(questions_list_2)

if not query:
    col11, col21, col31 = st.columns(3)
    with col11:
        st.container()
    with col21:
            st.image("assets/logo.png", width=280)
    with col31:
        st.container()
            
    col1, col2, col3 = st.columns(3)
    
    with col1:
        with st.container(border=True, height=135):
            st.markdown("Estou pronto para te ajudar a entender o mundo pela ótica da Escola Austríaca de Economia (EAE).")
    with col2:
        with st.container(border=True, height=135):
            st.write("Pergunte-me:",question_sample_1)
    with col3:
        with st.container(border=True, height=135):
            st.write("Pergunte-me:", question_sample_2)