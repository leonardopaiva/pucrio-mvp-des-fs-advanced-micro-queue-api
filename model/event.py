# from schemas.event import EventType
from sqlalchemy import Column, String, Integer, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union
from enum import Enum

from  model import Base, Comentario

#Para o tipo de evento, procurei algo que fosse parecido com o Enum 
#que estou acostumado a usar no typescript, mesmo que no momento
#possua apenas 1 tipo evento, será melhor para escalar no próximo MVP
class EventType(Enum):
    CONSULTATION = 1
    EXAM = 2

class Event(Base):
    __tablename__ = 'event'

    id = Column("pk_event", Integer, primary_key=True)
    name = Column(String(140), unique=False)
    
    description = Column(String(255), unique=False)
    observation = Column(String(255), unique=False)
    type = Column(Integer)
    date = Column(DateTime, default=datetime.now, unique=False)
    data_insercao = Column(DateTime, default=datetime.now)
    doctor_name = Column(String(140), unique=False)
    location_name = Column(String(140), unique=False)
    #Definição dos relactionamentos com location, doctor e user
    #Location e doctor não são obrigatórios assumindo que o usuário 
    #porém user_id é obrigatório
    location_id = Column(Integer, ForeignKey("location.pk_location"), nullable=True)
    doctor_id = Column(Integer, ForeignKey("doctor.pk_doctor"), nullable=True)
    user_id = Column(Integer, ForeignKey("user.pk_user"), nullable=False)
        
    # Definição do relacionamento entre o event e o comentário.
    # Essa relação é implicita, não está salva na tabela 'event',
    # mas aqui estou deixando para SQLAlchemy a responsabilidade
    # de reconstruir esse relacionamento.
    comentarios = relationship("Comentario")

    def __init__(self, 
                 name:str, 
                 date:DateTime,
                 type: EventType,
                 doctor_name:Union[str, None] = None,
                 location_name:Union[str, None] = None, 
                 description:Union[str, None] = None,
                 observation:Union[str, None] = None,
                 location_id:Union[int, None] = None,
                 doctor_id:Union[int, None] = None,
                 user_id:Union[int, None] = None,
                 data_insercao:Union[DateTime, None] = None):
        """
        Cria um Event

        Arguments:
            name: name do event.
            description: uma descricao mais relacionada ao evento, algo sobre o local ou medico
            observation: uma descricao mais relacionada a alguma necessidade que o paciente vai ter
            date: data e hora do evento
            doctor_name: localizacao do evento (apenas string)
            location_name: localizacao do evento (apenas string)
            location_id: localizacao do evento
            doctor_id: doutor relacionado ao evento caso seja tipo consulta
            user_id: id do usuario que criou o evento
            data_insercao: data de quando o event foi inserido à base
        """
        self.name = name
        self.date = date
        self.type = type.value
        self.description = description
        self.observation = observation
        self.doctor_name = doctor_name
        self.location_name = location_name
        self.location_id = location_id
        self.doctor_id = doctor_id
        self.user_id = user_id or 1

        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao

    def adiciona_comentario(self, comentario:Comentario):
        """ Adiciona um novo comentário ao Event
        """
        self.comentarios.append(comentario)

