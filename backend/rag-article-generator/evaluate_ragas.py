# import os
# import time
# import random
# import json
# import pandas as pd
# from datasets import Dataset

# # --- 1. CHARGEMENT ENV ---
# from dotenv import load_dotenv
# load_dotenv()

# # --- 2. IMPORTS ---
# from ragas import evaluate
# from ragas.metrics import Faithfulness, AnswerRelevancy, ContextPrecision, ContextRecall
# from ragas.llms import LangchainLLMWrapper
# from ragas.embeddings import LangchainEmbeddingsWrapper

# # Imports LangChain
# from langchain_openai import ChatOpenAI, OpenAIEmbeddings
# from langchain_core.prompts import ChatPromptTemplate

# # Imports de TON application
# from rag_app.config import URLS, DOCS_GLOB, INDEX_DIR, USE_URLS_DEFAULT, USE_FILES_DEFAULT
# from rag_app.data import _load_from_urls, _load_from_files, get_retriever
# from rag_app.llm import get_llm
# # from rag_app.router import create_router  <-- SUPPRIMÉ (Optimisation Speculative RAG)
# from rag_app.graders import (
#     create_doc_grader, 
#     create_quality_grader # <-- NOUVEAU (Remplace Hallucination + Answer Grader)
# )
# from rag_app.websearch import get_web_search_tool
# from rag_app.workflow import build_graph, run_question

# # --- CONFIGURATION ---
# TEST_SIZE = 5
# OUTPUT_FILE = "ragas_eval_optimized.xlsx"

# # ---------------------------------------------------------
# # 1. PRÉPARATION DES DOCUMENTS
# # ---------------------------------------------------------
# def prepare_documents():
#     print("📚 [Setup] Chargement des documents sources...")
#     docs = []
    
#     if USE_URLS_DEFAULT:
#         print(f"   - Chargement depuis {len(URLS)} URLs...")
#         raw_docs = _load_from_urls(URLS)
#         docs.extend(raw_docs)
    
#     if USE_FILES_DEFAULT:
#         print(f"   - Chargement depuis glob '{DOCS_GLOB}'...")
#         raw_docs = _load_from_files(DOCS_GLOB)
#         docs.extend(raw_docs)
        
#     valid_docs = [d for d in docs if len(d.page_content) > 200]
    
#     print(f"✅ [Setup] {len(valid_docs)} documents valides chargés.")
#     if not valid_docs:
#         raise ValueError("Aucun document valide trouvé.")
        
#     return valid_docs

# # ---------------------------------------------------------
# # 2. GÉNÉRATEUR MAISON (ROBUSTE)
# # ---------------------------------------------------------
# def generate_custom_testset(documents, size=5):
#     """
#     Génère des questions/réponses via GPT-4o.
#     """
#     print(f"🧠 [Custom Gen] Génération de {size} questions via GPT-4o...")
    
#     llm = ChatOpenAI(model="gpt-4o", temperature=0.7)
    
#     prompt = ChatPromptTemplate.from_template("""
#     Tu es un expert chargé de créer un examen pour un étudiant.
#     Voici un extrait de document :
#     ----------------
#     {context}
#     ----------------
    
#     Tâche :
#     1. Formule une question CLAIRE et PRÉCISE dont la réponse se trouve dans le texte ci-dessus.
#     2. Formule la réponse attendue (Ground Truth).
    
#     Format de sortie OBLIGATOIRE (JSON brut sans markdown) :
#     {{
#         "question": "Ta question ici",
#         "ground_truth": "La réponse attendue ici"
#     }}
#     """)
    
#     generated_data = []
#     count = 0
#     attempts = 0
#     max_attempts = size * 3
    
#     while count < size and attempts < max_attempts:
#         attempts += 1
#         doc = random.choice(documents)
#         context_text = doc.page_content[:2000]
        
#         try:
#             chain = prompt | llm
#             response = chain.invoke({"context": context_text})
#             content = response.content.replace("```json", "").replace("```", "").strip()
#             data = json.loads(content)
            
