from sqlalchemy.exc import IntegrityError
from urllib.parse import unquote
from model import Session, Specialty
from schemas.specialty import SpecialtySchema, SpecialtyBuscaSchema, \
                            apresenta_specialties, \
                            apresenta_specialty, apresenta_specialties
from logger import logger

class SpecialtyService:
    def add_specialty(form: SpecialtySchema):
        specialty = Specialty(
        name=form.name)
        logger.debug(f"Adicionando specialty de name: '{specialty.name}'")
        try:
            # criando conexão com a base
            session = Session()
            # adicionando specialty
            session.add(specialty)
            # efetivando o camando de adição de novo item na tabela
            session.commit()
            logger.debug(f"Adicionado specialty de name: '{specialty.name}'")
            return apresenta_specialty(specialty), 200

        except IntegrityError as e:
            # como a duplicidade do name é a provável razão do IntegrityError
            error_msg = "Specialty de mesmo name já salvo na base :/"
            logger.warning(f"Erro ao adicionar specialty '{specialty.name}', {error_msg}")
            return {"message": error_msg}, 409

        except Exception as e:
            # caso um erro fora do previsto
            error_msg = "Não foi possível salvar novo item :/"
            logger.warning(f"Erro ao adicionar specialty '{specialty.name}', {error_msg}")
            return {"message": error_msg}, 400
    
    def get_specialties():
        logger.debug(f"Coletando specialties ")
        # criando conexão com a base
        session = Session()
        # fazendo a busca
        specialties = session.query(Specialty).all()

        if not specialties:
            # se não há specialties cadastrados
            return {"specialties": []}, 200
        else:
            logger.debug(f"%d rodutos econtrados" % len(specialties))
            # retorna a representação de specialty
            print(specialties)
            return apresenta_specialties(specialties), 200
    
    def get_specialty(query: SpecialtyBuscaSchema):
        name = query.name
        logger.debug(f"Coletando dados sobre specialty #{name}")
        # criando conexão com a base
        session = Session()
        # fazendo a busca
        specialty = session.query(Specialty).filter(Specialty.name == name).first()

        if not specialty:
            # se o specialty não foi encontrado
            error_msg = "Specialty não encontrado na base :/"
            logger.warning(f"Erro ao buscar specialty '{name}', {error_msg}")
            return {"message": error_msg}, 404
        else:
            logger.debug(f"Specialty econtrado: '{specialty.name}'")
            # retorna a representação de specialty
            return apresenta_specialty(specialty), 200
    
    def del_specialty(query: SpecialtyBuscaSchema):
        specialty_name = unquote(unquote(query.name))
        print(specialty_name)
        logger.debug(f"Deletando dados sobre specialty #{specialty_name}")
        # criando conexão com a base
        session = Session()
        # fazendo a remoção
        count = session.query(Specialty).filter(Specialty.name == specialty_name).delete()
        session.commit()

        if count:
            # retorna a representação da mensagem de confirmação
            logger.debug(f"Deletado specialty #{specialty_name}")
            return {"message": "Specialty removido", "id": specialty_name}
        else:
            # se o specialty não foi encontrado
            error_msg = "Specialty não encontrado na base :/"
            logger.warning(f"Erro ao deletar specialty #'{specialty_name}', {error_msg}")
            return {"message": error_msg}, 404