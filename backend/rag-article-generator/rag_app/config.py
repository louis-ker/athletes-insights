URLS = [
    "https://lilianweng.github.io/posts/2023-06-23-agent/",
    "https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/",
    "https://lilianweng.github.io/posts/2023-10-25-adv-attack-llm/",
]

# Fichiers locaux .txt (relatif à la racine du projet)
DOCS_GLOB = "data/**/*.txt"  # crée un dossier data/ et mets-y tes .txt

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

MISTRAL_MODEL = "mistral-small-latest"

TAVILY_K = 3

DEFAULT_MAX_RETRIES = 3

# Persistance de l'index FAISS
INDEX_DIR = "artifacts/index-faiss"

# Sources activées par défaut
USE_URLS_DEFAULT = True
USE_FILES_DEFAULT = True

# Web search activé par défaut
USE_WEBSEARCH_DEFAULT = True
