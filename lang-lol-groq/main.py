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

def show_login():
    st.markdown("""# Welcome to LOLGA <img align="center" src="https://i.imgur.com/X4n9ruu.png" width="45">""", unsafe_allow_html=True)
    st.write("Please log in to continue:")

    # Input fields for username and password
    username = st.text_input("Username", placeholder="Enter your username")
    password = st.text_input("Password", type="password", placeholder="Enter your password")

    # Login button
    if st.button("Login"):
        st.info("Double-click the button to log in.")
        if username.strip() and password.strip():  # Check if username and password are not empty or just spaces
            # Add actual authentication logic here if needed
            st.session_state["logged_in"] = True
            st.success("Login successful!")
            st.session_state["show_login"] = False
            # Use a flag to indicate that login was successful
            st.session_state["reload_page"] = True
        else:
            st.error("Username and password cannot be empty or just spaces.")

# Check if the user is logged in
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    if "reload_page" in st.session_state and st.session_state["reload_page"]:
        # Clear the reload flag and reset the session state to simulate a restart
        st.session_state["reload_page"] = False
        st.experimental_rerun()
    show_login()
else:
    # Código principal do aplicativo
    # Inicialização do LLM
    llm = ChatGroq(
        temperature=0,
        model_name="mixtral-8x7b-32768",
        groq_api_key="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"
    )

    # Configuração inicial do Streamlit
    st.set_page_config(page_title="LOLGA - League of Legends Game Assistant", page_icon="🎱", layout="wide")

    def initialize_session_state():
        # Inicializa a lista de respostas com a pergunta padrão, se ainda não existir
        if 'responses' not in st.session_state:
            st.session_state['responses'] = ["Please elaborate your question related to the game League of Legends!"]
        
        # Inicializa a lista de solicitações vazia
        if 'requests' not in st.session_state:
            st.session_state['requests'] = ["Can you help me with questions about League of Legends?"]  # Primeira pergunta padrão

        # Inicializa o buffer de memória da conversação
        if 'buffer_memory' not in st.session_state:
            st.session_state.buffer_memory = ConversationBufferWindowMemory(k=3, return_messages=True)

    # Função para validar se a pergunta é sobre League of Legends
    def is_question_related_to_lol(query):
        lol_keywords = lol_keywords = [
            'champion', 'League of Legends', 'LoL', 'runes', 'abilities', 'skins', 'lore', 'jungler', 
            'ADC', 'marksman', 'top', 'mid', 'support', 'dragon', 'baron', 'Demacia', 'Noxus', 
            'Runeterra', 'championship', 'Riot Games', 'summoner', 'nexus', 'Wild Rift', 'ARAM', 
            'ranked', 'draft pick', 'blind pick', 'pro play', 'meta', 'kill', 'death', 'assist', 'KDA', 
            'towers', 'inhibitor', 'turrets', 'lanes', 'wave management', 'minions', 'creeps', 'cs', 
            'last hit', 'poke', 'all-in', 'engage', 'disengage', 'macro', 'micro', 'farming', 'split push', 
            'team fight', 'ward', 'vision control', 'bot lane', 'mid lane', 'top lane', 'red buff', 
            'blue buff', 'gank', 'counter gank', 'invade', 'counter jungle', 'peel', 'CC', 'crowd control', 
            'slow', 'stun', 'snare', 'knockup', 'knockback', 'silence', 'supression', 'root', 'skillshot', 
            'passive', 'ultimate', 'flash', 'ignite', 'teleport', 'smite', 'exhaust', 'baron buff', 
            'rift herald', 'elder dragon', 'hextech drake', 'cloud drake', 'mountain drake', 'infernal drake', 
            'ocean drake', 'scuttle crab', 'hex gates', 'bush', 'terrain', 'terrain manipulation', 
            'summoner spells', 'keystone', 'omnivamp', 'lifesteal', 'AP', 'AD', 'armor', 'magic resistance', 
            'penetration', 'lethality', 'tenacity', 'attack speed', 'movement speed', 'champion pool', 
            'draft phase', 'ban phase', 'outplay', 'snowball', 'shutdown', 'gold lead', 'objective', 
            'turret plating', 'herald push', 'tower dive', 'reset', 'respawn', 'homeguard', 'boots', 
            'mythic item', 'legendary item', 'support item', 'control ward', 'sweep', 'orb', 'trinket', 
            'stopwatch', 'Zhonya\'s', 'Galeforce', 'Kraken Slayer', 'Essence Reaver', 'Maw of Malmortius', 
            'Sunfire Aegis', 'Randuin\'s Omen', 'Frozen Heart', 'Thornmail', 'Banshee\'s Veil', 
            'Mercurial Scimitar', 'Guardian Angel', 'Sterak\'s Gage', 'Dead Man\'s Plate', 
            'Rabadon\'s Deathcap', 'Void Staff', 'Liandry\'s Anguish', 'Luden\'s Tempest', 
            'Everfrost', 'Shurelya\'s Reverie', 'Moonstone Renewer', 'Imperial Mandate', 'Stridebreaker', 
            'Divine Sunderer', 'Trinity Force', 'Riftmaker', 'Frostfire Gauntlet', 'Turbo Chemtank', 
            'Chemtech Soul', 'Hextech Soul', 'Cloud Soul', 'Infernal Soul', 'Ocean Soul', 'Mountain Soul', 
            'Aatrox', 'Ahri', 'Akali', 'Akshan', 'Alistar', 'Amumu', 'Anivia', 'Annie', 'Aphelios', 
            'Ashe', 'Aurelion Sol', 'Azir', 'Bard', 'Bel\'Veth', 'Blitzcrank', 'Brand', 'Braum', 
            'Caitlyn', 'Camille', 'Cassiopeia', 'Cho\'Gath', 'Corki', 'Darius', 'Diana', 'Dr. Mundo', 
            'Draven', 'Ekko', 'Elise', 'Evelynn', 'Ezreal', 'Fiddlesticks', 'Fiora', 'Fizz', 'Galio', 
            'Gangplank', 'Garen', 'Gnar', 'Gragas', 'Graves', 'Gwen', 'Hecarim', 'Heimerdinger', 
            'Illaoi', 'Irelia', 'Ivern', 'Janna', 'Jarvan IV', 'Jax', 'Jayce', 'Jhin', 'Jinx', 
            'K\'Sante', 'Kai\'Sa', 'Kalista', 'Karma', 'Karthus', 'Kassadin', 'Katarina', 'Kayle', 
            'Kayn', 'Kennen', 'Kha\'Zix', 'Kindred', 'Kled', 'Kog\'Maw', 'LeBlanc', 'Lee Sin', 
            'Leona', 'Lillia', 'Lissandra', 'Lucian', 'Lulu', 'Lux', 'Malphite', 'Malzahar', 
            'Maokai', 'Master Yi', 'Milio', 'Miss Fortune', 'Mordekaiser', 'Morgana', 'Naafiri', 
            'Nami', 'Nasus', 'Nautilus', 'Neeko', 'Nidalee', 'Nocturne', 'Nunu & Willump', 
            'Olaf', 'Orianna', 'Ornn', 'Pantheon', 'Poppy', 'Pyke', 'Qiyana', 'Quinn', 
            'Rakan', 'Rammus', 'Rek\'Sai', 'Rell', 'Renekton', 'Rengar', 'Riven', 'Rumble', 
            'Ryze', 'Sejuani', 'Senna', 'Seraphine', 'Sett', 'Shaco', 'Shen', 'Shyvana', 
            'Singed', 'Sion', 'Sivir', 'Sona', 'Soraka', 'Swain', 'Sylas', 'Syndra', 
            'Tahm Kench', 'Taliyah', 'Talon', 'Taric', 'Teemo', 'Thresh', 'Tristana', 'Trundle', 
            'Tryndamere', 'Twisted Fate', 'Twitch', 'Udyr', 'Urgot', 'Varus', 'Vayne', 'Veigar', 
            'Vel\'Koz', 'Vex', 'Vi', 'Viego', 'Viktor', 'Vladimir', 'Volibear', 'Warwick', 'Wukong', 
            'Xayah', 'Xerath', 'Xin Zhao', 'Yasuo', 'Yone', 'Yorick', 'Yuumi', 'Zac', 'Zed', 'Zeri', 
            'Ziggs', 'Zilean', 'Zoe', 'Zyra'
        ]  # Lista de palavras-chave
        # Verifica se a pergunta contém alguma palavra-chave relevante
        return any(keyword.lower() in query.lower() for keyword in lol_keywords)

    # Chama a função para garantir que o estado da sessão seja inicializado corretamente
    initialize_session_state()

    # Título e descrição da aplicação
    st.markdown("""
    <style>
    /* Remove or adjust margin/padding of the Streamlit container */
    .block-container {
        padding-top: 30px;
    }
    </style>
    """, unsafe_allow_html=True)
    st.markdown("""# LOLGA - League of Legends Game Assistant <img align="center" src="https://i.imgur.com/X4n9ruu.png" width="45">""", unsafe_allow_html=True)
    st.markdown("""
    🎱 *Explore the world of League of Legends with ease and depth. Enjoy personalized insights and answers to your questions about the game.*<br>
    🤖 **An intelligent assistant for quick queries about League of Legends.**
    """, unsafe_allow_html=True)
    st.markdown("")

    # Organização do layout em colunas
    text_container, response_container = st.columns([1, 2], gap="medium")

    # Conteúdo do lado esquerdo (text_container)
    with text_container:
        st.header("Ask a Question")
        st.markdown("""
        <span style="font-size: 14px;"><strong>For example</strong>: </span><span style="color: lightblue; font-size: 14px;">Who is Garen's sister?</span>
        """, unsafe_allow_html=True)
        
        # Ajuste do campo de entrada para aumentar a altura e reduzir a largura
        query = st.text_area(
            "Your Question", 
            key="input", 
            placeholder="Ex: Which champion can summon Tibbers?",
            help="Type your question here",
            max_chars=300,
            value=st.session_state.get("input", "")
        )

        if len(query) > 300:
            st.error("Por favor, insira uma pergunta com no máximo 300 caracteres.")

        st.markdown("""
            <style>
            /* Personaliza a cor do botão "Send" */
            .stButton button {
                background-color: #a83d3d; /* Vermelho */
                color: #FFFFFF; /* Texto preto */
                border: 2px solid #591d1d; /* Borda branca */
                border-radius: 5px; /* Bordas arredondadas */
            }
            .stButton button:hover {
                background-color: #300505;
            }
            </style>
            """, unsafe_allow_html=True)
        
        if st.button("Send"):
            if query:
                if is_question_related_to_lol(query):
                    with st.spinner("Processing..."):
                        conversation_string = get_conversation_string()
                        refined_query = query_refiner(conversation_string, query)
                        st.subheader("Refined query by the Agent")
                        st.write(refined_query)
                        context = find_match(refined_query)

                        # Ajustando o prompt para usar o MessagesPlaceholder corretamente
                        system_msg_template = SystemMessagePromptTemplate.from_template(
                            template="""Please answer the question as truthfully as possible using the context provided, and if the answer is not contained in the bulletin board text, formulate one with basic and truthful information about the game League of Legends If there is any problem finding answers in the database, please return: 'Please resubmit your question!'"""
                        )
                        human_msg_template = HumanMessagePromptTemplate.from_template(template="{input}")
                            
                        # Incluindo a variável 'history' para o buffer de memória
                        prompt_template = ChatPromptTemplate.from_messages(
                            [
                                system_msg_template,
                                MessagesPlaceholder(variable_name="history"),  # Inclua 'history' do buffer de memória
                                human_msg_template
                            ]
                        )
                            
                        conversation = ConversationChain(
                            memory=st.session_state.buffer_memory,
                            prompt=prompt_template,
                            llm=llm,
                            verbose=True
                        )

                        # A consulta é passada como 'input'
                        response = conversation.predict(input=f"Context:\n {context} \n\n Query:\n{query}")
                        st.session_state.requests.append(query)
                        st.session_state.responses.append(response)
                else:
                    st.error("This question does not seem to be related to League of Legends. Please ask questions about the game.")
            else:
                st.error("Please enter a question before submitting.")
        st.markdown("""
            <style>
            .clean-chat-button {
                background-color: #34A85A; /* Verde */
                color: #FFFFFF; /* Texto branco */
                border: 2px solid #2F865F; /* Borda verde escuro */
                border-radius: 5px; /* Bordas arredondadas */
                padding: 10px 20px; /* Espaçamento interno */
                cursor: pointer; /* Cursor como mãozinha */
                font-size: 16px; /* Tamanho da fonte */
                font-weight: bold; /* Fonte em negrito */
            }
            .clean-chat-button:hover {
                background-color: #228B22; /* Verde escuro ao passar o mouse */
            }
            </style>
        """, unsafe_allow_html=True)

        # HTML do botão com a classe CSS aplicada
        if st.button("Clear Chat", key="clear_chat_button"):
            st.session_state['responses'] = []
            st.session_state['requests'] = []
            st.session_state["user_input_area"] = ""
            st.session_state["needs_update"] = True  # Marca para indicar que uma atualização é necessária

        # Lógica para atualizar a interface
        if st.session_state.get("needs_update", False):
            st.session_state["needs_update"] = False

        # Conteúdo do lado direito (response_container)
        with response_container:
            st.header("Query History")
            
            # Verifica se há respostas e solicitações
            if st.session_state['requests'] and st.session_state['responses']:
                for i in range(len(st.session_state['responses'])):
                    # Verifica se o índice 'i' existe em ambas as listas
                    if i < len(st.session_state['requests']):
                        with st.expander(f"Query {i+1}", expanded=True):
                            st.markdown(f"**Question:** {st.session_state['requests'][i]}")
                            st.write(f"""
            <div style="display: flex; align-items: center; padding: 20px;">
            <img src="https://i.imgur.com/X4n9ruu.png" width="50" style="margin-left: -10px; margin-right: 34px;">
            <div style="background-color: transparent; padding: 10px; border-radius: 10px; border: 1px solid #666; width: 92%;">
                <p style="color: #e3e3e3;">{st.session_state['responses'][i]}</p>
            </div>
            </div>
            """, unsafe_allow_html=True)
            else:
                st.write("No queries yet. Please ask a question to get started.")

    st.markdown("---")
    st.markdown("<center><strong>LOLGA - League of Legends Game Assistant</strong> © 2024  | Developed with 🎮 and 💡 using Streamlit</center>", unsafe_allow_html=True)
