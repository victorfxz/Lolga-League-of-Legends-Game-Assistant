# LoLGA - League of Legends Game Assistant <img align="center" src="https://i.imgur.com/X4n9ruu.png" width="34">

<p align="center"><img src="https://i.imgur.com/PVgqqV1.png" width="150"><img src="https://i.imgur.com/e8hXph2.gif" width="650"></p>

## 📑 Project Overview
<p align="justify">League of Legends (LoL) is a game rich in lore, characters, and trivia that aren't always easily accessible to players. Many fans are curious about details like relationships between champions, backstories, and other interesting facts about the game universe. The LoLGA Game Assistant was developed to solve this problem by providing a fast and accurate assistant for answering questions about the game's lore and trivia. Using <strong>RAG (Retrieval-Augmented Generation)</strong> technology, this application allows users to ask questions and receive detailed responses about LoL's lore and characters, serving both casual fans and more involved players.</p>

> 📍 The text dataset was transformed into a vectorized dataset during the process.

## ⛔ Problem Description
<p align="justify">LoLGA is a chat app designed to solve the problem of fragmented access to League of Legends' lore. Currently, players face difficulties in finding accurate and up-to-date information about the game's history, champions, and equipment, as the information is scattered across multiple platforms, including Riot's official website, third-party wikis, forums, and fan-created content.
  
This can be frustrating and time-consuming, especially for players who want to deepen their knowledge of the game and its lore. Moreover, LoL's lore is vast and constantly evolving, making it even harder for players to stay up-to-date.
To address this issue, LoLGA was created to provide a centralized and user-friendly platform where players can ask questions and receive accurate and instant answers about LoL's history, champions, and equipment.
      
With LoLGA, players can:
* Access information about LoL's history, including its lore and in-game events
* Get details about champions, including their abilities and backstories
* Discover information about equipment and items in the game
* Receive accurate and up-to-date answers to frequently asked questions
  
LoLGA is an essential tool for any League of Legends player looking to deepen their knowledge of the game and its lore.
</p>

## 🔧 Technologies and Tools Used
### Key Technologies
ㅤ<img align="center" src="https://icon.icepanel.io/Technology/svg/Anaconda.svg" width="17">ㅤ**Anaconda** - Used for package management and creating the virtual environment.  
ㅤ<img align="center" src="https://icon.icepanel.io/Technology/svg/Docker.svg" width="17">ㅤ**Docker** - Containerizes the application for consistent deployment across environments.  
ㅤ<img align="center" src="https://icon.icepanel.io/Technology/svg/Grafana.svg" width="17">ㅤ**Grafana** - Monitors application performance with real-time dashboards.  
ㅤ<img align="center" src="https://icon.icepanel.io/Technology/svg/Streamlit.svg" width="17">ㅤ**Streamlit** - Powers the user-friendly interface.  
ㅤ<img align="center" src="https://i.imgur.com/oLTwr0e.png" width="17">ㅤ**Prefect** - Orchestrates data ingestion pipelines.  
ㅤ<img align="center" src="https://docs.cloud.ploomber.io/en/latest/_static/logo.png" width="17">ㅤ**Ploomber Cloud** - Used for hosting and deploying the web application.  

### LLMs Used (for RAG workflow and evaluation)
ㅤ<img align="center" src="https://avatars.githubusercontent.com/u/132372032?s=280&v=4" width="17">ㅤ**Mixtral (mixtral-8x7b-32768)** - Handles large-scale text processing and context-rich answers.  
ㅤ<img align="center" src="https://ai.google.dev/gemma/images/gemma_sq.png?hl=pt-br" width="17">ㅤ**Gemma (gemma-7b-it)** - Reframes user questions for improved response accuracy.  
ㅤ<img align="center" src="https://logopng.com.br/logos/microsoft-92.png" width="17">ㅤ**all-MiniLM-L6-v2** - Performs embeddings and semantic search.  
ㅤ<img align="center" src="https://ollama.com/assets/library/llama3-groq-tool-use/ebf53e82-1faf-4bac-84b0-47b8f5d9d8d1" width="17">ㅤ**Groq** - Processes vectors to retrieve accurate data.  
ㅤ<img align="center" src="https://seeklogo.com/images/P/pinecone-icon-logo-AF8B5B7F96-seeklogo.com.png" width="17">ㅤ**Pinecone** - Manages vector databases for fast, scalable semantic search.  