#             generated_data.append({
#                 "question": data["question"],
#                 "ground_truth": data["ground_truth"]
#             })
#             count += 1
#             print(f"   - Question {count}/{size} générée.")
            
#         except Exception as e:
#             print(f"   ⚠️ Échec génération (essai {attempts}): {e}")
#             continue

#     df = pd.DataFrame(generated_data)
#     return df

# # ---------------------------------------------------------
# # 3. INITIALISATION RAG (MISE À JOUR)
# # ---------------------------------------------------------
# def initialize_rag_app():
#     print("🤖 [Student] Initialisation de ton RAG optimisé...")
#     llm = get_llm(temperature=0)
    
#     # force_rebuild=False pour gagner du temps au lancement
#     retriever = get_retriever(INDEX_DIR, URLS, DOCS_GLOB, USE_URLS_DEFAULT, USE_FILES_DEFAULT, False)
    
#     # --- MODIFICATIONS ICI ---
#     # 1. Plus de Router
#     # 2. Doc Grader (Batch)
#     doc_grader = create_doc_grader(llm)
#     # 3. Quality Grader (Fusionné)
#     quality_grader = create_quality_grader(llm)
    
#     web_tool = get_web_search_tool() 

#     # Mise à jour de l'appel à build_graph
#     graph = build_graph(
#         retriever=retriever, 
#         llm=llm, 
#         # router=router, <-- SUPPRIMÉ
#         doc_grader=doc_grader, 
#         quality_grader=quality_grader, # <-- NOUVEAU
#         web_search_tool=web_tool, 
#         enable_websearch=True
#     )
#     return graph

# # ---------------------------------------------------------
# # 4. ÉVALUATION ET MESURE PERF
# # ---------------------------------------------------------
# def evaluate_rag(test_df, graph):
#     print("📝 [Exam] Le RAG passe l'examen...")
    
#     answers = []
#     contexts = []
#     latencies = [] 

#     for index, row in test_df.iterrows():
#         q = row["question"]
#         print(f"   Q {index+1}: {q}")
        
#         start_time = time.time()
#         try:
#             # max_retries=3 pour laisser la chance à l'autocorrection
#             res = run_question(graph, q, max_retries=3)
#             answers.append(res["answer"])
#             contexts.append(res["contexts"])
#         except Exception as e:
#             print(f"   ❌ Erreur RAG: {e}")
#             answers.append("Error")
#             contexts.append([])
        
#         end_time = time.time()
#         elapsed = end_time - start_time
#         latencies.append(elapsed)
#         print(f"      ⏱️ Temps: {elapsed:.2f}s") # Affichage direct pour monitoring

#     data_dict = {
#         "user_input": test_df["question"].tolist(),
#         "response": answers,
#         "retrieved_contexts": contexts,
#         "reference": test_df["ground_truth"].tolist()
#     }
    
#     hf_dataset = Dataset.from_dict(data_dict)
    
#     print("⚖️ [Grading] Le juge (GPT-4o) corrige les copies...")
    
#     eval_llm = LangchainLLMWrapper(ChatOpenAI(model="gpt-4o"))
#     eval_embeddings = LangchainEmbeddingsWrapper(OpenAIEmbeddings())
    
#     results = evaluate(
#         hf_dataset,
#         metrics=[
#             Faithfulness(), 
#             AnswerRelevancy(),
#             ContextPrecision(),
#             ContextRecall()
#         ],
#         llm=eval_llm,
#         embeddings=eval_embeddings
#     )
    
#     df_res = results.to_pandas()
#     df_res["latency_seconds"] = latencies
    
#     return df_res

# # ---------------------------------------------------------
# # MAIN
# # ---------------------------------------------------------
# def main():
#     try:
#         # 1. Docs
#         docs = prepare_documents()
        
#         # 2. Génération du Test Set
#         test_df = generate_custom_testset(docs, size=TEST_SIZE)
        
#         # 3. Init RAG
#         graph = initialize_rag_app()
        
#         # 4. Eval
#         df_res = evaluate_rag(test_df, graph)
        
#         print("\n=== 📊 RÉSULTATS MOYENS ===")
#         print(df_res.mean(numeric_only=True))
        
