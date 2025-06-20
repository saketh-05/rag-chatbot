from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import os
import pandas as pd

df = pd.read_csv("onepiece-epdata.csv")

embeddings = OllamaEmbeddings(model="mxbai-embed-large")

db_location = "./chroma_langchain_db"

add_documents = not os.path.exists(db_location)

if(add_documents):
    documents = []
    ids = []
    
    for i,row in df.iterrows():
        document = Document(
            page_content = "Episode number: " + str(row["episode"]) + "Episode name: " + row["name"] + "Episode rating: " + str(row["average_rating"]),
            metadata = {
                "episode": row["episode"],
                "name": row["name"],
                "total_votes": row["total_votes"],
                "rating": row["average_rating"],
            }
        )
        ids.append(str(row["episode"]))
        documents.append(document)
        

vector_store = Chroma(
    collection_name="onepiece-episodes",
    persist_directory=db_location,
    embedding_function=embeddings
)

if add_documents:
    vector_store.add_documents(documents=documents, ids=ids)

retriever = vector_store.as_retriever(
    search_kwargs={"k" : 10}
)