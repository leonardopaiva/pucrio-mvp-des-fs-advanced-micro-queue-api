from sqlalchemy import Column, String, Integer, DateTime, Float
from datetime import datetime
from typing import Union

from  model import Base


class User(Base):
    __tablename__ = 'user'

    id = Column("pk_user", Integer, primary_key=True)
    name = Column(String(140), unique=True)
    email = Column(String(140), unique=True)
    password = Column(String(140), unique=True)
    data_insercao = Column(DateTime, default=datetime.now())

    def __init__(self, name:str, email: str, password: str,
                 data_insercao:Union[DateTime, None] = None):
        """
        Cria um User

        Arguments:
            name: name do user.
            email: e-mail do usuário.
            password: password para validar usuario.
            data_insercao: data de quando o user foi inserido à base
        """
        self.name = name
        self.email = email
        self.password = password

        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao