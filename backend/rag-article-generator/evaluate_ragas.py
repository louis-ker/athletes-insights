import os
import time
import random
import json
import pandas as pd
from datasets import Dataset

# --- 1. CHARGEMENT ENV ---
from dotenv import load_dotenv
load_dotenv()

# --- 2. IMPORTS ---
# On garde Ragas pour l'évaluation, mais plus pour la génération
from ragas import evaluate
from ragas.metrics import Faithfulness, AnswerRelevancy, ContextPrecision, ContextRecall
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper

# Imports LangChain
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate

# Imports de TON application
from rag_app.config import URLS, DOCS_GLOB, INDEX_DIR, USE_URLS_DEFAULT, USE_FILES_DEFAULT
from rag_app.data import _load_from_urls, _load_from_files, get_retriever
from rag_app.llm import get_llm
from rag_app.router import create_router
from rag_app.graders import create_doc_grader, create_hallucination_grader, create_answer_grader
from rag_app.websearch import get_web_search_tool
from rag_app.workflow import build_graph, run_question

# --- CONFIGURATION ---
TEST_SIZE = 100
OUTPUT_FILE = "ragas_evaluation_report_q100_amelioration_documentGrader.xlsx"

# ---------------------------------------------------------
# 1. PRÉPARATION DES DOCUMENTS
# ---------------------------------------------------------
def prepare_documents():
    print("📚 [Setup] Chargement des documents sources...")
    docs = []
    
    if USE_URLS_DEFAULT:
        print(f"   - Chargement depuis {len(URLS)} URLs...")
        # On utilise ton chargeur mais on nettoie un peu
        raw_docs = _load_from_urls(URLS)
        docs.extend(raw_docs)
    
    if USE_FILES_DEFAULT:
        print(f"   - Chargement depuis glob '{DOCS_GLOB}'...")
        raw_docs = _load_from_files(DOCS_GLOB)
        docs.extend(raw_docs)
        
    # Filtrage simple : on ne garde que les textes qui ont du sens (> 200 chars)
    valid_docs = [d for d in docs if len(d.page_content) > 200]
    
    print(f"✅ [Setup] {len(valid_docs)} documents valides chargés.")
    if not valid_docs:
        raise ValueError("Aucun document valide trouvé.")
        
    return valid_docs

# ---------------------------------------------------------
# 2. GÉNÉRATEUR MAISON (ROBUSTE)
# ---------------------------------------------------------
def generate_custom_testset(documents, size=5):
    """
    Génère des questions/réponses en utilisant directement GPT-4 via LangChain.
    Contourne le générateur instable de Ragas.
    """
    print(f"🧠 [Custom Gen] Génération de {size} questions via GPT-4o...")
    
    llm = ChatOpenAI(model="gpt-4o", temperature=0.7)
    
    # Prompt strict pour forcer le JSON
    prompt = ChatPromptTemplate.from_template("""
    Tu es un expert chargé de créer un examen pour un étudiant.
    Voici un extrait de document :
    ----------------
    {context}
    ----------------
    
    Tâche :
    1. Formule une question CLAIRE et PRÉCISE dont la réponse se trouve dans le texte ci-dessus.
    2. Formule la réponse attendue (Ground Truth).
    
    Format de sortie OBLIGATOIRE (JSON brut sans markdown) :
    {{
        "question": "Ta question ici",
        "ground_truth": "La réponse attendue ici"
    }}
    """)
    
    generated_data = []
    
    # On boucle jusqu'à avoir le nombre de questions voulu
    count = 0
    attempts = 0
    max_attempts = size * 3 # Sécurité pour éviter boucle infinie
    
    while count < size and attempts < max_attempts:
        attempts += 1
        
        # 1. On tire un document au hasard
        doc = random.choice(documents)
        context_text = doc.page_content[:2000] # On tronque pour pas exploser le contexte
        
        try:
            # 2. On appelle GPT-4
            chain = prompt | llm
            response = chain.invoke({"context": context_text})
            content = response.content.replace("```json", "").replace("```", "").strip()
            
            # 3. On parse le JSON
            data = json.loads(content)
            
            # 4. On ajoute à la liste
            generated_data.append({
                "question": data["question"],
                "ground_truth": data["ground_truth"]
            })
            count += 1
            print(f"   - Question {count}/{size} générée.")
            
        except Exception as e:
            print(f"   ⚠️ Échec génération sur ce doc (essai {attempts}): {e}")
            continue

    df = pd.DataFrame(generated_data)
    print(f"✅ [Custom Gen] Terminé. {len(df)} questions prêtes.")
    return df

# ---------------------------------------------------------
# 3. INITIALISATION RAG
# ---------------------------------------------------------
def initialize_rag_app():
    print("🤖 [Student] Initialisation de ton RAG...")
    llm = get_llm(temperature=0)
    # On utilise force_rebuild=False pour gagner du temps
    retriever = get_retriever(INDEX_DIR, URLS, DOCS_GLOB, USE_URLS_DEFAULT, USE_FILES_DEFAULT, False)
    
    router = create_router(llm)
    doc_grader = create_doc_grader(llm)
    hallucination_grader = create_hallucination_grader(llm)
    answer_grader = create_answer_grader(llm)
    web_tool = get_web_search_tool() 

    graph = build_graph(
        retriever, llm, router, doc_grader, hallucination_grader, answer_grader, web_tool, True
    )
    return graph

