from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base, Comentario


class Specialty(Base):
    __tablename__ = 'specialty'

    id = Column("pk_specialty", Integer, primary_key=True)
    name = Column(String(140), unique=True)
    data_insercao = Column(DateTime, default=datetime.now())

    # Definição do relacionamento entre o specialty e o comentário.
    # Essa relação é implicita, não está salva na tabela 'specialty',
    # mas aqui estou deixando para SQLAlchemy a responsabilidade
    # de reconstruir esse relacionamento.
    comentarios = relationship("Comentario")

    def __init__(self, name:str,
                 data_insercao:Union[DateTime, None] = None):
        """
        Cria um Specialty

        Arguments:
            name: name do specialty.
            data_insercao: data de quando o specialty foi inserido à base
        """
        self.name = name

        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao

    def adiciona_comentario(self, comentario:Comentario):
        """ Adiciona um novo comentário ao Specialty
        """
        self.comentarios.append(comentario)