#         # Export
#         df_res.to_excel(OUTPUT_FILE, index=False)
#         print(f"\n✅ Rapport sauvegardé : {OUTPUT_FILE}")
        
#     except Exception as e:
#         print(f"\n❌ ERREUR FATALE : {e}")
#         import traceback
#         traceback.print_exc()

# if __name__ == "__main__":
#     main()

"""======================================================="""
# =======================================================
"""======================================================="""
# =======================================================
"""======================================================="""
# =======================================================
"""======================================================="""
# =======================================================
"""======================================================="""

# import os
# import time
# import random
# import json
# import argparse # <--- NOUVEAU
# import pandas as pd
# from datasets import Dataset

# # --- 1. CHARGEMENT ENV ---
# from dotenv import load_dotenv
# load_dotenv()

# # --- 2. IMPORTS ---
# from ragas import evaluate
# from ragas.metrics import Faithfulness, AnswerRelevancy, ContextPrecision, ContextRecall
# from ragas.llms import LangchainLLMWrapper
# from ragas.embeddings import LangchainEmbeddingsWrapper

# # Imports LangChain
# from langchain_openai import ChatOpenAI, OpenAIEmbeddings
# from langchain_core.prompts import ChatPromptTemplate

# # Imports de TON application
# from rag_app.config import URLS, DOCS_GLOB, INDEX_DIR, USE_URLS_DEFAULT, USE_FILES_DEFAULT
# from rag_app.data import _load_from_urls, _load_from_files, get_retriever
# from rag_app.llm import get_llm
# from rag_app.graders import create_doc_grader, create_quality_grader
# from rag_app.websearch import get_web_search_tool
# from rag_app.workflow import build_graph, run_question

# # --- CONFIGURATION ---
# TEST_SIZE = 100
# OUTPUT_FILE = "ragas_eval_comparison.xlsx" # Nom de fichier par défaut

# # ---------------------------------------------------------
# # 1. PRÉPARATION DES DOCUMENTS (Mode Génération)
# # ---------------------------------------------------------
# def prepare_documents():
#     print("📚 [Setup] Chargement des documents sources...")
#     docs = []
    
#     if USE_URLS_DEFAULT:
#         print(f"   - Chargement depuis {len(URLS)} URLs...")
#         raw_docs = _load_from_urls(URLS)
#         docs.extend(raw_docs)
    
#     if USE_FILES_DEFAULT:
#         print(f"   - Chargement depuis glob '{DOCS_GLOB}'...")
#         raw_docs = _load_from_files(DOCS_GLOB)
#         docs.extend(raw_docs)
        
#     valid_docs = [d for d in docs if len(d.page_content) > 200]
    
#     print(f"✅ [Setup] {len(valid_docs)} documents valides chargés.")
#     if not valid_docs:
#         raise ValueError("Aucun document valide trouvé.")
        
#     return valid_docs

# # ---------------------------------------------------------
# # 2. GÉNÉRATEUR MAISON (Mode Génération)
# # ---------------------------------------------------------
# def generate_custom_testset(documents, size=5):
#     print(f"🧠 [Custom Gen] Génération de {size} questions via GPT-4o...")
    
#     llm = ChatOpenAI(model="gpt-4o", temperature=0.7)
    
#     prompt = ChatPromptTemplate.from_template("""
#     Tu es un expert chargé de créer un examen pour un étudiant.
#     Voici un extrait de document :
#     ----------------
#     {context}
#     ----------------
    
#     Tâche :
#     1. Formule une question CLAIRE et PRÉCISE dont la réponse se trouve dans le texte ci-dessus.
#     2. Formule la réponse attendue (Ground Truth).
    
#     Format de sortie OBLIGATOIRE (JSON brut sans markdown) :
#     {{
#         "question": "Ta question ici",
#         "ground_truth": "La réponse attendue ici"
#     }}
#     """)
    
#     generated_data = []
#     count = 0
#     attempts = 0
#     max_attempts = size * 3
    