# ---------------------------------------------------------
# 4. ÉVALUATION ET CORRECTION
# ---------------------------------------------------------
# def evaluate_rag(test_df, graph):
#     print("📝 [Exam] Le RAG passe l'examen...")
    
#     answers = []
#     contexts = []

#     for index, row in test_df.iterrows():
#         q = row["question"]
#         print(f"   Q {index+1}: {q}")
#         try:
#             # On utilise ta fonction modifiée qui renvoie {answer, contexts}
#             res = run_question(graph, q, max_retries=3)
#             answers.append(res["answer"])
#             contexts.append(res["contexts"])
#         except Exception as e:
#             print(f"   ❌ Erreur RAG: {e}")
#             answers.append("Error")
#             contexts.append([])

#     # Préparation pour Ragas
#     # Ragas v0.2 attend : 'user_input', 'response', 'retrieved_contexts', 'reference'
#     data_dict = {
#         "user_input": test_df["question"].tolist(),
#         "response": answers,
#         "retrieved_contexts": contexts,
#         "reference": test_df["ground_truth"].tolist()
#     }
    
#     hf_dataset = Dataset.from_dict(data_dict)
    
#     print("⚖️ [Grading] Le juge (GPT-4o) corrige les copies...")
    
#     # Wrappers indispensables pour Ragas v0.2
#     eval_llm = LangchainLLMWrapper(ChatOpenAI(model="gpt-4o"))
#     eval_embeddings = LangchainEmbeddingsWrapper(OpenAIEmbeddings())
    
#     results = evaluate(
#         hf_dataset,
#         metrics=[Faithfulness(), AnswerRelevancy()],
#         llm=eval_llm,
#         embeddings=eval_embeddings
#     )
    
#     return results

def evaluate_rag(test_df, graph):
    print("📝 [Exam] Le RAG passe l'examen...")
    
    answers = []
    contexts = []
    latencies = [] # <--- NOUVEAU : Liste pour stocker le temps

    for index, row in test_df.iterrows():
        q = row["question"]
        print(f"   Q {index+1}: {q}")
        
        start_time = time.time() # <--- Top départ
        try:
            res = run_question(graph, q, max_retries=3)
            answers.append(res["answer"])
            contexts.append(res["contexts"])
        except Exception as e:
            print(f"   ❌ Erreur RAG: {e}")
            answers.append("Error")
            contexts.append([])
        
        end_time = time.time() # <--- Top fin
        elapsed = end_time - start_time
        latencies.append(elapsed) # On stocke

    # Ajout des résultats dans le dictionnaire Ragas
    data_dict = {
        "user_input": test_df["question"].tolist(),
        "response": answers,
        "retrieved_contexts": contexts,
        "reference": test_df["ground_truth"].tolist()
        # Note: Ragas ne gère pas la latence nativement dans le dataset, 
        # on l'ajoutera au DataFrame final manuellement
    }
    
    hf_dataset = Dataset.from_dict(data_dict)
    
    print("⚖️ [Grading] Le juge (GPT-4o) corrige les copies...")
    
    eval_llm = LangchainLLMWrapper(ChatOpenAI(model="gpt-4o"))
    eval_embeddings = LangchainEmbeddingsWrapper(OpenAIEmbeddings())
    
    # --- MISE À JOUR DES MÉTRIQUES ---
    results = evaluate(
        hf_dataset,
        metrics=[
            Faithfulness(), 
            AnswerRelevancy(),
            ContextPrecision(), # <--- NOUVEAU : Le retriever a-t-il ramené trop de bruit ?
            ContextRecall()     # <--- NOUVEAU : Le retriever a-t-il trouvé la vérité ?
        ],
        llm=eval_llm,
        embeddings=eval_embeddings
    )
    
    # On convertit en Pandas et on ajoute la latence
    df_res = results.to_pandas()
    df_res["latency_seconds"] = latencies # <--- On injecte la colonne latence
    
    return df_res # On retourne directement le DataFrame modifié

# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------
def main():
    try:
        # 1. Docs
        docs = prepare_documents()
        
        # 2. Génération MANUELLE (Plus de crash Ragas ici)
        test_df = generate_custom_testset(docs, size=TEST_SIZE)
        
        # 3. RAG
        graph = initialize_rag_app()
        
        # # 4. Eval
        # results = evaluate_rag(test_df, graph)
        
        # print("\n=== 📊 RÉSULTATS ===")
        # print(results)
        
        # # Export
        # df_res = results.to_pandas()
        # df_res.to_excel(OUTPUT_FILE, index=False)

        # 4. Eval
        df_res = evaluate_rag(test_df, graph) # df_res est déjà le DataFrame
        
        print("\n=== 📊 RÉSULTATS MOYENS ===")
        # Affiche la moyenne de chaque colonne numérique
        print(df_res.mean(numeric_only=True))
        
        # Export
        df_res.to_excel(OUTPUT_FILE, index=False)
        print(f"\n✅ Rapport sauvegardé : {OUTPUT_FILE}")
        
    except Exception as e:
        print(f"\n❌ ERREUR FATALE : {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()