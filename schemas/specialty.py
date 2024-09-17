from pydantic import BaseModel
from typing import Optional, List
from model.specialty import Specialty

from schemas import ComentarioSchema


class SpecialtySchema(BaseModel):
    """ Define como um novo specialty a ser inserido deve ser representado
    """
    name: str = "Dermatologista"


class SpecialtyBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no name do specialty.
    """
    name: str = "Dermatologista"


class ListagemSpecialtiesSchema(BaseModel):
    """ Define como uma listagem de specialties será retornada.
    """
    specialties:List[SpecialtySchema]


def apresenta_specialties(specialties: List[Specialty]):
    """ Retorna uma representação do specialty seguindo o schema definido em
        SpecialtyViewSchema.
    """
    result = []
    for specialty in specialties:
        result.append({
            "name": specialty.name,
        })

    return {"specialties": result}


class SpecialtyViewSchema(BaseModel):
    """ Define como um specialty será retornado: specialty + comentários.
    """
    id: int = 1
    name: str = "Dermatologista"
    total_cometarios: int = 1
    comentarios:List[ComentarioSchema]


class SpecialtyDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    message: str
    name: str

def apresenta_specialty(specialty: Specialty):
    """ Retorna uma representação do specialty seguindo o schema definido em
        SpecialtyViewSchema.
    """
    return {
        "id": specialty.id,
        "name": specialty.name,
        "total_cometarios": len(specialty.comentarios),
        "comentarios": [{"texto": c.texto} for c in specialty.comentarios]
    }
