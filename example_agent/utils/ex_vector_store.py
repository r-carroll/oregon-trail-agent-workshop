import os

from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_ollama import OllamaEmbeddings
from langchain_redis import RedisConfig, RedisVectorStore

load_dotenv()

REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
INDEX_NAME = os.environ.get("VECTOR_INDEX_NAME", "oregon_trail")

config = RedisConfig(index_name=INDEX_NAME, redis_url=REDIS_URL)

doc = Document(
    page_content="the northern trail, of the blue mountains, was destroyed by a flood and is no longer safe to traverse. It is recommended to take the southern trail although it is longer."
)


def get_vector_store():
    openai_embedding = OpenAIEmbeddings()
    ollama_write_embedding = OllamaEmbeddings(model="nomic-embed-text")
    ollama_read_embedding = OllamaEmbeddings(model="llama3")

    if os.environ.get("MODEL_NAME") == "openai":
        try:
            config.from_existing = True
            vector_store = RedisVectorStore(openai_embedding, config=config)
        except:
            print("Init vector store with document")
            config.from_existing = False
            vector_store = RedisVectorStore.from_documents(
                [doc], openai_embedding, config=config
            )
    elif os.environ.get("MODEL_NAME") == "openai":
        try:
            config.from_existing = True
            vector_store = RedisVectorStore(embeddings=ollama_read_embedding, config=config)
            results = vector_store.similarity_search(doc, k=1)
            if not results:
                raise Exception("Required content not found in existing store")
        except:
            print("Init vector store with document")
            config.from_existing = False
            vector_store = RedisVectorStore.from_documents(
                [doc], ollama_write_embedding, config=config
            )
    return vector_store
