import os
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings

# The path to the folder where the pre-built index is saved
INDEX_SAVE_PATH = os.path.join(os.path.dirname(__file__), "faiss_index")

class VectorDB:
    def __init__(self):
        """Initializes the vector database by loading a pre-calculated FAISS index."""
        # The embedding model is still needed to understand new user queries
        self.embedding_model = OllamaEmbeddings(model="mxbai-embed-large")

        if not os.path.exists(INDEX_SAVE_PATH):
            raise FileNotFoundError(
                f"FAISS index not found at '{INDEX_SAVE_PATH}'.\n"
                f"Please run the 'python create_index.py' script first to generate it."
            )

        print(f"✅ Loading pre-built FAISS index from '{INDEX_SAVE_PATH}'...")
        # Load the local index, which is very fast
        self.db = FAISS.load_local(
            INDEX_SAVE_PATH,
            self.embedding_model,
            allow_dangerous_deserialization=True # Required by FAISS
        )
        print("✅ Index loaded successfully.")

    def get_db(self):
        """Returns the FAISS database instance."""
        return self.db