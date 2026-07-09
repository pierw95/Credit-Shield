import chromadb
from llama_index.core import Document, VectorStoreIndex, StorageContext
from llama_index.core.embeddings import MockEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore

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
    # Utilizza il MockEmbedding nativo di LlamaIndex per mantenere il flusso leggero
    mock_embed = MockEmbedding(embed_dim=384)
    index = VectorStoreIndex.from_documents(
        documents, storage_context=storage_context, embed_model=mock_embed
    )
    print("✅ [Infrastruttura] Knowledge Base indicizzata con successo su ChromaDB via LlamaIndex.")
    return index

if __name__ == "__main__":
    initialize_local_db()
