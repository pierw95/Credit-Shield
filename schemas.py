from pydantic import BaseModel, Field
from typing import List, Optional

# 1. Il Contratto dell'Auditor Agent (Dati Finanziari Strutturati via MCP/dbt)
class FinancialMetrics(BaseModel):
    company_name: str = Field(..., description="Nome della società analizzata")
    mrr_or_revenue: float = Field(..., gt=0, description="Ricavi o MRR in Euro")
    leverage_ratio: float = Field(..., description="Indice di indebitamento finanziario")
    compliance_score: float = Field(..., ge=0.0, le=1.0, description="Punteggio di compliance interna")

# 2. Il Contratto dell'Analyst Agent (Dati non strutturati estratti da GraphRAG/LlamaIndex)
class LegalUnstructuredData(BaseModel):
    detected_clausole_rischio: List[str] = Field(default=[], description="Clausole critiche rilevate nei contratti")
    has_pii_violation: bool = Field(..., description="True se ci sono dati personali non mascherati")
    parent_document_id: str = Field(..., description="ID del documento sorgente parent")

# 3. Lo Stato Globale Condiviso del Sistema Multi-Agente (La State Machine)
class GraphState(BaseModel):
    query: str = Field(..., description="La richiesta iniziale dell'utente")
    analyst_output: Optional[LegalUnstructuredData] = None
    auditor_output: Optional[FinancialMetrics] = None
    judge_approved: bool = Field(default=False, description="Approvazione finale del Judge")
    retry_count: int = Field(default=0, description="Numero di cicli di Reflexion eseguiti")
    final_report: str = Field(default="", description="Risultato deterministico finale")
