# import os
# import json
# import hashlib
# from typing import List, Optional

# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_community.document_loaders import WebBaseLoader
# from langchain_community.vectorstores import FAISS
# from langchain_core.documents import Document

# from .config import CHUNK_SIZE, CHUNK_OVERLAP
# from .llm import get_embeddings


# # -------- Helpers: IO / fingerprint --------

# def _ensure_dir(path: str):
#     os.makedirs(path, exist_ok=True)

# def _meta_path(index_dir: str) -> str:
#     return os.path.join(index_dir, "meta.json")

# def _fingerprint(urls: List[str], chunk_size: int, chunk_overlap: int) -> str:
#     payload = json.dumps(
#         {"urls": sorted(urls), "chunk_size": chunk_size, "chunk_overlap": chunk_overlap},
#         sort_keys=True,
#     ).encode("utf-8")
#     return hashlib.md5(payload).hexdigest()

# def _write_meta(index_dir: str, meta: dict):
#     _ensure_dir(index_dir)
#     with open(_meta_path(index_dir), "w", encoding="utf-8") as f:
#         json.dump(meta, f, indent=2)

# def _read_meta(index_dir: str) -> Optional[dict]:
#     try:
#         with open(_meta_path(index_dir), "r", encoding="utf-8") as f:
#             return json.load(f)
#     except FileNotFoundError:
#         return None


# # -------- Pipeline: load / split / index --------

# def load_documents(urls: List[str]) -> List[Document]:
#     docs_nested = [WebBaseLoader(url).load() for url in urls]
#     return [d for sub in docs_nested for d in sub]

# def split_documents(docs: List[Document]) -> List[Document]:
#     splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
#         chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP
#     )
#     return splitter.split_documents(docs)

# def _build_faiss_index(urls: List[str], index_dir: str) -> FAISS:
#     print(f"[index] Building FAISS index from URLs ({len(urls)}) …")
#     docs = load_documents(urls)
#     splits = split_documents(docs)
#     embeddings = get_embeddings()
#     vs = FAISS.from_documents(splits, embeddings)
#     _ensure_dir(index_dir)
#     vs.save_local(index_dir)
#     meta = {
#         "fingerprint": _fingerprint(urls, CHUNK_SIZE, CHUNK_OVERLAP),
#         "urls": urls,
#         "chunk_size": CHUNK_SIZE,
#         "chunk_overlap": CHUNK_OVERLAP,
#         "backend": "faiss",
#     }
#     _write_meta(index_dir, meta)
#     print(f"[index] Saved to {index_dir}")
#     return vs

# def _load_faiss_index(index_dir: str) -> FAISS:
#     print(f"[index] Loading FAISS index from {index_dir} …")
#     embeddings = get_embeddings()
#     # allow_dangerous_deserialization=True requis pour FAISS.load_local
#     vs = FAISS.load_local(index_dir, embeddings, allow_dangerous_deserialization=True)
#     return vs


# # -------- Public API --------

# def get_retriever(
#     index_dir: str,
#     urls: List[str],
#     force_rebuild: bool = False,
# ):
#     """
#     Charge ou (re)construit un index FAISS persistant, et renvoie un retriever.
#     * Si l'index existe et que son fingerprint correspond aux URLs & au chunking, on le recharge.
#     * Sinon on reconstruit.
#     * `force_rebuild=True` force la reconstruction.
#     """
#     desired_fp = _fingerprint(urls, CHUNK_SIZE, CHUNK_OVERLAP)
#     meta = _read_meta(index_dir)

#     must_rebuild = force_rebuild or (meta is None) or (meta.get("fingerprint") != desired_fp)

#     if must_rebuild:
#         vs = _build_faiss_index(urls, index_dir)
#     else:
#         vs = _load_faiss_index(index_dir)

#     return vs.as_retriever()

# =========================== ce code fonctionne bien =============
# =========================== ce code fonctionne bien =============
# =========================== ce code fonctionne bien =============
# =========================== ce code fonctionne bien =============
# =========================== ce code fonctionne bien =============

# import os
# import json
# import hashlib
# from typing import List, Optional, Dict, Any

# from pathlib import Path

# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_community.document_loaders import WebBaseLoader
# from langchain_community.vectorstores import FAISS
# from langchain_core.documents import Document

# from .config import CHUNK_SIZE, CHUNK_OVERLAP
# from .llm import get_embeddings


# # -------- Helpers: IO / fingerprint --------

# def _ensure_dir(path: str):
#     os.makedirs(path, exist_ok=True)

# def _meta_path(index_dir: str) -> str:
#     return os.path.join(index_dir, "meta.json")

