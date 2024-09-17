from sqlalchemy.exc import IntegrityError
from urllib.parse import unquote
from model import Session, Location
from schemas.location import LocationSchema, LocationBuscaSchema, \
                            apresenta_locations, \
                            apresenta_location, apresenta_locations
from logger import logger

class LocationService:
    def add_location(form: LocationSchema):
        location = Location(
        name = form.name,
        street = form.street,
        number = form.number,
        complement = form.complement,
        neighborhood = form.neighborhood,
        city = form.city,
        state = form.state,
        postal_code = form.postal_code,
        country = form.country,
        phone = form.phone,
        phone_b = form.phone_b,
        observation = form.observation)
        logger.debug(f"Adicionando location de name: '{location.name}'")
        try:
            # criando conexão com a base
            session = Session()
            # adicionando location
            session.add(location)
            # efetivando o camando de adição de novo item na tabela
            session.commit()
            logger.debug(f"Adicionado location de name: '{location.name}'")
            return apresenta_location(location), 200

        except IntegrityError as e:
            # como a duplicidade do name é a provável razão do IntegrityError
            error_msg = "Location de mesmo name já salvo na base :/"
            logger.warning(f"Erro ao adicionar location '{location.name}', {error_msg}, {e}")
            return {"message": error_msg}, 409

        except Exception as e:
            # caso um erro fora do previsto
            error_msg = "Não foi possível salvar novo item :/"
            logger.warning(f"Erro ao adicionar location '{location.name}', {error_msg}, {e}")
            return {"message": error_msg}, 400
    
    def get_locations():
        logger.debug(f"Coletando locations ")

        try:
            # criando conexão com a base
            session = Session()
            # fazendo a busca
            locations = session.query(Location).all()

            if not locations:
                # se não há locations cadastrados
                return {"locations": []}, 200
            else:
                logger.debug(f"%d rodutos econtrados" % len(locations))
                # retorna a representação de location
                print(locations)
                return apresenta_locations(locations), 200
        except Exception as e:
            # caso um erro fora do previsto
            error_msg = "Não foi possível buscar locations!"
            logger.warning(f"Erro ao buscar locations, {error_msg}, {e}")
            return {"message": error_msg}, 400
    
    def get_location(query: LocationBuscaSchema):
        location_name = query.name
        logger.debug(f"Coletando dados sobre location #{location_name}")
        # criando conexão com a base
        session = Session()
        # fazendo a busca
        location = session.query(Location).filter(Location.name == location_name).first()

        if not location:
            # se o location não foi encontrado
            error_msg = "Location não encontrado na base :/"
            logger.warning(f"Erro ao buscar location '{location_name}', {error_msg}")
            return {"message": error_msg}, 404
        else:
            logger.debug(f"Location econtrado: '{location.name}'")
            # retorna a representação de location
            return apresenta_location(location), 200
    
    def del_location(query: LocationBuscaSchema):
        location_name = unquote(unquote(query.name))
        print(location_name)
        logger.debug(f"Deletando dados sobre location #{location_name}")
        # criando conexão com a base
        session = Session()
        # fazendo a remoção
        count = session.query(Location).filter(Location.name == location_name).delete()
        session.commit()

        if count:
            # retorna a representação da mensagem de confirmação
            logger.debug(f"Deletado location #{location_name}")
            return {"message": "Location removido", "id": location_name}
        else:
            # se o location não foi encontrado
            error_msg = "Location não encontrado na base :/"
            logger.warning(f"Erro ao deletar location #'{location_name}', {error_msg}")
            return {"message": error_msg}, 404