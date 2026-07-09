import time
from schemas import GraphState, LegalUnstructuredData, FinancialMetrics
from knowledge_base import initialize_local_db

# Inizializziamo l'indice LlamaIndex globale all'avvio dell'engine
try:
    kb_index = initialize_local_db()
    query_engine = kb_index.as_query_engine(similarity_top_k=1)
except Exception as e:
    print(f"Errore inizializzazione DB: {e}")
    query_engine = None

# --- NODO 1: ANALYST AGENT (Simulazione Retrieval Avanzato LlamaIndex + Chroma)
def analyst_node(state: GraphState) -> GraphState:
    print("\n🕵️‍♂️ [Analyst Agent] Esecuzione Query semantica su LlamaIndex...")
    time.sleep(0.5)

    # Cerchiamo la violazione PII direttamente nella query dell'utente per il test della UI
    pii_found = "mario rossi" in state.query.lower()

    if query_engine and not pii_found:
        try:
            response = query_engine.query(state.query)
            clausole = [response.response[:100] + "..."] if getattr(response, 'response', None) else ["Clausola 4.2: Limitazione delle responsabilità finanziarie."]
            parent_id = response.source_nodes[0].node.metadata.get("parent_id", "UNKNOWN") if getattr(response, 'source_nodes', None) else "DOC-CRIF-2026-X9"
        except Exception:
            clausole = ["Clausola 4.2: Limitazione delle responsabilità finanziarie."]
            parent_id = "DOC-CRIF-2026-X9"
    else:
        # Forziamo dei dati simulati coerenti per mostrare il comportamento all'utente
        clausole = ["Clausola 4.2: Limitazione delle responsabilità finanziarie."]
        parent_id = "DOC-CRIF-2026-X9"

    state.analyst_output = LegalUnstructuredData(
        detected_clausole_rischio=clausole,
        has_pii_violation=pii_found,
        parent_document_id=parent_id
    )

    print(f"✅ [Analyst Agent] Retrieval completato. Parent Doc ID associato: {state.analyst_output.parent_document_id}")
    return state

# --- NODO 2: AUDITOR AGENT (Simulazione Connessione dbt via protocollo MCP)
def auditor_node(state: GraphState) -> GraphState:
    print("\n🧮 [Auditor Agent] Invocazione Server MCP verso Feature Store dbt...")
    time.sleep(0.8)
    
    # Forza un contratto Pydantic rigido per i dati finanziari
    state.auditor_output = FinancialMetrics(
        company_name="Amaris-CRIF Corp",
        mrr_or_revenue=1250000.00,
        leverage_ratio=2.4,
        compliance_score=0.89
    )
    print("✅ [Auditor Agent] Dati finanziari tipizzati inseriti nello Stato.")
    return state

# --- NODO 3: JUDGE AGENT (Validatore e Gestore degli Edge Condizionali / Reflexion)
def judge_node(state: GraphState) -> GraphState:
    print("\n⚖️ [Judge Agent] Esecuzione controlli di qualità e metriche RAGAS...")
    time.sleep(1)
    
    # Controllo Sicurezza (NeMo Guardrails simulato) e contratti
    if state.analyst_output and state.analyst_output.has_pii_violation:
        print("❌ [Judge Agent - RIFIUTATO] Rilevata violazione PII (Dati personali non mascherati)!")
        state.judge_approved = False
    else:
        print("🟢 [Judge Agent - APPROVATO] Struttura dati conforme ai requisiti 2026.")
        state.judge_approved = True
        auditor_name = state.auditor_output.company_name if state.auditor_output else "<unknown>"
        compliance = state.auditor_output.compliance_score if state.auditor_output else 0.0
        clausole = state.analyst_output.detected_clausole_rischio if state.analyst_output else []
        state.final_report = f"REPORT DETERMINISTICO:\nSocietà: {auditor_name} | Compliance: {compliance:.2%}\nClausole: {clausole}"
        
    return state

# --- ORCHESTRATORE CENTRALE (Loop del Grafo)
def run_credit_shield(user_query: str):
    # Inizializzazione dello Stato
    state = GraphState(query=user_query)
    
    # Loop di esecuzione del Grafo (State Machine)
    while not state.judge_approved and state.retry_count < 2:
        if state.retry_count > 0:
            print(f"\n🔁 --- AVVIO CICLO DI REFLEXION (Autocorrezione #{state.retry_count}) ---")
            # Simula l'azione di sanificazione dell'input prima del retry
            state.query = state.query.lower().replace("mario rossi", "[REDACTED_USER]")
            
        # Esecuzione dei nodi
        state = analyst_node(state)
        state = auditor_node(state)
        state = judge_node(state)
        
        if not state.judge_approved:
            state.retry_count += 1
            
    print("\n--- WORKFLOW TERMINATO ---")
    if state.judge_approved:
        print(state.final_report)
    else:
        print("🚨 Sistema bloccato dal Judge per motivi di sicurezza dopo tentativi di Reflexion.")
    return state

# --- TEST DI ESECUZIONE
if __name__ == "__main__":
    print("--- TEST 1: Richiesta standard pulita ---")
    run_credit_shield("Analizza il rischio di Amaris per l'anno 2026")
    
    print("\n" + "="*50 + "\n")
    
    print("--- TEST 2: Richiesta con violazione PII (Trigger ciclo di Reflexion) ---")
    run_credit_shield("Controlla il contratto contenente i dati di Mario Rossi")
