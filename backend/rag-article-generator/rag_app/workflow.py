from typing import Dict, Any

from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage
from langchain_core.documents import Document

from .types import GraphState
from .prompts import RAG_PROMPT
from .utils import format_docs
from .router import route_decision
from .graders import grade_document_relevance, grade_hallucination, grade_answer

import json
import pandas as pd
import os
from openai import OpenAI


def build_graph(
    retriever,
    llm,
    router,
    doc_grader,
    hallucination_grader,
    answer_grader,
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
        web_results = "\n".join([d["content"] for d in docs])
        documents.append(Document(page_content=web_results))
        return {"documents": documents}

    def retrieve(state: Dict[str, Any]):
        print("---RETRIEVE---")
        question = state["question"]
        documents = retriever.invoke(question)
        return {"documents": documents}

    def grade_documents(state: Dict[str, Any]):
        print("---CHECK DOCUMENT RELEVANCE TO QUESTION---")
        question = state["question"]
        documents = state["documents"]

        filtered_docs = []
        web_search_flag = "No"
        for d in documents:
            grade = grade_document_relevance(doc_grader, d.page_content, question)
            if grade == "yes":
                print("---GRADE: DOCUMENT RELEVANT---")
                filtered_docs.append(d)
            else:
                print("---GRADE: DOCUMENT NOT RELEVANT---")
                if enable_websearch:
                    web_search_flag = "Yes"
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

    def route_question(state: Dict[str, Any]):
        print("---ROUTE QUESTION---")
        if not enable_websearch:
            print("[router] Web search désactivé → force RETRIEVE (RAG).")
            return "retrieve"
        decision = route_decision(router, state["question"])
        if decision == "websearch":
            print("---ROUTE QUESTION TO WEB SEARCH---")
            return "websearch"
        print("---ROUTE QUESTION TO RAG---")
        return "retrieve"

    def decide_to_generate(state: Dict[str, Any]):
        print("---ASSESS GRADED DOCUMENTS---")
        if enable_websearch and state.get("web_search") == "Yes":
            print("---DECISION: INCLUDE WEB SEARCH---")
            return "websearch"
        print("---DECISION: GENERATE---")
        return "generate"

    def grade_generation_v_documents_and_question(state: Dict[str, Any]):
        print("---CHECK HALLUCINATIONS---")
        question = state["question"]
        documents = state["documents"]
        generation = state["generation"]
        max_retries = state.get("max_retries", 3)
        loop_step = state.get("loop_step", 0)

        facts = format_docs(documents)
        halluc_grade, _ = grade_hallucination(
            hallucination_grader, facts_text=facts, generation_text=generation.content
        )

        if halluc_grade == "yes":
            print("---DECISION: GENERATION IS GROUNDED IN DOCUMENTS---")
            ans_grade, _ = grade_answer(
                answer_grader, question=question, generation_text=generation.content
            )
            if ans_grade == "yes":
                print("---DECISION: GENERATION ADDRESSES QUESTION---")
                return "useful"
            elif loop_step <= max_retries:
                print("---DECISION: GENERATION DOES NOT ADDRESS QUESTION---")
                # Si web search off, on réessaie la génération RAG
                return "not useful"
            else:
                print("---DECISION: MAX RETRIES REACHED---")
                return "max retries"
        else:
            if loop_step <= max_retries:
                print("---DECISION: GENERATION NOT GROUNDED, RE-TRY---")
                return "not supported"
            else:
                print("---DECISION: MAX RETRIES REACHED---")
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
    if enable_websearch:
        workflow.set_conditional_entry_point(
            route_question,
            {"websearch": "websearch", "retrieve": "retrieve"},
        )
    else:
        workflow.set_conditional_entry_point(
            route_question,
            {"retrieve": "retrieve"},
        )

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


def run_question(graph, question: str, max_retries: int = 3) -> str:
    """
    Exécute le graphe en mode stream et renvoie le texte final de génération.
    """
    final_text = ""
    graph_input = {"question": question, "max_retries": max_retries}
    for event in graph.stream(graph_input, stream_mode="values"):
        if "generation" in event:
            final_text = event["generation"].content
    return final_text or "(no answer)"

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

def process_canva_with_graph(graph, canva, max_retries=3):
    results = {}

    for part_key in ["header", "part1", "part2", "part3"]:
        if part_key in canva and "content" in canva[part_key]:
            question = canva[part_key]["content"]
            answer = run_question(graph, question=question, max_retries=max_retries)
            results[part_key] = {
                "question": question,
                "content_type": canva[part_key]["content_type"],
                "generated_answer": answer
            }

    return results

# def generate_matplotlib_figure(content_type, question):
#     if content_type == "data_analysis":
#         print(f"Figure needed to anwser: {question}")

#         print(os.getcwd())
#         df = pd.read_csv("data/tables/athletes_500m_full_noNull_ordered.csv")
#         print("Aperçu des données :")
#         print(df.head())

#         prompt = f"""
#         You are a Python assistant. Here is an extract of a pandas DataFrame:
#         {df.head().to_string(index=False)}

#         The user is asking: "{question}"

#         Génère uniquement le code Python nécessaire pour créer un graphique clair avec matplotlib.
#         Le code doit supposer que le DataFrame complet est déjà chargé dans la variable `df`.

#         Ne mets pas de texte explicatif, renvoie juste le code exécutable.
#         """
#         client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

#         # Appel API
#         response = client.chat.completions.create(
#             model="gpt-4o-mini",
#             messages=[{"role": "user", "content": prompt}],
#         )

#         code = response.choices[0].message.content

#         # Nettoyer le code (enlever les ```python``` ou ```)
#         code = code.replace("```python", "").replace("```", "").strip()

#         print("\n--- Code généré ---\n")
#         print(code)

#         # Sauvegarder et exécuter le code
#         with open("generated_plot.py", "w") as f:
#             f.write("import pandas as pd\nimport matplotlib.pyplot as plt\nimport plotly.express as px\n")
#             f.write("import sys\n\n")
#             f.write(code)

#     return 0

# def generate_mui_chart_component(content_type, question):
#     if content_type == "data_analysis":
#         print(f"React component needed to answer: {question}")

#         print(os.getcwd())
#         df = pd.read_csv("data/tables/athletes_500m_full_noNull_ordered.csv")
#         print("Aperçu des données :")
#         print(df.head())

#         # Conversion minimaliste de l'extrait du df pour le contexte
#         head_string = df.head().to_string(index=False)

#         prompt = f"""
#         You are a front-end expert using React + MUI X Charts.

#         Here is a preview of the dataset (the full dataset will be imported as JSON on the front-end):
#         {head_string}

#         The user is asking: "{question}"

#         You are an expert in data visualization using React + MUI X Charts.

#         Column details:
#         - country: str, origin of the ice speed skating athlete
#         - name: str, name of the ice speed skating athlete
#         - laptime_min: minutes part of race time
#         - laptime_sec: seconds part of race time
#         - laptime_thousandth: milliseconds part of race time
#         - date: date of the ice speed skating event
#         - location: location of the ice speed skating event
#         - competition: name of the ice speed skating event
#         - category: category of the ice speed skating event

#         Visualization objective: detect temporal trends and compare values across categories.

#         Dataset size: ~50,000 rows.

#         Task:
#         Generate a ready-to-use React component that answers best the question with MUI X Charts.

#         Rules:
#         - Output only valid JSX. Do NOT output any explanation.
#         - Use a most 50 rows of data
#         - import the data like so : import data from './../../../backend/rag-article-generator/data/tables/athletes_500m_full_noNull_ordered.json';
#         """

#         client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

#         response = client.chat.completions.create(
#             model="gpt-4o-mini",
#             messages=[{"role": "user", "content": prompt}]
#         )

#         code = response.choices[0].message.content
#         code = code.replace("```jsx", "").replace("```javascript", "").replace("```", "").strip()

#         print("\n--- Composant React généré ---\n")
#         print(code)

#         # Sauvegarde du composant
#         output_path = "./../../frontend/src/components/GeneratedGraph.jsx"  # ajuste si nécessaire
#         with open(output_path, "w") as f:
#             f.write(code)

#         print(f"\n✅ Fichier écrit dans : {output_path}")

#     return 0

# workflow.py
# def generate_mui_chart_component(content_type, question):
#     if content_type != "data_analysis":
#         return None

#     print(f"React component needed to answer: {question}")

#     df = pd.read_csv("data/tables/athletes_500m_full_noNull_ordered.csv")
#     head_string = df.head().to_string(index=False)

#     # prompt = f"""
#     # You are a front-end expert using React + MUI X Charts.

#     # Dataset preview (the full dataset will be passed as a `data` prop on the front-end):
#     # {head_string}

#     # The user is asking: "{question}"

#     # Rules (IMPORTANT):
#     # - Output only valid JSX (no markdown fences).
#     # - Do NOT import any local dataset. The component MUST accept a `data` prop (array of objects).
#     # - Prefer MUI X Charts primitives. You may import from 'react', '@mui/x-charts' and 'recharts' only.
#     # - Export a default React component named GeneratedChart: `export default function GeneratedChart({{ data }}) {{ ... }}`.
#     # - Use at most 50 rows (slice in code if needed).
#     # - No network calls, no dynamic imports, no CSS imports.
#     # """

#     prompt = f"""
#     You are a front-end expert using React + recharts.

#     Dataset preview (the full dataset will be passed as a `data` prop on the front-end):
#     {head_string}

#     The user is asking: "{question}"

#     Rules (IMPORTANT):
#     - Output only valid JSX (no markdown fences).
#     - Do NOT import any local dataset. The component MUST accept a `data` prop (array of objects).
#     - **Do NOT use `require()` or `import`.**
#     - Export a default React component named GeneratedChart: `export default function GeneratedChart({{ data }}) {{ ... }}`.
#     - Use at most 50 rows (slice in code if needed).
#     - No network calls, no dynamic imports, no CSS imports.
#     """

#     client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
#     response = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[{"role": "user", "content": prompt}]
#     )

#     code = response.choices[0].message.content or ""
#     code = code.replace("```jsx", "").replace("```javascript", "").replace("```", "").strip()

#     # (Optionnel) conserver le flux Dev en écrivant le fichier pour HMR
#     output_path = "./../../frontend/src/components/GeneratedGraph.jsx"
#     try:
#         with open(output_path, "w") as f:
#             f.write(code)
#         print(f"\n✅ Fichier écrit dans : {output_path}")
#     except Exception as e:
#         print(f"⚠️ Impossible d'écrire le fichier : {e}")

#     return code

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

    Rules (IMPORTANT):
    - Output only valid JSX (no markdown fences).
    - Do NOT import any local dataset. The component MUST accept a `data` prop (array of objects).
    - **Do NOT use `require()` or `import`.**
    - Export a default React component named GeneratedChart: `export default function GeneratedChart({{ data }}) {{ ... }}`.
    - Use at most 50 rows (slice in code if needed).
    - No network calls, no dynamic imports, no CSS imports.
    - Use ONLY Recharts primitives (e.g., LineChart, BarChart, PieChart, AreaChart, ComposedChart, XAxis, YAxis, Tooltip, Legend, CartesianGrid, ResponsiveContainer, etc.) that are expected to exist in scope.
    """

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4o-mini",
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

