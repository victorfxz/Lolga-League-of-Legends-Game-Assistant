# LoLGA - League of Legends Game Assistant

<p align="center"><img src="https://github.com/user-attachments/assets/62ee397a-334a-46df-b756-b7363eaf224b" width="269"><img src="https://github.com/user-attachments/assets/1a0951c6-ca8b-4c34-8d3e-7ed8f33a8a0a" width="700"></p>

## Project Overview
<p align="justify">League of Legends (LoL) é um jogo rico em história, personagens e curiosidades que nem sempre estão prontamente disponíveis para os jogadores. Muitos fãs se interessam por detalhes como as relações entre campeões, histórias de fundo, e outros fatos curiosos sobre o universo do jogo. O LoLGA Game Assistant foi criado para solucionar esse problema, fornecendo um assistente que responde de maneira rápida e precisa a perguntas sobre curiosidades do jogo. Utilizando a tecnologia RAG (Retrieval-Augmented Generation), o aplicativo permite que os usuários façam perguntas e obtenham respostas detalhadas sobre o lore e os personagens de LoL, atendendo tanto a curiosos quanto a jogadores mais envolvidos com o universo do game.</p>

> 📍 Base de dados de texto que, durante o processo, foi transformado em uma base de dados vetorial.

## Problem Description
<p align="justify">League of Legends (LoL) é um jogo rico em história, personagens e curiosidades que nem sempre estão prontamente disponíveis para os jogadores. Muitos fãs se interessam por detalhes como as relações entre campeões, histórias de fundo, e outros fatos curiosos sobre o universo do jogo. O LoLGA Game Assistant foi criado para solucionar esse problema, fornecendo um assistente que responde de maneira rápida e precisa a perguntas sobre curiosidades do jogo. Utilizando a tecnologia RAG (Retrieval-Augmented Generation), o aplicativo permite que os usuários façam perguntas e obtenham respostas detalhadas sobre o lore e os personagens de LoL, atendendo tanto a curiosos quanto a jogadores mais envolvidos com o universo do game.</p>

## Technologies and Tools Used
### Key Technologies
ㅤ<img img align="center" src="https://github.com/user-attachments/assets/d48aa56b-bce1-404d-9b72-25632905c001" width="16">ㅤ**Anaconda** - Used for package management and creating the virtual environment  
ㅤ<img img align="center" src="https://github.com/user-attachments/assets/ec87d23a-028b-43f1-b739-8195e256c817" width="16">ㅤ**Docker** - Used for containerization of the application  
ㅤ<img img align="center" src="https://github.com/user-attachments/assets/27fb21a1-33bb-478e-b755-e33bec6c3bbf" width="16">ㅤ**Grafana** - Usado para o monitoramento do aplicativo  
ㅤ<img img align="center" src="https://streamlit.io/images/brand/streamlit-mark-color.png" width="16">ㅤ**Streamlit** - Usado para a criação da interface gráfica  
ㅤ<img img align="center" src="https://i.imgur.com/oLTwr0e.png" width="16">ㅤ**Prefect** - Usado para pipeline de ingestão  
ㅤ<img img align="center" src="https://docs.cloud.ploomber.io/en/latest/_static/logo.png" width="16">ㅤ**Ploomber Cloud** - Used as a cloud-based web application hosting and deployment platform  

