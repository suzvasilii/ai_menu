import pandas as pd
import faiss
from sentence_transformers import SentenceTransformer
import os

class TextClassifier:
    def __init__(self, csv_path: str = "dishes.csv", model_name: str = "all-MiniLM-L6-v2"):
        self.csv_path = csv_path
        self.model_name = model_name
        self.embedder = None
        self.index = None
        self.categories = []
        self.names = []
        self.dimension = None

        self._load_data()
        self._build_index()

    def _load_data(self):
        if not os.path.exists(self.csv_path):
            return
        df = pd.read_csv(self.csv_path)
        self.names = df["name"].tolist()
        self.categories = df["category"].tolist()
        self.embedder = SentenceTransformer(self.model_name)
        embeddings = self.embedder.encode(self.names, convert_to_numpy=True)
        self.dimension = embeddings.shape[1]
        self._embeddings = embeddings.astype('float32')

    def _build_index(self):
        self.index = faiss.IndexFlatIP(self.dimension)
        self.index.add(self._embeddings)

    def classify(self, query: str, top_k: int = 1) -> str:
        query_embedding = self.embedder.encode([query], convert_to_numpy=True)
        query_embedding = query_embedding.astype('float32')
        distances, indices = self.index.search(query_embedding, top_k)
        best_idx = indices[0][0]
        return self.categories[best_idx]

    def add_item(self, name: str, category: str):
        embedding = self.embedder.encode([name], convert_to_numpy=True)
        embedding = embedding.astype('float32')
        self.index.add(embedding)
        self.names.append(name)
        self.categories.append(category)
        new_row = pd.DataFrame({"name": [name], "category": [category]})
        if os.path.exists(self.csv_path):
            df = pd.read_csv(self.csv_path)
            df = pd.concat([df, new_row], ignore_index=True)
            df.to_csv(self.csv_path, index=False)
        else:
            new_row.to_csv(self.csv_path, index=False)