#     while count < size and attempts < max_attempts:
#         attempts += 1
#         doc = random.choice(documents)
#         context_text = doc.page_content[:2000]
        
#         try:
#             chain = prompt | llm
#             response = chain.invoke({"context": context_text})
#             content = response.content.replace("```json", "").replace("```", "").strip()
#             data = json.loads(content)
            
#             generated_data.append({
#                 "question": data["question"],
#                 "ground_truth": data["ground_truth"]
#             })
#             count += 1
#             print(f"   - Question {count}/{size} générée.")
            
#         except Exception as e:
#             print(f"   ⚠️ Échec génération (essai {attempts}): {e}")
#             continue

#     df = pd.DataFrame(generated_data)
#     return df

# # ---------------------------------------------------------
# # 2-BIS. CHARGEMENT FICHIER EXISTANT (Mode Comparaison)
# # ---------------------------------------------------------
# def load_existing_testset(file_path):
#     """
#     Charge un fichier Excel existant et prépare les colonnes pour l'évaluation.
#     """
#     print(f"📂 [Load] Chargement du dataset existant : {file_path}")
    
#     if not os.path.exists(file_path):
#         raise FileNotFoundError(f"Le fichier {file_path} est introuvable.")
        
#     df = pd.read_excel(file_path)
    
#     # Vérification des colonnes nécessaires
#     required_cols = ["user_input", "reference"]
#     if not all(col in df.columns for col in required_cols):
#         raise ValueError(f"Le fichier Excel doit contenir les colonnes : {required_cols}")
    
#     # On renomme pour correspondre à la logique interne du script
#     # 'user_input' devient 'question'
#     # 'reference' devient 'ground_truth'
#     # On ignore les anciennes réponses et contextes, on veut juste re-tester les questions.
#     df_ready = df.rename(columns={
#         "user_input": "question", 
#         "reference": "ground_truth"
#     })
    
#     print(f"✅ [Load] {len(df_ready)} questions chargées prêtes à être re-testées.")
#     return df_ready[["question", "ground_truth"]]

# # ---------------------------------------------------------
# # 3. INITIALISATION RAG
# # ---------------------------------------------------------
# def initialize_rag_app():
#     print("🤖 [Student] Initialisation de ton RAG optimisé...")
#     llm = get_llm(temperature=0)
#     retriever = get_retriever(INDEX_DIR, URLS, DOCS_GLOB, USE_URLS_DEFAULT, USE_FILES_DEFAULT, False)
    
#     doc_grader = create_doc_grader(llm)
#     quality_grader = create_quality_grader(llm)
#     web_tool = get_web_search_tool() 

#     graph = build_graph(
#         retriever=retriever, 
#         llm=llm, 
#         doc_grader=doc_grader, 
#         quality_grader=quality_grader,
#         web_search_tool=web_tool, 
#         enable_websearch=True
#     )
#     return graph

# # ---------------------------------------------------------
# # 4. ÉVALUATION ET MESURE PERF
# # ---------------------------------------------------------
# def evaluate_rag(test_df, graph):
#     print("📝 [Exam] Le RAG passe l'examen...")
    
#     answers = []
#     contexts = []
#     latencies = [] 

#     for index, row in test_df.iterrows():
#         q = row["question"]
#         print(f"   Q {index+1}: {q}")
        
#         start_time = time.time()
#         try:
#             res = run_question(graph, q, max_retries=3)
#             answers.append(res["answer"])
#             contexts.append(res["contexts"])
#         except Exception as e:
#             print(f"   ❌ Erreur RAG: {e}")
#             answers.append("Error")
#             contexts.append([])
        
#         end_time = time.time()
#         elapsed = end_time - start_time
#         latencies.append(elapsed)
#         print(f"      ⏱️ Temps: {elapsed:.2f}s")

#     data_dict = {
#         "user_input": test_df["question"].tolist(),
#         "response": answers,
#         "retrieved_contexts": contexts,
#         "reference": test_df["ground_truth"].tolist()
#     }
    
#     hf_dataset = Dataset.from_dict(data_dict)
    
#     print("⚖️ [Grading] Le juge (GPT-4o) corrige les copies...")
    
