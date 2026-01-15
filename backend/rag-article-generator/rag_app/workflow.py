from typing import Dict, Any, List

from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage
from langchain_core.documents import Document

from .types import GraphState
from .prompts import RAG_PROMPT
from .utils import format_docs
# from .router import route_decision
# from .graders import grade_document_relevance, grade_hallucination, grade_answer
# from .graders import grade_documents_batch, grade_hallucination, grade_answer
from .graders import grade_documents_batch, grade_generation_quality

import json
import pandas as pd
import os
from openai import OpenAI

import concurrent.futures


def build_graph(
    retriever,
    llm,
    # router,
    doc_grader,
    quality_grader,
    # hallucination_grader,
    # answer_grader,
    web_search_tool,
    enable_websearch: bool = True,   # <<< nouveau paramètre
):
    """
    Construit et compile le graphe LangGraph.
    Si `enable_websearch=False`, le noeud websearch est retiré et le routage est forcé sur RAG.
    """

    # ---------- NODES ----------

    def web_search(state: Dict[str, Any]):
        print("---WEB SEARCH---")
        question = state["question"]
        documents = state.get("documents", [])
        
        if web_search_tool is None:
            print("[websearch] Désactivé (aucun outil).")
            return {"documents": documents}
            
        docs = web_search_tool.invoke({"query": question})
        
        # --- DÉBUT CORRECTIF ---
        web_results = ""
        # Cas 1 : Tavily renvoie une liste de Strings (nouveau comportement)
        if isinstance(docs, list) and len(docs) > 0 and isinstance(docs[0], str):
            web_results = "\n".join(docs)
        # Cas 2 : Tavily renvoie une liste de Dictionnaires (ancien comportement)
        elif isinstance(docs, list) and len(docs) > 0 and isinstance(docs[0], dict):
            web_results = "\n".join([d.get("content", "") for d in docs])
        # Cas 3 : Autre format inattendu
        else:
            web_results = str(docs)
        # --- FIN CORRECTIF ---

        documents.append(Document(page_content=web_results))
        return {"documents": documents}

    def retrieve(state: Dict[str, Any]):
        print("---RETRIEVE---")
        raw_question = state["question"]
        
        # --- DÉBUT NETTOYAGE ---
        # On extrait la vraie question des instructions du prompt
        if "Question spécifique :" in raw_question:
            search_query = raw_question.split("Question spécifique :")[-1].strip()
        elif "Question principale :" in raw_question:
            search_query = raw_question.split("Question principale :")[-1].strip()
        else:
            search_query = raw_question
        # --- FIN NETTOYAGE ---

        print(f"[retrieve] Recherche nettoyée : '{search_query}'")
        
        documents = retriever.invoke(search_query)
        return {"documents": documents}

    # def grade_documents(state: Dict[str, Any]):
    #     print("---CHECK DOCUMENT RELEVANCE TO QUESTION---")
    #     question = state["question"]
    #     documents = state["documents"]

    #     # AJOUT TEMPORAIRE DE DEBUG
    #     print(f"\n[DEBUG] Documents trouvés pour '{state['question']}':")
    #     for i, d in enumerate(documents):
    #         print(f"--- Doc {i} (extrait): {d.page_content[:200]}...")
    #     # FIN AJOUT

    #     filtered_docs = []
    #     web_search_flag = "No"
    #     for d in documents:
    #         grade = grade_document_relevance(doc_grader, d.page_content, question)
    #         if grade == "yes":
    #             print("---GRADE: DOCUMENT RELEVANT---")
    #             filtered_docs.append(d)
    #         else:
    #             print("---GRADE: DOCUMENT NOT RELEVANT---")
    #             if enable_websearch:
    #                 web_search_flag = "Yes"
    #     return {"documents": filtered_docs, "web_search": web_search_flag}

    # def grade_documents(state: Dict[str, Any]):
    #     print("---CHECK DOCUMENT RELEVANCE (BATCH)---")
    #     question = state["question"]
    #     documents = state["documents"]
        
    #     # S'il n'y a pas de documents, on sort direct
    #     if not documents:
    #         return {"documents": [], "web_search": "Yes" if enable_websearch else "No"}

    #     # 1. APPEL LLM UNIQUE (Batch)
    #     scores_dict = grade_documents_batch(doc_grader, documents, question)
        
    #     filtered_docs = []
    #     web_search_flag = "No"
        
    #     # 2. On itère localement (super rapide, pas d'appel LLM)
    #     for i, d in enumerate(documents):
    #         # On récupère le score via l'index. Par défaut "no" si le LLM a oublié l'index.
    #         score = scores_dict.get(i, "no")
            
    #         if score == "yes":
    #             print(f"---GRADE: Doc {i} RELEVANT---")
    #             filtered_docs.append(d)
    #         else:
    #             print(f"---GRADE: Doc {i} NOT RELEVANT---")
        
    #     # 3. Logique de déclenchement Web Search
    #     # OPTIMISATION: On ne déclenche Web Search que si on a perdu TROP de documents
    #     # Exemple : Si on a 0 pertinent, ou si on a récupéré moins de 1 doc valide
    #     if len(filtered_docs) == 0:
    #         if enable_websearch:
    #             print("---DECISION: ALL DOCS IRRELEVANT -> WEB SEARCH---")
    #             web_search_flag = "Yes"
        
    #     return {"documents": filtered_docs, "web_search": web_search_flag}

    def grade_documents(state: Dict[str, Any]):
        print("---CHECK DOCUMENT RELEVANCE (BATCH)---")
        question = state["question"]
        documents = state["documents"]
        
        # S'il n'y a pas de documents au départ, web search direct
        if not documents:
            return {"documents": [], "web_search": "Yes" if enable_websearch else "No"}

        # 1. APPEL LLM UNIQUE (Batch)
        scores_dict = grade_documents_batch(doc_grader, documents, question)
        
        filtered_docs = []
        web_search_flag = "No"
        
        # 2. On filtre les documents
        for i, d in enumerate(documents):
            score = scores_dict.get(i, "no")
            
            if score == "yes":
                print(f"---GRADE: Doc {i} RELEVANT---")
                filtered_docs.append(d)
            else:
                print(f"---GRADE: Doc {i} NOT RELEVANT---")
                # ANCIEN CODE SUPPRIMÉ :
                # if enable_websearch: web_search_flag = "Yes"
        
        # 3. NOUVELLE LOGIQUE DE DÉCLENCHEMENT (Seuil de tolérance)
        # On active la recherche Web SEULEMENT si on a 0 document pertinent.
        # (Tu peux changer 0 par 1 si tu veux être plus strict et exiger au moins 2 docs)
        if len(filtered_docs) == 0:
            if enable_websearch:
                print("---DECISION: NO RELEVANT DOCS FOUND -> WEB SEARCH---")
                web_search_flag = "Yes"
        else:
            print(f"---DECISION: {len(filtered_docs)} GOOD DOCS FOUND -> KEEP GOING---")
        
        return {"documents": filtered_docs, "web_search": web_search_flag}

    def generate(state: Dict[str, Any]):
        print("---GENERATE---")
        question = state["question"]
        documents = state["documents"]
        loop_step = state.get("loop_step", 0)

        docs_txt = format_docs(documents)
        rag_prompt_formatted = RAG_PROMPT.format(context=docs_txt, question=question)
        generation = llm.invoke([HumanMessage(content=rag_prompt_formatted)])
        return {"generation": generation, "loop_step": loop_step + 1}

    # ---------- ROUTERS / DECISIONS ----------

    # def route_question(state: Dict[str, Any]):
    #     print("---ROUTE QUESTION---")
    #     if not enable_websearch:
    #         print("[router] Web search désactivé → force RETRIEVE (RAG).")
    #         return "retrieve"
    #     decision = route_decision(router, state["question"])
    #     if decision == "websearch":
    #         print("---ROUTE QUESTION TO WEB SEARCH---")
    #         return "websearch"
    #     print("---ROUTE QUESTION TO RAG---")
    #     return "retrieve"

    def decide_to_generate(state: Dict[str, Any]):
        print("---ASSESS GRADED DOCUMENTS---")
        if enable_websearch and state.get("web_search") == "Yes":
            print("---DECISION: INCLUDE WEB SEARCH---")
            return "websearch"
        print("---DECISION: GENERATE---")
        return "generate"

    # def grade_generation_v_documents_and_question(state: Dict[str, Any]):
    #     print("---CHECK HALLUCINATIONS---")
    #     question = state["question"]
    #     documents = state["documents"]
    #     generation = state["generation"]
    #     max_retries = state.get("max_retries", 3)
    #     loop_step = state.get("loop_step", 0)

    #     facts = format_docs(documents)
    #     halluc_grade, _ = grade_hallucination(
    #         hallucination_grader, facts_text=facts, generation_text=generation.content
    #     )

    #     if halluc_grade == "yes":
    #         print("---DECISION: GENERATION IS GROUNDED IN DOCUMENTS---")
    #         ans_grade, _ = grade_answer(
    #             answer_grader, question=question, generation_text=generation.content
    #         )
    #         if ans_grade == "yes":
    #             print("---DECISION: GENERATION ADDRESSES QUESTION---")
    #             return "useful"
    #         elif loop_step <= max_retries:
    #             print("---DECISION: GENERATION DOES NOT ADDRESS QUESTION---")
    #             # Si web search off, on réessaie la génération RAG
    #             return "not useful"
    #         else:
    #             print("---DECISION: MAX RETRIES REACHED---")
    #             return "max retries"
    #     else:
    #         if loop_step <= max_retries:
    #             print("---DECISION: GENERATION NOT GROUNDED, RE-TRY---")
    #             return "not supported"
    #         else:
    #             print("---DECISION: MAX RETRIES REACHED---")
    #             return "max retries"

    def grade_generation_v_documents_and_question(state: Dict[str, Any]):
        print("---CHECK QUALITY (HALLUCINATION + RELEVANCE)---")
        question = state["question"]
        documents = state["documents"]
        generation = state["generation"]
        max_retries = state.get("max_retries", 3)
        loop_step = state.get("loop_step", 0)

        facts = format_docs(documents)
        
        # APPEL UNIQUE ICI
        score = grade_generation_quality(
            quality_grader, 
            documents_text=facts, 
            question=question, 
            generation_text=generation.content
        )
        
        is_grounded = score.is_grounded.lower()
        is_relevant = score.is_relevant.lower()
        
        print(f"---SCORES: Grounded={is_grounded} | Relevant={is_relevant}---")

        # LOGIQUE DE DÉCISION
        
        # 1. Vérification Hallucination
        if is_grounded == "yes":
            print("---DECISION: GENERATION IS GROUNDED---")
            
            # 2. Vérification Pertinence (On a déjà le résultat !)
            if is_relevant == "yes":
                print("---DECISION: GENERATION ADDRESSES QUESTION---")
                return "useful"
            
            # Si grounded mais pas relevant -> Websearch (ou retry)
            else:
                print("---DECISION: GENERATION DOES NOT ADDRESS QUESTION---")
                if loop_step <= max_retries:
                    return "not useful" # Va déclencher websearch selon le graphe
                else:
                    return "max retries"
        
        # Si Hallucination (pas grounded)
        else:
            print("---DECISION: GENERATION NOT GROUNDED (HALLUCINATION)---")
            if loop_step <= max_retries:
                return "not supported" # Va déclencher retry generate
            else:
                return "max retries"

    # ---------- BUILD GRAPH ----------
    workflow = StateGraph(GraphState)

    # Noeuds communs
    workflow.add_node("retrieve", retrieve)
    workflow.add_node("grade_documents", grade_documents)
    workflow.add_node("generate", generate)

    # Noeud websearch seulement si activé
    if enable_websearch:
        workflow.add_node("websearch", web_search)

    # Entry point conditionnel
    # if enable_websearch:
    #     workflow.set_conditional_entry_point(
    #         route_question,
    #         {"websearch": "websearch", "retrieve": "retrieve"},
    #     )
    # else:
    #     workflow.set_conditional_entry_point(
    #         route_question,
    #         {"retrieve": "retrieve"},
    #     )

    # Entry point direct (NOUVEAU : Speculative RAG)
    # On commence TOUJOURS par chercher dans la base locale (très rapide).
    # Si les documents sont mauvais, le "grade_documents" nous enverra au websearch ensuite.
    workflow.set_entry_point("retrieve")

    # Edges
    if enable_websearch:
        workflow.add_edge("websearch", "generate")
    workflow.add_edge("retrieve", "grade_documents")

    # Après grading des docs
    if enable_websearch:
        workflow.add_conditional_edges(
            "grade_documents",
            decide_to_generate,
            {"websearch": "websearch", "generate": "generate"},
        )
    else:
        # Si le grading suggère websearch mais qu'il est off, on génère quand même
        workflow.add_conditional_edges(
            "grade_documents",
            decide_to_generate,
            {"websearch": "generate", "generate": "generate"},
        )

    # Après génération
    if enable_websearch:
        workflow.add_conditional_edges(
            "generate",
            grade_generation_v_documents_and_question,
            {
                "not supported": "generate",
                "useful": END,
                "not useful": "websearch",
                "max retries": END,
            },
        )
    else:
        # Sans websearch, on boucle sur generate jusqu'au max_retries
        workflow.add_conditional_edges(
            "generate",
            grade_generation_v_documents_and_question,
            {
                "not supported": "generate",
                "useful": END,
                "not useful": "generate",
                "max retries": END,
            },
        )

    return workflow.compile()