# def _hash_dict(payload: Dict[str, Any]) -> str:
#     blob = json.dumps(payload, sort_keys=True, ensure_ascii=False).encode("utf-8")
#     return hashlib.md5(blob).hexdigest()

# def _list_txt_files(files_glob: str) -> List[str]:
#     if not files_glob:
#         return []
#     paths = []
#     for p in Path(".").glob(files_glob):
#         if p.is_file() and p.suffix.lower() == ".txt":
#             paths.append(p.resolve().as_posix())
#     return sorted(set(paths))

# def _files_sig(files: List[str]) -> List[Dict[str, Any]]:
#     """
#     Signature légère des fichiers (chemin, taille, mtime). On évite de hasher le contenu
#     pour rester rapide; si tu veux une détection 100% robuste, remplace par un hash du contenu.
#     """
#     sig = []
#     for f in files:
#         try:
#             st = os.stat(f)
#             sig.append({"path": f, "size": st.st_size, "mtime_ns": st.st_mtime_ns})
#         except FileNotFoundError:
#             # fichier supprimé : on note quand même l'entrée
#             sig.append({"path": f, "size": -1, "mtime_ns": -1})
#     return sig

# def _fingerprint(urls: List[str], files_glob: str, chunk_size: int, chunk_overlap: int) -> str:
#     files = _list_txt_files(files_glob)
#     payload = {
#         "urls": sorted(urls or []),
#         "files_sig": _files_sig(files),
#         "chunk_size": chunk_size,
#         "chunk_overlap": chunk_overlap,
#         "backend": "faiss",
#     }
#     return _hash_dict(payload)

# def _write_meta(index_dir: str, meta: dict):
#     _ensure_dir(index_dir)
#     with open(_meta_path(index_dir), "w", encoding="utf-8") as f:
#         json.dump(meta, f, indent=2, ensure_ascii=False)

# def _read_meta(index_dir: str) -> Optional[dict]:
#     try:
#         with open(_meta_path(index_dir), "r", encoding="utf-8") as f:
#             return json.load(f)
#     except FileNotFoundError:
#         return None


# # -------- Loaders --------

# def _load_from_urls(urls: List[str]) -> List[Document]:
#     if not urls:
#         return []
#     docs_nested = [WebBaseLoader(url).load() for url in urls]
#     return [d for sub in docs_nested for d in sub]

# # def _load_from_files(files_glob: str) -> List[Document]:
# #     files = _list_txt_files(files_glob)
# #     docs: List[Document] = []
# #     for path in files:
# #         try:
# #             with open(path, "r", encoding="utf-8", errors="ignore") as f:
# #                 txt = f.read()
# #             docs.append(Document(page_content=txt, metadata={"source": path}))
# #         except Exception as e:
# #             print(f"[warn] Impossible de lire {path}: {e}")
# #     return docs

# def _load_from_files(files_glob: str) -> List[Document]:
#     files = _list_txt_files(files_glob)
#     if not files:
#         cwd = os.getcwd()
#         print(f"[index] Aucun fichier .txt ne matche '{files_glob}' (cwd: {cwd}).")
#         return []
#     print(f"[index] {len(files)} fichier(s) .txt détecté(s) via '{files_glob}'.")
#     docs: List[Document] = []
#     for path in files:
#         try:
#             with open(path, "r", encoding="utf-8", errors="ignore") as f:
#                 txt = f.read()
#             docs.append(Document(page_content=txt, metadata={"source": path}))
#         except Exception as e:
#             print(f"[warn] Impossible de lire {path}: {e}")
#     return docs



# # -------- Split --------

# def split_documents(docs: List[Document]) -> List[Document]:
#     splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
#         chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP
#     )
#     return splitter.split_documents(docs)


# # -------- Index build/load --------

# def _build_faiss_index(
#     urls: List[str],
#     files_glob: str,
#     index_dir: str,
#     use_urls: bool,
#     use_files: bool,
# ) -> FAISS:
#     sources: List[Document] = []
#     if use_urls:
#         print(f"[index] Loading {len(urls)} URL(s) …")
#         sources.extend(_load_from_urls(urls))
#     if use_files:
#         print(f"[index] Loading local .txt from pattern: {files_glob!r} …")
#         sources.extend(_load_from_files(files_glob))

#     if not sources:
#         raise ValueError("Aucune source fournie : active les URLs et/ou les fichiers .txt.")

#     print(f"[index] Total documents avant split: {len(sources)}")
#     splits = split_documents(sources)
#     print(f"[index] Total chunks après split: {len(splits)}")

#     embeddings = get_embeddings()
#     vs = FAISS.from_documents(splits, embeddings)

