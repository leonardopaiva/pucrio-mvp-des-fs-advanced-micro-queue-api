from pydantic import BaseModel
from typing import List
from model.user import User


class UserSchema(BaseModel):
    """ Define como um novo user a ser inserido deve ser representado
    """
    name: str = "Leonardo Paiva"
    email: str = "leonardopaiva.portfolio@gmail.com"
    password: str = "123123"


class UserBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no name do user.
    """
    name: str = "Leonardo Paiva"


class ListagemUsersSchema(BaseModel):
    """ Define como uma listagem de users será retornada.
    """
    users:List[UserSchema]


def apresenta_users(users: List[User]):
    """ Retorna uma representação do user seguindo o schema definido em
        UserViewSchema.
    """
    result = []
    for user in users:
        result.append({
            "name": user.name,
            "email": user.email
        })

    return {"users": result}


class UserViewSchema(BaseModel):
    """ Define como um user será retornado: user + comentários.
    """
    id: int = 1
    name: str = "Leonardo Paiva"
    email: str = "leonardopaiva.portfolio@gmail.com"
    password: str = "123123"


class UserDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    message: str
    name: str

def apresenta_user(user: User):
    """ Retorna uma representação do user seguindo o schema definido em
        UserViewSchema.
    """
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "password": user.password
    }
