# Vietnamese Legal Chatbot
## Overview
![demo app](asset\demo.png)

[Watch video demo]([asset\video.mp4](https://www.facebook.com/khang.luu.56884))

This project implements a Retrieval-Augmented Generation (RAG) pipeline, enabling users to ask about Vietnamese Law on Marriage and Family. The chatbot is powered by **Gemini**, or local models accessible through **Ollama**, retrieving relevant information and using **Large Language Models (LLMs)** to enhance responses based on user queries. 

## Feature

1. **Qdrant-based storage and retrieval** - Uses Qdrant to store vector embeddings and perform efficient **hybrid searches**.
2. **Interactive Chatbot** - Chatbot interaction is enhanced by Gemini, or local LLMs to generate context-aware responses.
3. **Semantic chunking** - Provide semantic chunking strategy
4. **Condense mode** - Refine user questions for better performance.
5. **Diverse legal database** - Laws, Decrees, Circulars, the Constitution, Regulations, and Guidelines on the Law on Marriage and Family.
6. **Fine-tuned embeding model** - Use customized embedding model or for Marriage and Family Law field.
7. **Acessibility** - Access by either web or messenger
8. **Hybrid Search** - Combine **Semantic seach** and **Keyword search** to enhace retrieval

# Run the Application
## 1. Requirement
- Your own QdrantDB(cause I use local on Docker)
- requirement
## 2. Clone the Repo
``` bash
git clone https://github.com/khangsilly21/Project-2-Vietnamese-Legal-Chatbot.git
cd Project-2-Vietnamese-Legal-Chatbot
```
## 3. Install Requirement
- You can ultilize `example` repository to build your own Qdrant vector database

``` bash
pip install -r requirement.txt
```
## 4. Run the Streamlit App

``` bash
streamlit run streamlitapp.py
```
> You can deploy rapidly on messenger by [ngrok](https://ngrok.com/) and code in `app`

 