def run_question(graph, question: str, max_retries: int = 3) -> Dict[str, Any]:
    """
    Exécute le graphe et renvoie la réponse ET les contextes (documents).
    Format retourné : {
        "answer": str,
        "contexts": List[str]  # Liste des textes des chunks utilisés
    }
    """
    final_answer = ""
    final_contexts = []
    
    graph_input = {"question": question, "max_retries": max_retries}
    
    # On itère sur le flux. stream_mode="values" renvoie l'état complet à chaque étape.
    for event in graph.stream(graph_input, stream_mode="values"):
        # On capture la réponse générée si elle existe
        if "generation" in event:
            final_answer = event["generation"].content
        
        # On capture les documents s'ils existent (c'est le contexte)
        if "documents" in event:
            # Ragas a besoin d'une liste de strings, pas d'objets Document
            final_contexts = [d.page_content for d in event["documents"]]

    return {
        "answer": final_answer or "(no answer)",
        "contexts": final_contexts
    }

def generate_article_canva(llm, question: str):
    prompt = f"""
    Tu es chargé de concevoir le plan structuré d'un article à partir de la question suivante :

    "{question}"

    Le plan doit être renvoyé AU FORMAT JSON STRICT suivant :
    {{
      "header": {{
          "title": <titre principal>,
          "content": <question reformulée de l'article>
          "content_type": <"text_generation">
      }},
      "part1": {{
          "title": <titre de la partie 1>,
          "content": <question éclairante pour cette partie>,
          "content_type": <"text_generation" ou "data_analysis">
      }},
      "part2": {{
          "title": <titre de la partie 2>,
          "content": <question éclairante pour cette partie>,
          "content_type": <"text_generation" ou "data_analysis">
      }},
      "part3": {{
          "title": <titre de la partie 3>,
          "content": <question éclairante pour cette partie>,
          "content_type": <"text_generation" ou "data_analysis">
      }}
    }}

    Règles :
    - Maximum 3 parties.
    - Si une question implique une analyse quantitative → content_type = "data_analysis", sinon "text_generation".
    - Le header a toujours "content_type" = "text_generation"
    - Ne renvoie aucune phrase hors du JSON.
    """

    response = llm.invoke([HumanMessage(content=prompt)])
    response_clean = response.content.replace("```json", "").replace("```", "").strip()
    print("CLEAN LLM OUTPUT:\n", response_clean)
    return json.loads(response_clean)