#     _ensure_dir(index_dir)
#     vs.save_local(index_dir)

#     meta = {
#         "fingerprint": _fingerprint(urls, files_glob, CHUNK_SIZE, CHUNK_OVERLAP),
#         "urls": urls,
#         "files_glob": files_glob,
#         "files_sig": _files_sig(_list_txt_files(files_glob)),
#         "chunk_size": CHUNK_SIZE,
#         "chunk_overlap": CHUNK_OVERLAP,
#         "backend": "faiss",
#         "use_urls": use_urls,
#         "use_files": use_files,
#     }
#     _write_meta(index_dir, meta)
#     print(f"[index] Saved to {index_dir}")
#     return vs

# def _load_faiss_index(index_dir: str) -> FAISS:
#     print(f"[index] Loading FAISS index from {index_dir} …")
#     embeddings = get_embeddings()
#     return FAISS.load_local(index_dir, embeddings, allow_dangerous_deserialization=True)


# # -------- Public API --------

# def get_retriever(
#     index_dir: str,
#     urls: List[str],
#     files_glob: str,
#     use_urls: bool = True,
#     use_files: bool = True,
#     force_rebuild: bool = False,
# ):
#     """
#     Charge ou (re)construit un index FAISS persistant, et renvoie un retriever.
#     Les sources peuvent venir d'URLs, de fichiers .txt locaux (ou des deux).
#     La décision rebuild / reload se fait via un fingerprint (URLs + signature des fichiers + params de split).
#     """
#     desired_fp = _fingerprint(urls if use_urls else [], files_glob if use_files else "", CHUNK_SIZE, CHUNK_OVERLAP)
#     meta = _read_meta(index_dir)

#     must_rebuild = (
#         force_rebuild
#         or (meta is None)
#         or (meta.get("fingerprint") != desired_fp)
#     )

#     if must_rebuild:
#         vs = _build_faiss_index(
#             urls=urls if use_urls else [],
#             files_glob=files_glob if use_files else "",
#             index_dir=index_dir,
#             use_urls=use_urls,
#             use_files=use_files,
#         )
#     else:
#         vs = _load_faiss_index(index_dir)

#     return vs.as_retriever()

# ========================= test ================================

import os
import json
import hashlib
from typing import List, Optional, Dict, Any
from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

from .config import CHUNK_SIZE, CHUNK_OVERLAP
from .llm import get_embeddings


# -------- Helpers: IO / fingerprint --------

def _ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)

def _meta_path(index_dir: str) -> str:
    return os.path.join(index_dir, "meta.json")

