import chromadb
from llama_index.core import Document, VectorStoreIndex, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from typing import List


# Minimal, deterministic mock embeddings to avoid heavy external models
class MockEmbeddings:
    def __init__(self, dim: int = 8):
        self.dim = dim

    def _text_to_vector(self, text: str) -> List[float]:
        h = abs(hash(text))
        vec = []
        for i in range(self.dim):
            # deterministic pseudo-random but lightweight
            vec.append(((h >> (i * 4)) & 0xFF) / 255.0)
        return vec

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return [self._text_to_vector(t) for t in texts]

    def embed_query(self, text: str) -> List[float]:
        return self._text_to_vector(text)

def initialize_local_db():
    print("📦 [Infrastruttura] Inizializzazione ChromaDB locale in corso...")
    
    # Crea un client persistente sul disco del Chromebook
    db = chromadb.PersistentClient(path="./chroma_db")
    
    # Crea o recupera una collezione per i contratti creditizi
    chroma_collection = db.get_or_create_collection("credit_contracts")
    
    # Configura il Vector Store integrato di LlamaIndex
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    
    # Prepariamo dei dati Mock strutturati (Simulazione contratti reali Amaris/CRIF)
    # Applichiamo concettualmente il Semantic Chunking con metadati Parent-Child
    documents = [
        Document(
            text="Contratto di Finanziamento Quadro 2026. Il Gruppo Internazionale Amaris-CRIF Corp dichiara una linea di credito di emergenza. Nota di sicurezza: l'amministratore delegato delegato per le operazioni sensibili risponde al nome di Mario Rossi.",
            metadata={"parent_id": "DOC-CRIF-2026-X9", "category": "Legal"}
        ),
        Document(
            text="Clausola 4.2: Limitazione delle responsabilità finanziarie. Qualora l'indice di indebitamento (leverage ratio) superi la soglia critica di 3.0, CRIF si riserva il diritto di revisione immediata del tasso di interesse applicato.",
            metadata={"parent_id": "DOC-CRIF-2026-X9", "category": "Risk_Management"}
        )
    ]
    
    # Costruiamo l'indice (LlamaIndex gestirà i nodi)
    # Utilizza un modello di embedding di default leggerissimo per la manipolazione strutturata
    # Usa un modello di embedding locale leggero (mock) per Chromebook
    mock_embed = MockEmbeddings(dim=8)
    index = VectorStoreIndex.from_documents(
        documents, storage_context=storage_context, embed_model=mock_embed
    )
    print("✅ [Infrastruttura] Knowledge Base indicizzata con successo su ChromaDB via LlamaIndex.")
    return index

if __name__ == "__main__":
    initialize_local_db()