### LLMs Used (para o fluxo e avaliação RAG)
ㅤ<img img align="center" src="https://avatars.githubusercontent.com/u/132372032?s=280&v=4" width="16">ㅤ**Mixtral (mixtral-8x7b-32768)** - Usado para recuperação aumentada, ou seja, processar grandes volumes de texto e fornecer respostas contextuais mais profundas sobre o jogo  
ㅤ<img img align="center" src="https://github.com/user-attachments/assets/b86cf3b7-4d29-4cfd-88fb-1c5950ea506b" width="16">ㅤ**Gemma (gemma-7b-it)** - Usado para reformulação das questões  
ㅤ<img img align="center" src="https://logopng.com.br/logos/microsoft-92.png" width="16">ㅤ**all-MiniLM-L6-v2** - Usado para realizar o embeddings e para busca semântica  
ㅤ<img img align="center" src="https://ollama.com/assets/library/llama3-groq-tool-use/ebf53e82-1faf-4bac-84b0-47b8f5d9d8d1" width="16">ㅤ**Groq** - Usado para consumir os LLMs utilizados no projeto  
ㅤ<img img align="center" src="https://github.com/user-attachments/assets/752078ac-220c-4c9d-8c8f-4692471a7c31" width="16">ㅤ**Pinecone** - Usado como banco de dados vetorial  

### Other Tools Used for Development
ㅤ<img img align="center" src="https://reverbc.gallerycdn.vsassets.io/extensions/reverbc/vscode-pytest/0.1.1/1617123275355/Microsoft.VisualStudio.Services.Icons.Default" width="16">ㅤ**Pytest** - Usado para realizar os testes  
ㅤ<img img align="center" src="https://github.com/user-attachments/assets/ec1b86c6-492f-4345-ad16-6dc138b990c3" width="16">ㅤ**Git** - Used for version control  
ㅤ<img img align="center" src="https://github.com/user-attachments/assets/704b646c-58ae-426d-8f1c-e7c2c7fc964b" width="16">ㅤ**Visual Studio Code** - Usado para codificar o aplicativo web  
ㅤ<img img align="center" src="https://github.com/user-attachments/assets/d3eee82b-8a6b-4789-8182-d4d6816f0273" width="16">ㅤ**Jupyter Notebook** - Usado para carregar o dataset, fazer os chunks, criar os embadins e enviar para o banco de dados vetorial Pinecone  
ㅤ<img img align="center" src="https://github.com/user-attachments/assets/52316734-849b-4f46-8bf8-6a7f839405af" width="16">ㅤ**PostgreSQL** - Usado para armazenar o monitoramento  


## Dataset
<p align="justify">O dataset utilizado no LoLGA Game Assistant é composto por duas colunas: uma contendo perguntas relacionadas a curiosidades do universo de League of Legends, como "Quem é o irmão de Yasuo?" ou "Qual é a relação entre Vi e Jinx?", ou, ainda, "Which champion has the ability 'The Righteous Fury'?" ou  "What is the main function of the item 'Serpent's Fang'?", entre outras questões e suas respectivas respostas. Este dataset foi gerado de forma sintética utilizando ferramentas como Mixtral e OpenAI (GPT-4), o que permitiu a criação de uma vasta gama de perguntas e respostas com base no lore e nas histórias dos campeões. O dataset está atualizado, para incluir as mais recentes curiosidades ou mudanças nas relações dos personagens à medida que a história do jogo se expande, garantindo que os usuários tenham acesso às informações mais recentes.</p>

> 📌 O dataset possui **1791 perguntas** sobre o universo de LoL, desde nomes, curiosidadades sobre relacionamentos, classe/especialidade e tempo de recarga de habilidades dos campiões como também habilidades de armas e suas classificações e atributos especiais e complementares.

## Project hosted on Ploomber Cloud [Cloud Platform] <img align="center" src="https://github.com/user-attachments/assets/9935d5f6-5555-4f39-a69f-093dffcc28c3" width="34">
https://broken-wind-4798.ploomberapp.io/

## Project Execution [Locally] 💻
### **Pre-requisites**

* Anaconda (latest version)
* Python (latest version)
* Postgree (latest version)
* Grafana (latest version)
  
### Environment Setup
Clone the repository:

```bash
git clone https://github.com/victorfxz/Lolga-League-of-Legends-Game-Assistant/
cd Lolga-League-of-Legends-Game-Assistant
```

