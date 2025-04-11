from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum

class EventType(Enum):
    CONSULTATION = 1
    EXAM = 2

class EventSchema(BaseModel):
    name: str = "Consulta Dermatologista"
    description: str = "A consulta será por ordem de chegada"
    observation: str = "Vou precisar de ajuda para ir até a consulta porque o carro está quebrado"
    date: datetime = datetime.now()
    doctor_name: str = "Doutor Matheus"
    location_name: str = "memorial são jose recife 83"
    location_id: int = 1
    doctor_id: int = 1
    user_id: str = "default_user_id"
    type: EventType = EventType.CONSULTATION
