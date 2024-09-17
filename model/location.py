from sqlalchemy import Column, Numeric, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base, Comentario


class Location(Base):
    __tablename__ = 'location'

    id = Column("pk_location", Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    street = Column(String(255), nullable=False)
    number = Column(String(10), nullable=False)
    complement = Column(String(255), nullable=True)
    neighborhood = Column(String(255), nullable=True)
    city = Column(String(255), nullable=True)
    state = Column(String(2), nullable=True)
    postal_code = Column(String(10), unique=True, nullable=True)
    country = Column(String(255), nullable=True)
    phone = Column(String(255), nullable=True)
    phone_b = Column(String(255), nullable=True)
    observation = Column(String(255), nullable=True)
    data_insercao = Column(DateTime, default=datetime.now())

    # Definição do relacionamento entre o location e o comentário.
    # Essa relação é implicita, não está salva na tabela 'location',
    # mas aqui estou deixando para SQLAlchemy a responsabilidade
    # de reconstruir esse relacionamento.
    comentarios = relationship("Comentario")

    def __init__(self,
                name: str,
                street: str,
                number: str,
                complement: str,
                neighborhood: str,
                city: str,
                state: str,
                postal_code: str,
                country: str,
                phone: str,
                phone_b: str,
                observation: str,
                data_insercao:Union[DateTime, None] = None):
        """
        Cria um Location

        Arguments:
            self.name: Location name,
            self.street: Location street,
            self.number: Location number,
            self.complement: Complement exemplo apt 2020,
            self.neighborhood: location neighborhood (bairro),
            self.city = city,
            self.state = state,
            self.postal_code = postal_code,
            self.country = country,
            self.phone = first phone number,
            self.phone_b = second phone number,
            self.observation = any aditional information about the location,
            data_insercao: data de quando o location foi inserido à base
        """
        self.name = name
        self.street = street
        self.number = number
        self.complement = complement
        self.neighborhood = neighborhood
        self.city = city
        self.state = state
        self.postal_code = postal_code
        self.country = country
        self.phone = phone
        self.phone_b = phone_b
        self.observation = observation

        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao

    def adiciona_comentario(self, comentario:Comentario):
        """ Adiciona um novo comentário ao Location
        """
        self.comentarios.append(comentario)