def _hash_dict(payload: Dict[str, Any]) -> str:
    blob = json.dumps(payload, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return hashlib.md5(blob).hexdigest()

def _list_txt_files(files_glob: str) -> List[str]:
    if not files_glob:
        return []
    paths = []
    for p in Path(".").glob(files_glob):
        if p.is_file() and p.suffix.lower() == ".txt":
            paths.append(p.resolve().as_posix())
    return sorted(set(paths))

def _files_sig(files: List[str]) -> List[Dict[str, Any]]:
    """
    Signature légère des fichiers (chemin, taille, mtime).
    """
    sig = []
    for f in files:
        try:
            st = os.stat(f)
            sig.append({"path": f, "size": st.st_size, "mtime_ns": st.st_mtime_ns})
        except FileNotFoundError:
            sig.append({"path": f, "size": -1, "mtime_ns": -1})
    return sig

def _fingerprint(urls: List[str], files_glob: str, chunk_size: int, chunk_overlap: int) -> str:
    files = _list_txt_files(files_glob)
    payload = {
        "urls": sorted(urls or []),
        "files_sig": _files_sig(files),
        "chunk_size": chunk_size,
        "chunk_overlap": chunk_overlap,
        "backend": "faiss",
    }
    return _hash_dict(payload)

def _write_meta(index_dir: str, meta: dict):
    _ensure_dir(index_dir)
    with open(_meta_path(index_dir), "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)

def _read_meta(index_dir: str) -> Optional[dict]:
    try:
        with open(_meta_path(index_dir), "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return None


# -------- Loaders (avec prints de progression) --------

def _load_from_urls(urls: List[str]) -> List[Document]:
    if not urls:
        return []
    n = len(urls)
    print(f"[index][urls] {n} URL(s) à parser.")
    docs_total: List[Document] = []
    for i, url in enumerate(urls, 1):
        try:
            docs = WebBaseLoader(url).load()
            docs_total.extend(docs)
            print(f"[index][urls] {i}/{n} OK - {url} (docs: {len(docs)}; cumul: {len(docs_total)})")
        except Exception as e:
            print(f"[warn][urls] {i}/{n} FAIL - {url}: {e}")
    return docs_total

def _load_from_files(files_glob: str) -> List[Document]:
    files = _list_txt_files(files_glob)
    if not files:
        cwd = os.getcwd()
        print(f"[index][files] Aucun .txt ne matche '{files_glob}' (cwd: {cwd}).")
        return []
    n = len(files)
    print(f"[index][files] {n} fichier(s) .txt à parser (glob='{files_glob}').")
    docs: List[Document] = []
    for i, path in enumerate(files, 1):
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                txt = f.read()
            docs.append(Document(page_content=txt, metadata={"source": path}))
            print(f"[index][files] {i}/{n} OK - {path} (chars: {len(txt)}; cumul docs: {len(docs)})")
        except Exception as e:
            print(f"[warn][files] {i}/{n} FAIL - {path}: {e}")
    return docs


# -------- Split --------

def split_documents(docs: List[Document]) -> List[Document]:
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP
    )
    return splitter.split_documents(docs)


# -------- Index build/load --------

def _build_faiss_index(
    urls: List[str],
    files_glob: str,
    index_dir: str,
    use_urls: bool,
    use_files: bool,
) -> FAISS:
    sources: List[Document] = []
    urls_used = urls if use_urls else []
    files_used = _list_txt_files(files_glob) if use_files else []

    if use_urls:
        sources_from_urls = _load_from_urls(urls_used)
        sources.extend(sources_from_urls)
    if use_files:
        sources_from_files = _load_from_files(files_glob)
        sources.extend(sources_from_files)

    if not sources:
        raise ValueError("Aucune source fournie : active les URLs et/ou les fichiers .txt.")

    print(f"[index] Total documents avant split: {len(sources)}")
    splits = split_documents(sources)
    print(f"[index] Split terminé: {len(sources)} → {len(splits)} chunks (chunk={CHUNK_SIZE}, overlap={CHUNK_OVERLAP})")

    embeddings = get_embeddings()
    print(f"[index] Construction FAISS (chunks={len(splits)}) …")
    vs = FAISS.from_documents(splits, embeddings)

    _ensure_dir(index_dir)
    vs.save_local(index_dir)

    meta = {
        "fingerprint": _fingerprint(urls_used, files_glob if use_files else "", CHUNK_SIZE, CHUNK_OVERLAP),
        "urls": urls_used,
        "files_glob": files_glob if use_files else "",
        "files_sig": _files_sig(files_used),
        "chunk_size": CHUNK_SIZE,
        "chunk_overlap": CHUNK_OVERLAP,
        "backend": "faiss",
        "use_urls": use_urls,
        "use_files": use_files,
        "counts": {
            "urls": len(urls_used),
            "files": len(files_used),
            "sources": len(sources),
            "chunks": len(splits),
        },
    }
    _write_meta(index_dir, meta)
    print(f"[index] Saved to {index_dir}")
    return vs

def _load_faiss_index(index_dir: str) -> FAISS:
    print(f"[index] Loading FAISS index from {index_dir} …")
    embeddings = get_embeddings()
    return FAISS.load_local(index_dir, embeddings, allow_dangerous_deserialization=True)


# -------- Public API --------

def get_retriever(
    index_dir: str,
    urls: List[str],
    files_glob: str,
    use_urls: bool = True,
    use_files: bool = True,
    force_rebuild: bool = False,
):
    """
    Charge ou (re)construit un index FAISS persistant, et renvoie un retriever.
    Les sources peuvent venir d'URLs, de fichiers .txt locaux (ou des deux).
    La décision rebuild / reload se fait via un fingerprint (URLs + signature des fichiers + params de split).
    """
    desired_fp = _fingerprint(urls if use_urls else [], files_glob if use_files else "", CHUNK_SIZE, CHUNK_OVERLAP)
    meta = _read_meta(index_dir)

    must_rebuild = (
        force_rebuild
        or (meta is None)
        or (meta.get("fingerprint") != desired_fp)
    )

    if must_rebuild:
        vs = _build_faiss_index(
            urls=urls if use_urls else [],
            files_glob=files_glob if use_files else "",
            index_dir=index_dir,
            use_urls=use_urls,
            use_files=use_files,
        )
    else:
        vs = _load_faiss_index(index_dir)
        meta_reload = _read_meta(index_dir) or {}
        counts = meta_reload.get("counts", {})
        print(
            "[index] Reuse persisted index: "
            f"chunks≈{counts.get('chunks', '?')}, urls={counts.get('urls', '?')}, "
            f"files={counts.get('files', '?')}, glob='{meta_reload.get('files_glob', '')}'"
        )

    return vs.as_retriever()
