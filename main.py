import pandas as pd
import numpy as np
import google.generativeai as genai
import streamlit as st
import os
import random
from dotenv import load_dotenv
from openai import OpenAI

### Configures the genai library with the obtained API key ###
load_dotenv()
XAI_API_KEY = os.getenv("XAI_API_KEY") # 'REPLACE_BY_YOUR_API_HERE'
API_KEY = os.getenv("GOOGLE_API_KEY")  # 'REPLACE_BY_YOUR_API_HERE'
genai.configure(api_key=API_KEY)

### Defining the page title and icon ###
st.set_page_config(
    page_title="Agent M|535", page_icon="assets/badge.png", layout="centered"
)

### Load the CSV file into a pandas dataframe ###
knowledge_base = pd.read_csv("knowledge_base.csv")


### Defining the model in the model variable ###
embed_model = "models/text-embedding-004"

### Load the embeddings ###
# embeddings = np.load("embeddings.npy", allow_pickle=True)

### Embeddings generator function ###
@st.cache_data(persist=True)
def embed_doc(title, content):

    ''''
    Generates embeddings for documents using the specified template.

    Args:
        title: The title of the document.
        content: The body of the document's content.

    Returns:
        An embedding vector representing the document.
    '''
    embedding = genai.embed_content(model=embed_model,
                             content=content,
                             task_type='retrieval_document',
                             title=title)['embedding']

    return embedding

knowledge_base['Embeddings'] = knowledge_base.apply(lambda row: embed_doc(row['Title'], row['Content']), axis=1)

embeddings = knowledge_base['Embeddings'].values

### Function that generates query embeddings ###
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
        model=embed_model, content=query, task_type="retrieval_query")["embedding"]

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

    elif similarity > 0.60:
        print(f"\nsimilarity: {similarity}")
        prompt = f"""Responda sobre {query} pela ótica de Mises e da Escola Austriaca de Economia.
                    Sugira perguntas relacionadas a Escola Austriaca de Economia"""
        return prompt

    elif similarity < 60:
        print(f"\nsimilarity: {similarity}")
        prompt = f"""Você deve dizer: Este assunto sobre {query} está alem do seu conhecimento.
                    Você deve sugerir perguntas relacionadas a Escola Austriaca de Economia para envolver o usuário no assunto
                    Você deve sugerir sites relacionado a {query} ao usuário para que ele posso se informar 
                    """
        return prompt


### Gemini model configurations ###
gen_config = {"candidate_count": 1, "temperature": 0.5, "top_p": 0.7, "top_k": 25}

safety_config = {
    "harassment": "block_none",
    "hate": "block_none",
    "sexual": "block_none",
    "dangerous": "block_none",
}

#######################################################################
# Agent M|535

### Function that displays a chat history in a Streamlit application ###
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

### Sidebar layout definition ###
with st.sidebar:

    # Agent badge image
    st.image("assets/badge.png", caption="Agent Mi535")

    # Kids mode button
    on = st.toggle("Kids mode", help="Active the kids mode")

    models_choice = st.radio(label="Models", options=["gemini-2.0-flash", "grok-2-1212"])

    if models_choice == "gemini":
        llm = genai.GenerativeModel(
        "gemini-2.0-flash",
        generation_config=gen_config,
        safety_settings=safety_config,
        system_instruction="""Voce é um agente expecialista em Mises e escola Austriaca de economia, seu nome é M|535
                            Este conteúdo é o seu conhecimento sobre Mises e a Escola Austríaca de Economia.
                            Você sempre deve saudar o usuário""",
    )
    if models_choice == "grok":
        llm = OpenAI(
        api_key=XAI_API_KEY,
        base_url="https://api.x.ai/v1",
    )
    
    # Page footer
    footer = """
        <footer style="position: fixed; left: 0; bottom: 0; width: 20%; height: 5%;  padding: 4px; text-align: left;">
            <div class="footer-content">
                <p style="font-size: 0.875em; color: #4c5666; text-align: left;">Agent M|535 by SmokingSnakes83</p>
            </div>
        </footer>
            """
    st.markdown(footer, unsafe_allow_html=True)

### Function that processes a user query and embeds it ###
def input_user_query(user_query, model):
    """
    Processes a user query, embeds it, generates a response using a language model, and returns the response.

    Args:
    user_query: The user's input query as a string.
    model: A language model object capable of generating text.

    Returns:
    A string representing the generated response to the user query.
    """
    passage = embed_query(user_query)

    ### Conditional for kids mode activation ###
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

    ### Response of models ###        
    if models_choice in "gemini-2.0-flash":
        response = model.generate_content(prompt)
        return response.text

    if models_choice in "grok-2-1212":
        response = model.chat.completions.create(
        model="grok-2-1212",
        messages=[
            {"role": "user", "content": prompt}
        ],
        )
        return response.choices[0].message.content


### List of suggested questions ###
from modules import suggestion_questions
questions = suggestion_questions.questions_list
questions_samples = random.choice(questions)

#########################################################
### Start screen ###

col1, col2, col3 = st.columns(3)
with col1:
     with st.container():
        st.columns(spec=1)
with col2:
     with st.container():
        st.image("assets/logo.png")
with col3:
    with st.container():
        st.columns(spec=1)         


### Message history initialization ###
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display message history
chat_history(st.session_state.messages)

### Capture user query ###
query = st.chat_input(placeholder=questions_samples)

if query:
    with st.chat_message(name="You"):
        st.markdown(query)

    # Add the query to the history
    st.session_state.messages.append({"role": "You", "content": query})
    
    ### Configure the generative model ###
    # model = genai.GenerativeModel(
    #     "gemini-2.0-flash",
    #     generation_config=gen_config,
    #     safety_settings=safety_config,
    #     system_instruction="""Voce é um agente expecialista em Mises e escola Austriaca de economia, seu nome é M|535
    #                         Este conteúdo é o seu conhecimento sobre Mises e a Escola Austríaca de Economia.
    #                         Você sempre deve saudar o usuário""",
    # )
    llm = llm
    # model = OpenAI(
    # api_key=XAI_API_KEY,
    # base_url="https://api.x.ai/v1",
# )


    ### Process the query and get the response ###
    response = input_user_query(query, llm)

    #### Display the response ###
    with st.chat_message(avatar="assets/bot.png", name="Agent M|535"):
        st.markdown(response)
    # Add the answer to the history
    st.session_state.messages.append({"role": "M|535", "content": response})