### Other Tools Used for Development
ㅤ<img align="center" src="https://reverbc.gallerycdn.vsassets.io/extensions/reverbc/vscode-pytest/0.1.1/1617123275355/Microsoft.VisualStudio.Services.Icons.Default" width="17">ㅤ**Pytest** - For unit and integration testing.  
ㅤ<img align="center" src="https://icon.icepanel.io/Technology/svg/Git.svg" width="17">ㅤ**Git** - For version control and collaboration.  
ㅤ<img align="center" src="https://icon.icepanel.io/Technology/svg/Visual-Studio-Code-%28VS-Code%29.svg" width="17">ㅤ**Visual Studio Code** - Used for writing and debugging code.  
ㅤ<img align="center" src="https://icon.icepanel.io/Technology/png-shadow-512/Jupyter.png" width="17">ㅤ**Jupyter Notebook** - Used for dataset processing, vector embeddings, and loading data into Pinecone.  
ㅤ<img align="center" src="https://icon.icepanel.io/Technology/svg/PostgresSQL.svg" width="17">ㅤ**PostgreSQL** - Manages structured data and application logging.  


## 🗂️ Dataset
<p align="justify">The dataset used in the <strong>LoLGA Game Assistant</strong> consists of two columns: one containing questions related to League of Legends universe trivia, such as "Who is Yasuo's brother?" or "What is the relationship between Vi and Jinx?", or even "Which champion has the ability 'The Righteous Fury'?" or "What is the main function of the item 'Serpent's Fang'?", among other questions and their respective answers. This dataset was generated synthetically using tools such as <strong>Mixtral</strong> and <strong>OpenAI (GPT-4)</strong>, which allowed for the creation of a wide range of questions and answers based on the lore and stories of the champions. The dataset is kept up-to-date to include the latest trivia or changes in character relationships as the game's story expands, ensuring that users have access to the most recent information.</p>

> 📌 The dataset contains **1791 questions** about the League of Legends universe, covering topics such as champion names, relationship trivia, class/specialty, ability cooldown times, as well as weapon abilities, classifications, and special and complementary attributes.

## 🌐 Project hosted on Ploomber Cloud [Cloud Platform]
> ☑️ **OBS.**: You may need to "Restart the application" by clicking on Spin up your application, which typically takes less than 2 minutes to complete the "Spinning up" process. This is due to the activity time and maximum period for the application to remain active on the platform.
  
https://blue-block-3250.ploomberapp.io/ <img align="center" src="https://i.imgur.com/tjJFxTd.png" width="21">

## 💻 Project Execution [Locally]
### **Pre-requisites**
➯ Anaconda (latest version)  
➯ Python (latest version)  
➯ Postgree (latest version)  
➯ Grafana (latest version)  
    
### Environment Setup
* Clone the repository:

  ```bash
  git clone https://github.com/victorfxz/Lolga-League-of-Legends-Game-Assistant/
  cd Lolga-League-of-Legends-Game-Assistant
  ```

* Create and activate the virtual environment:
  > ❗ **Note**: This requires the Anaconda Environmentㅤ[ <a href="https://www.anaconda.com/download/success"><img align="center" src="https://github.com/user-attachments/assets/62bb7b30-50ed-4a7c-a427-05718f023c62" width="14"></a> ]

  ```bash
  conda create -n lolga-game-assistant python=3.10
  conda activate lolga-game-assistant
  ```

  > ❗ If you don't have pip installed:
  > ```bash
  > conda install pip
  > ```

* Install all dependencies:

  ```bash
  pip install -r requirements.txt
  ```

### Data Exploration and Preprocessing
* Start the `Langchain_Pinecone_Indexing` notebook with **Jupyter Notebook**:

  ```bash
  jupyter notebook
  ```

