# //////////////////////// IMPORTS ////////////////////////

import argparse
import os
import json
import sys
import traceback
from dotenv import load_dotenv

from rag_app.config import (
    URLS,
    DEFAULT_MAX_RETRIES,
    INDEX_DIR,
    DOCS_GLOB,
    USE_URLS_DEFAULT,
    USE_FILES_DEFAULT,
    USE_WEBSEARCH_DEFAULT,
)
from rag_app.llm import get_llm
from rag_app.data import get_retriever  # charge ou (re)construit l'index
from rag_app.router import create_router
from rag_app.graders import (
    create_doc_grader,
    create_hallucination_grader,
    create_answer_grader,
)
from rag_app.websearch import get_web_search_tool
from rag_app.workflow import build_graph, run_question

from rag_app.workflow import generate_article_canva
from rag_app.workflow import process_canva_with_graph
# from rag_app.workflow import generate_matplotlib_figure
from rag_app.workflow import generate_mui_chart_component

# //////////////////////// ENVIRONEMENT ////////////////////////

load_dotenv()

def _set_env(var: str):
    if not os.environ.get(var):
        os.environ[var] = getpass.getpass(f"{var}: ")

os.environ["USER_AGENT"] = "Mozilla/5.0 (compatible; LangChainBot/1.0; +https://python.langchain.com)"

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
os.environ['TOKENIZERS_PARALLELISM'] = 'true'

LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
# os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "default"

def log(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)  # tout le bruit en STDERR

def emit_json(canva):
    print("\n===CANVA_JSON_START===", flush=True)
    print(json.dumps(canva, ensure_ascii=False, indent=2), flush=True)
    print("===CANVA_JSON_END===", flush=True)

def main():
    parser = argparse.ArgumentParser(description="RAG + Router + Graders (LangGraph)")

    parser.add_argument(
        "-q", "--question",
        default="What is the International Skating Union?",
        help="Question utilisateur"
    )
    parser.add_argument(
        "--max-retries", type=int, default=DEFAULT_MAX_RETRIES,
        help="Nombre max de tentatives de génération en boucle"
    )
    parser.add_argument(
        "--rebuild-index", action="store_true",
        help="Force la reconstruction de l'index vectoriel"
    )
    parser.add_argument(
        "--index-dir", default=INDEX_DIR,
        help="Dossier de persistance FAISS (sera créé si absent)"
    )
    parser.add_argument(
        "--files-glob", default=DOCS_GLOB,
        help="Motif (glob) des fichiers .txt locaux à indexer (ex: 'data/**/*.txt')"
    )

    parser.add_argument("--use-urls", dest="use_urls", action="store_true",
                        default=USE_URLS_DEFAULT, help="Active la source URLs")
    parser.add_argument("--no-use-urls", dest="use_urls", action="store_false",
                        help="Désactive la source URLs")
    parser.add_argument("--use-files", dest="use_files", action="store_true",
                        default=USE_FILES_DEFAULT, help="Active la source FICHIERS .txt")
    parser.add_argument("--no-use-files", dest="use_files", action="store_false",
                        help="Désactive la source FICHIERS .txt")

    parser.add_argument("--web-search", dest="web_search", action="store_true",
                        default=USE_WEBSEARCH_DEFAULT, help="Active l'usage du web search (Tavily)")
    parser.add_argument("--no-web-search", dest="web_search", action="store_false",
                        help="Désactive le web search et force un workflow RAG pur")

    parser.add_argument(
        "--interactive", action="store_true",
        help="Mode interactif : poser plusieurs questions sans reconstruire l'index"
    )
    args = parser.parse_args()

    print(f"[cli] sources: urls={args.use_urls}, files={args.use_files}, glob='{args.files_glob}'")
    print(f"[cli] web_search={args.web_search} | index_dir: {args.index_dir} | rebuild_index={args.rebuild_index}")

    llm = get_llm(temperature=0)
    retriever = get_retriever(
        index_dir=args.index_dir,
        urls=URLS,
        files_glob=args.files_glob,
        use_urls=args.use_urls,
        use_files=args.use_files,
        force_rebuild=args.rebuild_index,
    )

    router = create_router(llm)
    doc_grader = create_doc_grader(llm)
    hallucination_grader = create_hallucination_grader(llm)
    answer_grader = create_answer_grader(llm)
    web_tool = get_web_search_tool() if args.web_search else None

    graph = build_graph(
        retriever=retriever,
        llm=llm,
        router=router,
        doc_grader=doc_grader,
        hallucination_grader=hallucination_grader,
        answer_grader=answer_grader,
        web_search_tool=web_tool,
        enable_websearch=args.web_search,
    )

    # MODE INTERACTIF
    if args.interactive:
        print("Index chargé. Pose des questions (entrée vide pour quitter).")
        while True:
            try:
                q = input("Q> ").strip()
            except (EOFError, KeyboardInterrupt):
                break
            if not q:
                break
            final = run_question(graph, question=q, max_retries=args.max_retries)
            print("\n=== FINAL ANSWER ===")
            print(final)
            print()
        return

    canva = {}
    try:
        log("\n=== GENERATION DU CANVA ===")
        canva = generate_article_canva(llm, args.question)

        log("\n=== TRAITEMENT DES SOUS-QUESTIONS AVEC LE GRAPH ===")
        results = process_canva_with_graph(graph, canva, max_retries=args.max_retries)

        # fusion texte
        canva["original_question"] = args.question
        for key in ["part1", "part2", "part3"]:
            if key in canva and key in results:
                canva[key]["question"] = results[key].get("question", canva[key].get("content", ""))
                canva[key]["generated_answer"] = results[key].get("generated_answer", "")

        # ajout des graphs (JSX) si data_analysis
        graphs = {}
        for key, data in results.items():
            if data.get("content_type") == "data_analysis":
                jsx = generate_mui_chart_component(data["content_type"], data["question"])
                if jsx:
                    graphs[key] = {
                        "componentName": "GeneratedChart",
                        "library": "mui-x-charts",
                        "jsx": jsx
                    }
        if graphs:
            canva["graphs"] = graphs

    except Exception as e:
        # On ne crash pas l’API : on renvoie quand même un JSON exploitable
        log("ERROR in main.py:", e)
        log(traceback.format_exc())
        canva = canva or {"header": {"title": "", "content": "", "content_type": "text_generation"}}
        canva["error"] = str(e)

    finally:
        # 🔴 Toujours émettre le JSON balisé sur STDOUT
        emit_json(canva)

        

if __name__ == "__main__":
    main()