Create and activate the virtual environment:
> ❗ **Note**: This requires the Anaconda Environmentㅤ[ <a href="https://www.anaconda.com/download/success"><img src="https://github.com/user-attachments/assets/62bb7b30-50ed-4a7c-a427-05718f023c62" width="14"></a> ]

```bash
conda create -n lolga-game-assistant python=3.10
conda activate lolga-game-assistant
```

> ❗ If you don't have pip installed:
> ```bash
> conda install pip
> ```

Install all dependencies:

```bash
pip install -r requirements.txt
```

### Data Exploration and Preprocessing
Start the `Langchain_Pinecone_Indexing` notebook with Jupyter Notebook:

```bash
jupyter notebook
```

### Running the Application
1. Para rodar o aplicativo é necessário que você possua as chaves de acesso (API Key) no GroqCloud e Pinecone, criando-as e substituindo-as, e, também, criar o Index no Pinecone:

> ⚠️ Será necessário ter uma conta em ambas as plataformas.

* Para criar a key no GroqCloud, crie ou logue na sua conta e acesse o <a href="https://console.groq.com/">site</a> > API Keys > Create API Key. Copie e salve a Key em algum bloco de notas.

  <img src="https://github.com/user-attachments/assets/80fbe038-0537-4eec-8a0b-7227acb62ef3" width="550"></p>

* Para criar a key no Pinecone, crie ou logue na sua conta e acesse o <a href="https://app.pinecone.io/">site</a> > API keys > + Create API key. Copie e salve a Key em algum bloco de notas.

  <img src="https://github.com/user-attachments/assets/6c22c109-c2fa-45a4-b2f3-2ff09e466eec" width="600"></p>

* Ainda no site do Pinecone, vá em **Indexes** > **Create index**. Dentro desta página, configure da seguinte maneira: 'Default / `lolga`', Configuration > 'Dimensions `384`' e 'Metric `Cosine`', 'Capacity mode `Serverless`', 'Cloud provider `AWS`', 'Region `Virginia | us-east-1`' > e finalize clicando em **`Create index`**.

  <img src="https://github.com/user-attachments/assets/80c58040-16cc-4fec-94c9-69fa6b5d0880" width="550"></p>

> ⚠️ Em especial, a **região** pode ser alterada sem interferencias consideraveis no código; já para as outras informações, é necessário ajustar consideravelmente o código e sua estrutura.

Após ter executado esses etapas, adicione o seu código nos arquivos `.env` das pasta `notebook` e `lang-lol-groq`, conforme demonstrado, respectivamente, abaixo:

<img src="https://github.com/user-attachments/assets/5fff51e9-499d-44ba-9b63-0c579afe2cfc" width="350"></p>
<img src="https://github.com/user-attachments/assets/e389f262-981f-4cf0-8958-8d6b79fbf7d6" width="350"></p>

> ⚠️ Caso necessário, também altere os dados sobre o banco de dados conforme o seu ambiente.

2. Execute o arquivo **´.env´** dentro da pasta `lang-lol-groq` > `sql`

  <img src="https://github.com/user-attachments/assets/d6b77605-234e-4c15-9db1-2457e4ff3946" width="320"></p>

> ⚠️ Para executar localmente, é necessário alterar os dados do arquivo conforme o seu ambiente (igualmente para os parâmetros do Grafana, logo abaixo).

3. No **Anaconda Prompt**, confira se está na pasta `lang-lol-groq` e execute o comando:

``` bash
streamlit run main.py
```

## More Information
<p align="justify">In the other folders, you will find additional files that were generated or developed during this project. Further information on the usage of Grafana and Prefect can be found in the `` folder.</p>

## Final Consideration
<p align="justify">This prediction model, despite its specific segment, can be particularly interesting for people who wish to live in the city of São Paulo and want a general or location-specific estimate of apartment rental prices based on coordinates.

This project was developed as the final assignment for the LLM Zoomcamp course.</p>


