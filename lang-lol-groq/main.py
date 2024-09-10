import os
import streamlit as st
from streamlit_chat import message
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder
)
from utils import get_conversation_string, query_refiner, find_match
import psycopg2

# Load environment variables
load_dotenv()

# Function to connect to the PostgreSQL database
def get_db_connection():
    conn = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT")
    )
    return conn

# Function to save question and answer to the database
def save_conversation_to_db(question, response):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO conversation_history (question, response) VALUES (%s, %s)", (question, response))
    conn.commit()
    cur.close()
    conn.close()

# Initialize the LLM
llm = ChatGroq(temperature=0, model_name="mixtral-8x7b-32768")

# Initial Streamlit configuration
st.set_page_config(page_title="LOLGA - League of Legends Game Assistant", page_icon="🎱", layout="wide")

def initialize_session_state():
    # Initialize the list of responses with the default question, if it doesn't exist
    if 'responses' not in st.session_state:
        st.session_state['responses'] = ["Please elaborate your question related to the game League of Legends"]
    
    # Initialize the list of requests as empty
    if 'requests' not in st.session_state:
        st.session_state['requests'] = ["Ex: What is the main role of Garen in League of Legends?"]  # First default question

    # Initialize the conversation buffer memory
    if 'buffer_memory' not in st.session_state:
        st.session_state.buffer_memory = ConversationBufferWindowMemory(k=3, return_messages=True)

# Call the function to ensure the session state is initialized correctly
initialize_session_state()

# Title and description of the application
st.title("LOLGA - League of Legends Game Assistant")
st.markdown("**An intelligent assistant for quick queries about League of Legends.**")

# Layout organization in columns
response_container, text_container = st.columns([2, 1])

# Content on the right side (text_container)
with text_container:
    st.header("Ask a Question")
    st.write("Type your question below: Ex: Who is Garen's sister?")
    query = st.text_input("Your Question", key="input", placeholder="Ex: What is the maximum level a champion can reach in a standard game of League of Legends?")
    
    if st.button("Send"):
        if query:
            with st.spinner("Processing..."):
                conversation_string = get_conversation_string()
                refined_query = query_refiner(conversation_string, query)
                st.subheader("Refined query by the Agent")
                st.write(refined_query)
                context = find_match(refined_query)

                # Adjust the prompt to use the MessagesPlaceholder correctly
                system_msg_template = SystemMessagePromptTemplate.from_template(
                    template="""Please answer the question as truthfully as possible using the context provided, and if the answer is not contained in the bulletin board text, formulate one with basic and truthful information about the game League of Legends If there is any problem finding answers in the database, please return: 'Please resubmit your question!'"""
                )
                human_msg_template = HumanMessagePromptTemplate.from_template(template="{input}")
                
                # Include the 'history' variable for the buffer memory
                prompt_template = ChatPromptTemplate.from_messages(
                    [
                        system_msg_template,
                        MessagesPlaceholder(variable_name="history"),  # Include 'history' from the buffer memory
                        human_msg_template
                    ]
                )
                
                conversation = ConversationChain(
                    memory=st.session_state.buffer_memory,
                    prompt=prompt_template,
                    llm=llm,
                    verbose=True
                )

                # The query is passed as 'input'
                response = conversation.predict(input=f"Context:\n {context} \n\n Query:\n{query}")
                
                # Save question and answer to the database
                save_conversation_to_db(query, response)

                st.session_state.requests.append(query)
                st.session_state.responses.append(response)
        else:
            st.error("Please enter a question before submitting.")

# Content on the left side (response_container)
with response_container:
    st.header("Query History")
    
    # Check if there are responses and requests
    if st.session_state['requests'] and st.session_state['responses']:
        for i in range(len(st.session_state['responses'])):
            # Check if the index 'i' exists in both lists
            if i < len(st.session_state['requests']):
                with st.expander(f"Query {i+1}", expanded=True):
                    st.markdown(f"**Question:** {st.session_state['requests'][i]}")
                    message(st.session_state['responses'][i], key=str(i), avatar_style="pixel-art", seed="AI")
    else:
        st.write("No queries yet. Please ask a question to get started.")

# Custom footer
st.markdown("---")
st.markdown("**LOLGA - League of Legends Game Assistant** 2024 | Developed with ❤️ and 🧠 using Streamlit")