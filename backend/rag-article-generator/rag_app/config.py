URLS = [
    "https://www.isu.org/inside-isu/about/",
    "https://en.wikipedia.org/wiki/International_Skating_Union",
    "https://en.wikipedia.org/wiki/Sports_governing_body",
    "https://en.wikipedia.org/wiki/Ice_skating",
    "https://en.wikipedia.org/wiki/Figure_skating",
    "https://en.wikipedia.org/wiki/Synchronized_skating",
    "https://en.wikipedia.org/wiki/Speed_skating",
    "https://en.wikipedia.org/wiki/Short_track_speed_skating",
    "https://en.wikipedia.org/wiki/U.S._Figure_Skating",
    "https://en.wikipedia.org/wiki/1924_Winter_Olympics",
    "https://en.wikipedia.org/wiki/1976_Winter_Olympics",
    "https://en.wikipedia.org/wiki/World_Short_Track_Speed_Skating_Championships",
    "https://en.wikipedia.org/wiki/Long_track_speed_skating",
    "https://en.wikipedia.org/wiki/World_Short_Track_Speed_Skating_Championships",
    "https://en.wikipedia.org/wiki/World_Short_Track_Speed_Skating_Team_Championships",
    "https://en.wikipedia.org/wiki/World_Junior_Short_Track_Speed_Skating_Championships",
    "https://en.wikipedia.org/wiki/European_Short_Track_Speed_Skating_Championships",
    "https://en.wikipedia.org/wiki/Asian_Distance_Speed_Skating_Championships",
    "https://en.wikipedia.org/wiki/Ahn_Hyun-Soo",
    "https://en.wikipedia.org/wiki/Marc_Gagnon",
    "https://en.wikipedia.org/wiki/Charles_Hamelin",
    "https://en.wikipedia.org/wiki/Kim_Ki-hoon",
    "https://en.wikipedia.org/wiki/Apolo_Anton_Ohno",
    "https://en.wikipedia.org/wiki/Lee_Ho-Suk",
    "https://en.wikipedia.org/wiki/Kim_Dong-Sung",
    "https://en.wikipedia.org/wiki/Shaoang_Liu",
    "https://en.wikipedia.org/wiki/Yang_Yang_(b._1976)",
    "https://en.wikipedia.org/wiki/Wang_Meng_(speed_skater)",
    "https://en.wikipedia.org/wiki/Chun_Lee-kyung",
    "https://en.wikipedia.org/wiki/Choi_Min-jeong",
    "https://en.wikipedia.org/wiki/Sylvie_Daigle",
    "https://en.wikipedia.org/wiki/Jin_Sun-yu",
    "https://en.wikipedia.org/wiki/Suzanne_Schulting",
    "https://en.wikipedia.org/wiki/Nathalie_Lambert",
    "https://en.wikipedia.org/wiki/Choi_Eun-kyung",
    "https://en.wikipedia.org/wiki/Shim_Suk-Hee",
    "https://en.wikipedia.org/wiki/Park_Seung-hi",
    "https://en.wikipedia.org/wiki/Zhou_Yang_(speed_skater)",
    "https://en.wikipedia.org/wiki/Arianna_Fontana"
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