def process_single_part(graph, part_key, part_data, main_question, max_retries):
    """
    Fonction helper exécutée en parallèle.
    Adaptée pour gérer le retour dictionnaire de run_question.
    """
    if "content" not in part_data:
        return part_key, None

    sub_question = part_data["content"].strip()
    ctype = part_data.get("content_type", "text_generation")

    if part_key == "header":
        prompt = (
            "Réponds directement, clairement et complètement à la question principale ci-dessous. "
            "Ne propose ni plan ni étapes, ne renvoie pas de JSON. "
            "Structure ta réponse en 2–3 paragraphes courts, avec des points clés si utile.\n\n"
            f"Question principale : {sub_question if sub_question else main_question}"
        )
    else:
        prompt = (
            "Contexte global (question principale) : "
            f"{main_question}\n\n"
            "Réponds maintenant à la question spécifique ci-dessous en t’alignant avec le contexte. "
            "Sois concret et auto-suffisant, pas de renvoi au plan :\n\n"
            f"Question spécifique : {sub_question}"
        )

    # Appel à la nouvelle version de run_question
    result_dict = run_question(graph, question=prompt, max_retries=max_retries)

    result_data = {
        "question": sub_question or main_question,
        "content_type": ctype,
        "generated_answer": result_dict["answer"],       # On extrait le texte pour l'affichage JSON
        "retrieved_contexts": result_dict["contexts"]    # On garde les contextes (utile pour debug ou Ragas futur)
    }
    return part_key, result_data