#     eval_llm = LangchainLLMWrapper(ChatOpenAI(model="gpt-4o"))
#     eval_embeddings = LangchainEmbeddingsWrapper(OpenAIEmbeddings())
    
#     results = evaluate(
#         hf_dataset,
#         metrics=[
#             Faithfulness(), 
#             AnswerRelevancy(),
#             ContextPrecision(),
#             ContextRecall()
#         ],
#         llm=eval_llm,
#         embeddings=eval_embeddings
#     )
    
#     df_res = results.to_pandas()
#     df_res["latency_seconds"] = latencies
    
#     return df_res

# # ---------------------------------------------------------
# # MAIN
# # ---------------------------------------------------------
# def main():
#     # Configuration des arguments CLI
#     parser = argparse.ArgumentParser(description="Script d'évaluation RAG")
#     parser.add_argument(
#         "--input", 
#         type=str, 
#         help="Chemin vers un fichier Excel existant (pour rejouer les mêmes questions)",
#         default=None
#     )
#     args = parser.parse_args()

#     try:
#         # --- ETAPE 1 : CHOIX DE LA SOURCE DES QUESTIONS ---
#         if args.input:
#             # Mode Comparaison : On charge l'ancien fichier
#             test_df = load_existing_testset(args.input)
#             output_filename = f"ragas_comparison_{int(time.time())}.xlsx"
#         else:
#             # Mode Génération : On crée de nouvelles questions
#             docs = prepare_documents()
#             test_df = generate_custom_testset(docs, size=TEST_SIZE)
#             output_filename = f"ragas_new_eval_{int(time.time())}.xlsx"

#         # --- ETAPE 2 : INIT RAG ---
#         graph = initialize_rag_app()
        
#         # --- ETAPE 3 : EVALUATION ---
#         df_res = evaluate_rag(test_df, graph)
        
#         print("\n=== 📊 RÉSULTATS MOYENS ===")
#         print(df_res.mean(numeric_only=True))
        
#         # --- ETAPE 4 : EXPORT ---
#         df_res.to_excel(output_filename, index=False)
#         print(f"\n✅ Rapport sauvegardé : {output_filename}")
        
#     except Exception as e:
#         print(f"\n❌ ERREUR FATALE : {e}")
#         import traceback
#         traceback.print_exc()

# if __name__ == "__main__":
#     main()
import os
import time
import random
import json
import argparse
import pandas as pd
from datasets import Dataset

# --- 1. LOAD ENV ---
from dotenv import load_dotenv
load_dotenv()

# --- 2. IMPORTS ---
from ragas import evaluate
from ragas.metrics import Faithfulness, AnswerRelevancy, ContextPrecision, ContextRecall
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper

# LangChain Imports
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage

# YOUR RAG APP IMPORTS
from rag_app.config import URLS, DOCS_GLOB, INDEX_DIR, USE_URLS_DEFAULT, USE_FILES_DEFAULT
from rag_app.data import _load_from_urls, _load_from_files, get_retriever
from rag_app.llm import get_llm
from rag_app.graders import create_doc_grader, create_quality_grader
from rag_app.websearch import get_web_search_tool
from rag_app.workflow import build_graph, run_question

# --- CONFIG ---
TEST_SIZE = 5
OUTPUT_FILE = "ragas_eval_translated.xlsx"

# ---------------------------------------------------------
# HELPER: TRANSLATION
# ---------------------------------------------------------
def translate_text_with_llm(llm, text, target_lang="English"):
    """
    Traduit un texte vers la langue cible en utilisant le LLM.
    """
    if not isinstance(text, str) or not text.strip():
        return ""
        
    prompt = (
        f"Translate the following text to {target_lang}. "
        "Output ONLY the translation, no introduction, no quotes."
        "\n\nText to translate:\n"
        f"{text}"
    )
    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content.strip()

