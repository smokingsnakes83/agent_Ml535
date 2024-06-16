import pandas as pd
import numpy as np
import google.generativeai as genai
import streamlit as st
import os

from dotenv import load_dotenv

# Configures the genai library with the obtained API key
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")  # 'REPLACE_BY_YOUR_API_HERE'
genai.configure(api_key=API_KEY)

# Load the CSV file into a pandas dataframe
df = pd.read_csv("knowledge_base.csv")
# df

# Defining the model in the model variable
embed_model = "models/text-embedding-004"


# Function that generates embeddings for documents
def embed_doc(title, content):
    """'
    Generates embeddings for documents using the specified template.

    Args:
        title: The title of the document.
        content: The body of the document's content.

    Returns:
        An embedding vector representing the document.
    """

    return genai.embed_content(
        model=embed_model, content=content, task_type="retrieval_document", title=title
    )["embedding"]


# Apply the embed_doc function to each row of the dataframe
df["Embeddings"] = df.apply(lambda row: embed_doc(row["Title"], row["Content"]), axis=1)

# df

# Function that generates query embeddings


def embed_querry(query, base, model, limit=0.6):
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

    query_embed = genai.embed_content(
        model=model, content=query, task_type="retrieval_query"
    )["embedding"]

    dot_products = np.dot(np.stack(df["Embeddings"]), query_embed)
    idx = np.argmax(dot_products)

    # Calculate cosine similarity
    similarity = dot_products[idx] / (
        np.linalg.norm(query_embed) * np.linalg.norm(base["Embeddings"][idx])
    )

    # Check if the highest similarity is above the limit
    if similarity >= limit:
        print("\nsimilarity:", similarity)
        return df.iloc[idx]["Content"]

    elif similarity > 0.5:
        print("\nsimilarity:", similarity)
        return f"You must respond by optic Mises's and the Economy Austrian School's "

    else:
        print("\nsimilarity:", similarity)
        return f"""You must Respond with the following fallback: "Isso está alem do meu conhecimento,"
                não fui treinado para este tema.
                Você deve sugerir algumas perguntas relacionada Mises, Economia e Escola Autriaca de Economia."""

# Model configurations and parameterization

gen_config = {"candidate_count": 1, "temperature": 0.5, "top_p": 0.95}

safety_config = {
    "harassment": "block_none",
    "hate": "block_none",
    "sexual": "block_none",
    "dangerous": "block_none",
}

# Agent M|535

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


# Defining the page title and icon
st.set_page_config(
    page_title="Agent M|535", page_icon="assets/badge.png", layout="wide"
)

# Sidebar's definition
with st.sidebar:
    # Agent badge image
    st.image("assets/badge.png", caption="Agent M|535")
    with st.container(height=0):
        # Kids mode button
        on = st.toggle("KIDS mode")

    code = """ 
        <footer>
            <div class="footer-content">
                <p>2024 - SmokingSnakes83</p>
                <ul>
                    <li><a href="https://github.com/smokingsnakes83/agent_Ml535" target="_blank"><i class="fab fa-github"></i>GitHub</a></li>
                </ul>
            </div>
        </footer>
        """
    st.html(code)

def input_user_query(user_query, df, gen_model, embed_model):
    """
    Processes a user query, embeds it, generates a response using a language model, and returns the response.

    Args:
    user_query: The user's input query as a string.
    df: A Pandas DataFrame containing relevant data for the query.
    gen_model: A language model object capable of generating text.
    embed_model: An embedding model used to embed the user query.

    Returns:
    A string representing the generated response to the user query.
    """
    passage = embed_querry(user_query, df, embed_model)

    # Conditional for kids mode activation
    if on:
        st.caption(":boy: :green[Kids mode activated]")

        system_instruction = f"""Seu nome é M|535, você é um agente expecialista em Mises e escola Austriaca de economia.
            Este texto agora faz parte de seus conhecimentos.
            Você sempre deve se referir a este texto como seus conhecimentos. 
            Você deve elaborar uma resposta com esses conhecimentos.
            Você responderá sobre {query} com base em seus conhecimentos como se estivesse explicando para uma criança de 5 anos de idade.
            Sua resposta deverá ser de fácil entendimento. {passage}
            Sempre responda uma saudação do usúario com cordialidade"""
    else:
        system_instruction = f"""Seu nome é M|535, você é um agente expecialista em Mises e escola Austriaca de economia.
            Este texto agora faz parte de seu conhecimento.
            Você sempre deve se referir a este texto como seus conhecimentos
            Você deve elaborar uma resposta com esses conhecimentos
            Você responderá sobre {query} com base em seus conhecimentos.
            Sua resposta deverá ser de fácil entendimento.
            Sempre responda uma saudação do usúario com cordialidade  {passage}"""

    response = gen_model.generate_content(system_instruction, stream=True)
    response.resolve()
    return response.text


with st.container(height=0):
    # Message history initialization
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display message history
    chat_history(st.session_state.messages)

# Capture user query
query = st.chat_input("Ask Agent M|535")

if query:
    with st.chat_message(name="You"):
        st.markdown(query)

    # Add the query to the history
    st.session_state.messages.append({"role": "You", "content": query})

    # Configure the generative model
    gen_model = genai.GenerativeModel(
        "gemini-1.5-pro-latest",
        generation_config=gen_config,
        safety_settings=safety_config,
    )

    # Process the query and get the response
    response = input_user_query(query, df, gen_model, embed_model)

    # Display the response
    with st.chat_message(avatar="assets/bot.png", name="Agent M|535"):
        st.markdown(response)

    # Add the answer to the history
    st.session_state.messages.append({"role": "M|535", "content": response})
