from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Literal

class SyncItem(BaseModel):
    id: Optional[str] = Field(None, description="Identificador único do item (opcional, se não fornecido será gerado).")
    domain: Literal["appointment", "doctor", "address"] = Field(..., description="Domínio do item. Valores permitidos: 'appointment', 'doctor' ou 'address'.")
    action: Literal["create", "update", "delete"] = Field(..., description="Ação a ser executada. Valores permitidos: 'create', 'update' ou 'delete'.")
    data: Dict[str, Any] = Field(..., description="Dados do item para sincronização.")

class ProcessSyncSchema(BaseModel):
    items: List[SyncItem] = Field(..., description="Lista de itens a serem sincronizados.")