# ---------------------------------------------------------
# 1. PREPARE DOCUMENTS
# ---------------------------------------------------------
def prepare_documents():
    print("📚 [Setup] Loading source documents...")
    docs = []
    
    if USE_URLS_DEFAULT:
        print(f"   - Loading from {len(URLS)} URLs...")
        raw_docs = _load_from_urls(URLS)
        docs.extend(raw_docs)
    
    if USE_FILES_DEFAULT:
        print(f"   - Loading from glob '{DOCS_GLOB}'...")
        raw_docs = _load_from_files(DOCS_GLOB)
        docs.extend(raw_docs)
        
    valid_docs = [d for d in docs if len(d.page_content) > 200]
    
    print(f"✅ [Setup] {len(valid_docs)} valid documents loaded.")
    if not valid_docs:
        raise ValueError("No valid documents found.")
        
    return valid_docs

# ---------------------------------------------------------
# 2. CUSTOM GENERATOR (New questions)
# ---------------------------------------------------------
def generate_custom_testset(documents, size=5):
    print(f"🧠 [Custom Gen] Generating {size} questions via GPT-4o (English)...")
    
    llm = ChatOpenAI(model="gpt-4o", temperature=0.7)
    
    prompt = ChatPromptTemplate.from_template("""
    You are an expert tasked with creating an exam for a student.
    Here is a document excerpt:
    ----------------
    {context}
    ----------------
    
    Task:
    1. Formulate a CLEAR and PRECISE question whose answer is found in the text above. 
       The question MUST be in English.
    2. Formulate the expected answer (Ground Truth). 
       The answer MUST be in English.
    
    REQUIRED Output Format (Raw JSON without markdown):
    {{
        "question": "Your question here",
        "ground_truth": "The expected answer here"
    }}
    """)
    
    generated_data = []
    count = 0
    attempts = 0
    max_attempts = size * 3
    
    while count < size and attempts < max_attempts:
        attempts += 1
        doc = random.choice(documents)
        context_text = doc.page_content[:2000]
        
        try:
            chain = prompt | llm
            response = chain.invoke({"context": context_text})
            content = response.content.replace("```json", "").replace("```", "").strip()
            data = json.loads(content)
            
            print(f"   👉 [CHECK] Generated (EN): {data['question']}")

            generated_data.append({
                "question": data["question"],
                "ground_truth": data["ground_truth"]
            })
            count += 1
            print(f"   - Question {count}/{size} saved.")
            
        except Exception as e:
            print(f"   ⚠️ Generation failed (attempt {attempts}): {e}")
            continue

    df = pd.DataFrame(generated_data)
    return df

# ---------------------------------------------------------
# 2-BIS. LOAD AND TRANSLATE EXISTING FILE
# ---------------------------------------------------------
def load_and_translate_testset(file_path):
    print(f"📂 [Load] Loading existing dataset: {file_path}")
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_path} not found.")
        
    # Détection CSV ou Excel
    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    else:
        df = pd.read_excel(file_path)
    
    required_cols = ["user_input", "reference"]
    if not all(col in df.columns for col in required_cols):
        raise ValueError(f"File must contain columns: {required_cols}. Found: {df.columns.tolist()}")
    
    # Renommage
    df_ready = df.rename(columns={
        "user_input": "question", 
        "reference": "ground_truth"
    })
    
    # --- PHASE DE TRADUCTION ---
    print("\n🌍 [Translation] Translating dataset from French to English via GPT-4o...")
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    
    translated_questions = []
    translated_truths = []
    
    total = len(df_ready)
    
    for idx, row in df_ready.iterrows():
        original_q = row["question"]
        original_gt = row["ground_truth"]
        
        # 1. Traduction Question
        trans_q = translate_text_with_llm(llm, original_q)
        
        # 2. Traduction Vérité Terrain (Ground Truth)
        trans_gt = translate_text_with_llm(llm, original_gt)
        
        # --- PRINT DE VÉRIFICATION ---
        print(f"   [{idx+1}/{total}] FR: {original_q[:50]}...  -->  🇺🇸 EN: {trans_q}")
        
        translated_questions.append(trans_q)
        translated_truths.append(trans_gt)
    
    # Remplacement des colonnes par les versions anglaises
    df_ready["question"] = translated_questions
    df_ready["ground_truth"] = translated_truths
    
    print(f"✅ [Translation] Translation complete for {total} items.\n")
    return df_ready[["question", "ground_truth"]]