### Running the Application
* To run the application, you need to have access keys (API Key) for GroqCloud and Pinecone, creating them and replacing them, and also creating the Index in Pinecone:  <p></p>
  
  > ⚠ㅤYou will need to have an account on both platforms.
  
  »ㅤTo create an API key on GroqCloud [<a href="https://console.groq.com/"><img align="center" src="https://ollama.com/assets/library/llama3-groq-tool-use/ebf53e82-1faf-4bac-84b0-47b8f5d9d8d1" width="21"></a>], create or log in to your account and access the <a href="https://console.groq.com/">site</a> ＞ **API Keys** ＞ **Create API Key**. Copy and save the key in a note-taking app.
  
  <img src="https://i.imgur.com/p2xtXpK.png" width="550">  
  
  »ㅤTo create an API key on Pinecone [<a href="https://console.groq.com/"><img align="center" src="https://seeklogo.com/images/P/pinecone-icon-logo-AF8B5B7F96-seeklogo.com.png" width="16"></a>], create or log in to your account and access the <a href="https://app.pinecone.io/">site</a> ＞ **API keys** ＞ **+ Create API key**. Copy and save the key in a note-taking app.
  
  <img src="https://i.imgur.com/ISSFx9X.png" width="600">  
  
  »ㅤ Still on the Pinecone website, go to **Indexes** ＞ **Create index**. On this page, configure your new index as follows: Default / `lolga`, Configuration ＞ Dimensions ▸ `384` and Metric ▸ `Cosine`, Capacity mode ▸ `Serverless`, Cloud provider ▸ `AWS`, Region ▸ `Virginia | us-east-1` ＞ and finalize by clicking **Create index**.
  
  <img src="https://i.imgur.com/MpF7fFJ.png" width="550">  <p></p>
  
  > ⚠ㅤIn particular, the **Region** can be changed without significant interference in the code, but for the other information, it is necessary to adjust the code considerably.
  
* After completing these steps, add your code to the `.env` files in the `notebook` and `lang-lol-groq` folders.

  `lang-lol-groq ▸ .env`  
  <img src="https://i.imgur.com/V2SIFlM.png" width="350">  
  
  `notebook ▸ .env`  
  <img src="https://i.imgur.com/QSs73ub.png" width="350">  
  
  > ⚠ㅤDon't forget to check if the file extension of the `.env` files is correct (if not, remove the **.txt**), and also update the database information according to your environment.
  
  »ㅤAlso, update the database values as indicated in the images below, in the `prefect_flow.py` files located in the main folder and the `lang-lol-groq` folder:
  
  `(main)` `prefect_flow.py` & `lang-lol-groq ▸ prefect_flow.py`  
  <img src="https://i.imgur.com/dyZk0tQ.png" width="350"> <img src="https://i.imgur.com/hwI7exH.png" width="350">

  > ⚠ㅤ In case of changes to the database information, also update the files inside the `grafana` (folder) ▸ `docker-compose.yaml` and `grafana_datasources.yaml` (inside the `config` subfolder).  
    
* Run the `.env` inside the `lang-lol-groq` > `sql` folder. 
  
  `lang-lol-groq ▸ sql ▸ .env`  
  <img src="https://i.imgur.com/iYYc9s1.png" width="320">  
  
  > ⚠ㅤTo run locally, you need to update the file information according to your environment (also for the Grafana parameters below).
  
* In the **Anaconda Prompt**, , check if you are in the `lang-lol-groq` folder and run the command:
  
  ``` bash
  streamlit run main.py
  ```
  
## More Information
<p align="justify">In the other folders, you will find additional files that were generated or developed during this project. Further information about the Grafana dashboard, including its configuration and visualization, is visually demonstrated in the images and grafana folders.</p>

## Final Consideration
<p align="justify">This chat application, despite being specific to the League of Legends community, can be particularly interesting for individuals who wish to deepen their knowledge of the game and its lore. LoLGA is a useful tool for players of all levels, from beginners to veterans, and can be an excellent option for those seeking a quick and easy way to access information about the game.</p>

This project was developed as the final assignment for the LLM Zoomcamp course.</p>
