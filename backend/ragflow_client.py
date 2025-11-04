from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv() 

RAGFLOW_API_KEY = os.getenv("RAGFLOW_API_KEY")
RAGFLOW_ADDRESS = os.getenv("RAGFLOW_ADDRESS")
CHAT_ID = os.getenv("CHAT_ID")

# client = OpenAI(
#     api_key=RAGFLOW_API_KEY,
#     base_url=f"{RAGFLOW_ADDRESS}/api/v1/chats_openai/{CHAT_ID}"
# )

# def ask_ragflow(question, session_id="default"):
#     try:
#         completion = client.chat.completions.create(
#             model="model",
#             messages=[{"role": "user", "content": question}],
#             stream=False,
#             extra_body={"reference": True}
#         )

#         choice = completion.choices[0]
#         message = choice.message  # C’est un objet, pas un dict

#         content = getattr(message, "content", "")
#         reference = getattr(message, "reference", "")

#         # Renvoyer le texte et la référence s’ils existent
#         if reference:
#             return f"{content}\n\n📄 Source : {reference}"
#         else:
#             return content or "(aucune réponse retournée)"

#     except Exception as e:
#         return f"Erreur RAGFlow : {e}"

client = OpenAI(
    api_key=RAGFLOW_API_KEY,
    base_url=f"{RAGFLOW_ADDRESS}/api/v1/chats_openai/{CHAT_ID}"
)

def ask_ragflow(question, session_id="default"):
    """
    Envoie une requête à RAGFlow et renvoie une réponse structurée :
    {
        "answer": "...",
        "sources": [...]
    }
    """
    try:
        completion = client.chat.completions.create(
            model="model",
            messages=[{"role": "user", "content": question}],
            stream=False,
            extra_body={"reference": True}
        )

        # On récupère la première réponse
        choice = completion.choices[0]
        message = getattr(choice, "message", None)

        if not message:
            return {"answer": "(aucune réponse retournée)", "sources": []}

        # Récupération du contenu principal
        answer = getattr(message, "content", "").strip()

        # Récupération des sources si elles existent
        references = getattr(message, "reference", [])
        if isinstance(references, str):
            # Si RAGFlow renvoie du JSON en texte
            import json
            try:
                references = json.loads(references)
            except json.JSONDecodeError:
                references = []

        # Structure finale
        return {
            "answer": answer or "(aucune réponse retournée)",
            "sources": references
        }

    except Exception as e:
        return {
            "answer": f"[Erreur RAGFlow] Le serveur ne tourne pas : {e}",
            "sources": []
        }
