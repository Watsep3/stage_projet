# chatbot/chatbot_memory.py

from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain_ollama import ChatOllama

class ChatbotMemory:
    def __init__(self, db):
        # --- Charger le modèle de chat depuis Ollama ---
        llm = ChatOllama(model="llama3.2:1b", temperature=0.7)
        

        # Le reste du code est identique
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        self.retriever = db.get_db().as_retriever(search_kwargs={"k": 3}) # Augmenté à 3 pour plus de contexte

        custom_template = """
        Vous êtes un assistant spécialisé dans la santé mentale au Maroc.
        Utilisez les informations de contexte suivantes pour répondre de manière concise à la question de l'utilisateur.
        Si vous ne connaissez pas la réponse, dites simplement que vous n'avez pas cette information dans vos documents. N'inventez rien.
        Répondez toujours en français.

        Contexte: {context}
        Historique de la conversation: {chat_history}
        Question: {question}
        Réponse:
        """
        CUSTOM_QUESTION_PROMPT = PromptTemplate.from_template(custom_template)

        self.conversation = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=self.retriever,
            memory=self.memory,
            combine_docs_chain_kwargs={"prompt": CUSTOM_QUESTION_PROMPT}
        )

    def ask(self, query):
        response = self.conversation({"question": query})
        return response["answer"]