import os
import pandas as pd
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from langchain.docstore.document import Document

# --- Configuration ---
CSV_PATH = os.path.join("chatbot", "etablissements_sante_mentale_maroc.csv")
INDEX_SAVE_PATH = os.path.join("chatbot", "faiss_index")

def create_document_from_row(row):
    """Creates a Document object from a row, handling empty values."""
    parts = []
    if 'nom' in row and pd.notna(row['nom']):
        parts.append(f"Nom: {row['nom']}")
    if 'type_etablissement' in row and pd.notna(row['type_etablissement']):
        parts.append(f"Type: {row['type_etablissement']}")
    if 'ville' in row and pd.notna(row['ville']):
        parts.append(f"Ville: {row['ville']}")
    if 'adresse' in row and pd.notna(row['adresse']):
        parts.append(f"Adresse: {row['adresse']}")
    if 'telephone' in row and pd.notna(row['telephone']):
        parts.append(f"Téléphone: {row['telephone']}")

    if not parts:
        return None

    content = "\n".join(parts)
    return Document(page_content=content, metadata=row.to_dict())

if __name__ == "__main__":
    print("🚀 Starting FAISS index creation...")
    print(f"Reading data from '{CSV_PATH}'")
    print("This is a one-time process and will take a long time (approx. 30-40 minutes).")

    # 1. Read the CSV data
    df = pd.read_csv(CSV_PATH)
    documents = [doc for doc in df.apply(create_document_from_row, axis=1) if doc]

    # 2. Initialize the embedding model
    embeddings = OllamaEmbeddings(model="mxbai-embed-large")

    # 3. Create the FAISS index (this is the slow part)
    vector_store = FAISS.from_documents(documents, embeddings)

    # 4. Save the completed index to disk
    vector_store.save_local(INDEX_SAVE_PATH)

    print(f"\n✅ Index created and saved successfully in '{INDEX_SAVE_PATH}'")
    print("You can now start the main app with 'python main.py'")