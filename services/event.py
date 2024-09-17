from sqlalchemy.exc import IntegrityError
from urllib.parse import unquote
from model import Session, Event, Comentario
from schemas.event import EventSchema, EventBuscaSchema, EventViewSchema, \
                            ListagemEventsSchema, EventDelSchema, apresenta_events, \
                            apresenta_event, apresenta_events
from logger import logger

class EventService:
    def add_event(form: EventSchema):
        event = Event(
            name=form.name,
            date=form.date,
            type=form.type,
            description=form.description,
            observation=form.observation,
            doctor_name=form.doctor_name,
            location_name=form.location_name,
            location_id=form.location_id,
            doctor_id = form.doctor_id,
            user_id = form.user_id)
        
        logger.debug(f"Adicionando event de name: '{event.name}'")
        
        try:
            # criando conexão com a base
            session = Session()
            # adicionando event
            session.add(event)
            # efetivando o camando de adição de novo item na tabela
            session.commit()
            logger.debug(f"Adicionado event de name: '{event.name}'")
            return apresenta_event(event), 200

        except IntegrityError as e:
            # como a duplicidade do name é a provável razão do IntegrityError
            error_msg = "Event de mesmo name já salvo na base :/"
            logger.warning(f"Erro ao adicionar event '{event.name}', {error_msg}, {e}")
            return {"message": error_msg}, 409

        except Exception as e:
            # caso um erro fora do previsto
            error_msg = "Não foi possível salvar novo item :/"
            logger.info("****************** ERROR ****************************")
            logger.warning(e)
            logger.info("*************************************************************")
            logger.warning(f"Erro ao adicionar event '{event.name}', {error_msg}, {e}")
            return {"message": error_msg}, 400
    
    def get_events():
        logger.debug(f"Coletando events ")
        # criando conexão com a base
        session = Session()
        # fazendo a busca
        events = session.query(Event).all()

        # logger.info("testando logger")
        if not events:
            # se não há events cadastrados
            return {"events": []}, 200
        else:
            logger.debug(f"%d events encontrados" % len(events))
            # retorna a representação de event
            print(events)
            return apresenta_events(events), 200
    
    def get_event(query: EventBuscaSchema):
        event_name = query.name
        logger.debug(f"Coletando dados sobre event #{event_name}")
        # criando conexão com a base
        session = Session()
        # fazendo a busca
        event = session.query(Event).filter(Event.name == event_name).first()

        if not event:
            # se o event não foi encontrado
            error_msg = "Event não encontrado na base :/"
            logger.warning(f"Erro ao buscar event '{event_name}', {error_msg}")
            return {"message": error_msg}, 404
        else:
            logger.debug(f"Event econtrado: '{event.name}'")
            # retorna a representação de event
            return apresenta_event(event), 200
    
    def del_event(query: EventBuscaSchema):
        event_name = unquote(unquote(query.name))
        print(event_name)
        logger.debug(f"Deletando dados sobre event #{event_name}")
        # criando conexão com a base
        session = Session()
        # fazendo a remoção
        count = session.query(Event).filter(Event.name == event_name).delete()
        session.commit()

        if count:
            # retorna a representação da mensagem de confirmação
            logger.debug(f"Deletado event #{event_name}")
            return {"message": "Event removido", "id": event_name}
        else:
            # se o event não foi encontrado
            error_msg = "Event não encontrado na base :/"
            logger.warning(f"Erro ao deletar event #'{event_name}', {error_msg}")
            return {"message": error_msg}, 404
        
    def add_comentario(form):
        try:
            event_id  = form.event_id

            if not event_id:
                error_msg = "Event id inválido :/"
                logger.warning(f"Operação inválida '{event_id}', {error_msg}")
                return {"message": error_msg}, 404
            
            logger.debug(f"Adicionando comentários ao event #{event_id}")
            # criando conexão com a base
            session = Session()
            # fazendo a busca pelo produto
            event = session.query(Event).filter(Event.id == event_id).first()

            if not event:
                # se produto não encontrado
                error_msg = "Event não encontrado na base :/"
                logger.warning(f"Erro ao adicionar comentário ao event '{event_id}', {error_msg}")
                return {"message": error_msg}, 404

            # criando o comentário
            texto = form.texto
            comentario = Comentario(texto)

            # adicionando o comentário ao produto
            event.adiciona_comentario(comentario)
            session.commit()

            logger.debug(f"Adicionado comentário ao event #{event_id}")

            # retorna a representação de doctor
            return apresenta_event(event), 200
        except IntegrityError as e:
                # como a duplicidade do nome é a provável razão do IntegrityError
            error_msg = ""
            logger.warning(f"Erro ao adicionar comentario, {error_msg}, {e}")
            return {"message": error_msg}, 409

        except Exception as e:
            # caso um erro fora do previsto
            error_msg = "Não foi possível salvar novo item :/ >> "
            logger.warning("************************************* ERROR *****************************")
            logger.warning(f"Erro ao adicionar comentário, {error_msg}, {e}")
            logger.warning("*************************************        *****************************")

            return {"message": error_msg}, 400