# ---------------------------------------------------------
# 3. INIT RAG
# ---------------------------------------------------------
def initialize_rag_app():
    print("🤖 [Student] Initializing Optimized RAG...")
    llm = get_llm(temperature=0)
    retriever = get_retriever(INDEX_DIR, URLS, DOCS_GLOB, USE_URLS_DEFAULT, USE_FILES_DEFAULT, False)
    
    doc_grader = create_doc_grader(llm)
    quality_grader = create_quality_grader(llm)
    web_tool = get_web_search_tool() 

    graph = build_graph(
        retriever=retriever, 
        llm=llm, 
        doc_grader=doc_grader, 
        quality_grader=quality_grader,
        web_search_tool=web_tool, 
        enable_websearch=True
    )
    return graph

# ---------------------------------------------------------
# 4. EVALUATION
# ---------------------------------------------------------
def evaluate_rag(test_df, graph):
    print("📝 [Exam] RAG is taking the exam (in English)...")
    
    answers = []
    contexts = []
    latencies = [] 

    for index, row in test_df.iterrows():
        q = row["question"]
        print(f"   Q {index+1}: {q}")
        
        start_time = time.time()
        try:
            res = run_question(graph, q, max_retries=3)
            answers.append(res["answer"])
            contexts.append(res["contexts"])
        except Exception as e:
            print(f"   ❌ RAG Error: {e}")
            answers.append("Error")
            contexts.append([])
        
        end_time = time.time()
        elapsed = end_time - start_time
        latencies.append(elapsed)
        print(f"      ⏱️ Time: {elapsed:.2f}s")

    data_dict = {
        "user_input": test_df["question"].tolist(),
        "response": answers,
        "retrieved_contexts": contexts,
        "reference": test_df["ground_truth"].tolist()
    }
    
    hf_dataset = Dataset.from_dict(data_dict)
    
    print("⚖️ [Grading] The Judge (GPT-4o) is grading...")
    
    eval_llm = LangchainLLMWrapper(ChatOpenAI(model="gpt-4o"))
    eval_embeddings = LangchainEmbeddingsWrapper(OpenAIEmbeddings())
    
    results = evaluate(
        hf_dataset,
        metrics=[
            Faithfulness(), 
            AnswerRelevancy(),
            ContextPrecision(),
            ContextRecall()
        ],
        llm=eval_llm,
        embeddings=eval_embeddings
    )
    
    df_res = results.to_pandas()
    df_res["latency_seconds"] = latencies
    
    return df_res

# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="RAG Evaluation Script")
    parser.add_argument("--input", type=str, help="Path to existing Excel/CSV file (will be translated)", default=None)
    args = parser.parse_args()

    try:
        # 1. SOURCE SELECTION & TRANSLATION
        if args.input:
            # Mode Traduction + Évaluation
            test_df = load_and_translate_testset(args.input)
            output_filename = f"ragas_translated_eval_{int(time.time())}.xlsx"
        else:
            # Mode Génération (déjà en anglais)
            docs = prepare_documents()
            test_df = generate_custom_testset(docs, size=TEST_SIZE)
            output_filename = f"ragas_new_eval_{int(time.time())}.xlsx"

        # 2. INIT RAG
        graph = initialize_rag_app()
        
        # 3. EVALUATION
        df_res = evaluate_rag(test_df, graph)
        
        # 4. HANDLE NaNs
        metrics = ["faithfulness", "answer_relevancy", "context_precision", "context_recall"]
        df_clean = df_res.fillna({m: 0.0 for m in metrics})
        
        print("\n=== 📊 AVERAGE SCORES (NaN = 0) ===")
        print(df_clean[metrics + ["latency_seconds"]].mean())
        
        # 5. EXPORT
        df_res.to_excel(output_filename, index=False)
        print(f"\n✅ Report saved: {output_filename}")
        
    except Exception as e:
        print(f"\n❌ FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()