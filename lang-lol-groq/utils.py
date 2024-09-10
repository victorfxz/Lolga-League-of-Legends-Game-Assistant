from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from pinecone import Pinecone
from pinecone import ServerlessSpec
import streamlit as st
import os
from groq import Groq

load_dotenv()

# Set your environment variables or replace them with your actual keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

# Groq API key and SentenceTransformer model initialization
groq_client = Groq(api_key=GROQ_API_KEY)

# Pinecone initialization
pc = Pinecone(api_key=PINECONE_API_KEY)

# Pinecone index creation (if it doesn't exist)
index_name = "lol"
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=384,  # Dimension for 'all-MiniLM-L6-v2' model
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )

# Get the index
index = pc.Index(index_name)

model = SentenceTransformer('all-MiniLM-L6-v2')

def find_match(input_text):
    input_embedding = model.encode(input_text).tolist()
    result = index.query(vector=input_embedding, top_k=2, include_metadata=True)
    matches = result['matches']
    return "\n".join([match['metadata']['text'] for match in matches])

def query_refiner(conversation, query):
    messages = [
        {"role": "system", "content": "An intelligent assistant for quick queries about League of Legends."},
        {"role": "user", "content": f"Given the user's query and the following conversation log, formulate a question so that it is more relevant to provide the user with an answer from a League of Legends game knowledge base. But, it is important that the meaning of the user's question is kept intact! \n\nCONVERSATION LOG: \n{conversation}\n\nQuery: {query}\n\nRefined Query:"},
    ]
    response = groq_client.chat.completions.create(
        messages=messages,
        model="gemma-7b-it",
        temperature=0.7,
        max_tokens=256,
    )
    return response.choices[0].message.content

def get_conversation_string():
    conversation_string = ""
    for i in range(len(st.session_state['responses'])-1):
        conversation_string += f"Human: {st.session_state['requests'][i]}\n"
        conversation_string += f"Bot: {st.session_state['responses'][i+1]}\n"
    return conversation_string