def process_canva_with_graph(graph, canva, max_retries=3):
    results = {}
    main_question = canva.get("header", {}).get("content", "").strip()
    
    # On prépare la liste des tâches à accomplir
    tasks = []
    
    # On crée un gestionnaire de threads (max_workers=5 signifie jusqu'à 5 tâches en parallèle)
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        
        for part_key in ["header", "part1", "part2", "part3"]:
            if part_key in canva:
                # On soumet la tâche à l'executor, sans attendre la réponse tout de suite
                future = executor.submit(
                    process_single_part, 
                    graph, 
                    part_key, 
                    canva[part_key], 
                    main_question, 
                    max_retries
                )
                tasks.append(future)
        
        # Maintenant on attend que les résultats arrivent (as_completed)
        for future in concurrent.futures.as_completed(tasks):
            try:
                key, data = future.result()
                if data:
                    results[key] = data
            except Exception as e:
                print(f"Erreur lors du traitement parallèle d'une partie : {e}")

    return results


def generate_mui_chart_component(content_type, question):
    if content_type != "data_analysis":
        return None

    print(f"React component needed to answer: {question}")

    df = pd.read_csv("data/tables/athletes_500m_full_noNull_ordered.csv")
    head_string = df.head().to_string(index=False)

    prompt = f"""
    You are a front-end expert using React + recharts.

    Dataset preview (the full dataset will be passed as a `data` prop on the front-end):
    {head_string}

    The user is asking: "{question}"

    - If the question ressembles : "How can you compare the consistency of lap times between different countries or categories of racers using the columns country, category, and the lap time data (laptime_min, laptime_sec, laptime_thousandth)?"
    then do a boxplot.
    - If the question ressembles : "Using the columns name and the lap time data (laptime_min, laptime_sec, laptime_thousandth), how can you show which racer achieved the best average or fastest lap times?"
    then do a barplot.
    - If the question ressembles : "If you want to represent the proportion of participants by country or by category, which columns from the table would you use, and how could a pie chart illustrate this distribution?"
    then do a piechart.

    Rules (IMPORTANT):
    - Output only valid JSX (no markdown fences).
    - Do NOT import any local dataset. The component MUST accept a `data` prop (array of objects).
    - **Do NOT use `require()` or `import`.**
    - Export a default React component named GeneratedChart: `export default function GeneratedChart({{ data }}) {{ ... }}`.
    
    - No network calls, no dynamic imports, no CSS imports.
    - Use ONLY Recharts primitives (e.g., LineChart, BarChart, PieChart, AreaChart, ComposedChart, XAxis, YAxis, Tooltip, Legend, CartesianGrid, ResponsiveContainer, etc.) that are expected to exist in scope.
    """
    # - Use at most 50 rows (slice in code if needed).
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )

    code = response.choices[0].message.content or ""
    code = code.replace("```jsx", "").replace("```javascript", "").replace("```", "").strip()

    output_path = "./../../frontend/src/components/GeneratedGraph.jsx"
    try:
        with open(output_path, "w") as f:
            f.write(code)
        print(f"\n✅ Fichier écrit dans : {output_path}")
    except Exception as e:
        print(f"⚠️ Impossible d'écrire le fichier : {e}")

    return code

