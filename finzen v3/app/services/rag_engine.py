import chromadb
from chromadb.utils import embedding_functions
import os

class FinZenMemory:
    def __init__(self):
        self.client = chromadb.PersistentClient(path="./finzen_memory_db")
        self.ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
        self.collection = self.client.get_or_create_collection(name="user_context", embedding_function=self.ef)

    def memorize(self, text):
        doc_id = str(hash(text))
        self.collection.upsert(documents=[text], ids=[doc_id])

    def recall(self, query):
        results = self.collection.query(query_texts=[query], n_results=2)
        return results['documents'][0] if results['documents'] else []