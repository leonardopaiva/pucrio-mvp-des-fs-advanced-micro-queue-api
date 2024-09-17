from pydantic import BaseModel
from typing import Optional, List
from model.location import Location

from schemas import ComentarioSchema


class LocationSchema(BaseModel):
    """ Define como um novo location a ser inserido deve ser representado
    """
    name: str = "Clínica Miramar"
    street: str = "Rua das ubaias"
    number: str = "123AB"
    complement: str = "Apt 2020"
    neighborhood: str = "Bairro Mardebode"
    city: str = "Recife"
    state: str = "PE"
    postal_code: str = "55555-555"
    country: str = "Brasil"
    phone: str = "55 (81)9999-99999"
    phone_b: str = "55 (81)9999-99999"
    observation: str = "Quando for para esta clínica lembrar de levar fio dental"


class LocationBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no name do location.
    """
    name: str = "Clínica Miramar"


class ListagemLocationsSchema(BaseModel):
    """ Define como uma listagem de locations será retornada.
    """
    locations:List[LocationSchema]


def apresenta_locations(locations: List[Location]):
    """ Retorna uma representação do location seguindo o schema definido em
        LocationViewSchema.
    """
    result = []
    for location in locations:
        result.append({
            "name": location.name,
            "street": location.street,
            "number": location.number,
            "complement": location.complement,
            "neighborhood": location.neighborhood,
            "city": location.city,
            "state": location.state,
            "postal_code": location.postal_code,
            "country": location.country,
            "phone": location.phone,
            "phone_b": location.phone_b,
            "observation": location.observation,
        })

    return {"locations": result}


class LocationViewSchema(BaseModel):
    """ Define como um location será retornado: location + comentários.
    """
    id: int = 1
    name: str = "Clínica Miramar"
    street: str = "Rua das ubaias"
    number: str = "123AB"
    complement: str = "Apt 2020"
    neighborhood: str = "Bairro Mardebode"
    city: str = "Recife"
    state: str = "PE"
    postal_code: str = "55555-555"
    country: str = "Brasil"
    phone: str = "55 (81)9999-99999"
    phone_b: str = "55 (81)9999-99999"
    observation: str = "Quando for para esta clínica lembrar de levar fio dental"
    total_cometarios: int = 1
    comentarios:List[ComentarioSchema]


class LocationDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    message: str
    name: str

def apresenta_location(location: Location):
    """ Retorna uma representação do location seguindo o schema definido em
        LocationViewSchema.
    """
    return {
        "id": location.id,
        "name": location.name,
        "street": location.street,
        "number": location.number,
        "complement": location.complement,
        "neighborhood": location.neighborhood,
        "city": location.city,
        "state": location.state,
        "postal_code": location.postal_code,
        "country": location.country,
        "phone": location.phone,
        "phone_b": location.phone_b,
        "observation": location.observation,
        "total_cometarios": len(location.comentarios),
        "comentarios": [{"texto": c.texto} for c in location.comentarios]
    }
