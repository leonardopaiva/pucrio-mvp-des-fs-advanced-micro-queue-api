from sqlalchemy.exc import IntegrityError
from urllib.parse import unquote
from model import Session, User
from schemas.user import UserSchema, UserBuscaSchema, \
                            apresenta_users, \
                            apresenta_user, apresenta_users
from logger import logger

class UserService:
    def add_user(form: UserSchema):
        
        user = User(
            name=form.name,
            email=form.email,
            password=form.password)
        
        logger.debug(f"Adicionando user de name: '{user.name}'")
        
        try:
            # criando conexão com a base
            session = Session()
            # adicionando user
            session.add(user)
            # efetivando o camando de adição de novo item na tabela
            session.commit()
            logger.debug(f"Adicionado user de nome: '{user.name}'")
            return apresenta_user(user), 200

        except IntegrityError as e:
            # como a duplicidade do nome é a provável razão do IntegrityError
            error_msg = "User de mesmo nome já salvo na base :/"
            logger.warning(f"Erro ao adicionar user '{user.name}', {error_msg}")
            return {"message": error_msg}, 409

        except Exception as e:
            # caso um erro fora do previsto
            error_msg = "Não foi possível salvar novo item :/ >> "
            logger.warning("************************************* ERROR *****************************")
            logger.warning(f"Erro ao adicionar produto '{user.name}', {error_msg}, {e}")
            logger.warning("*************************************        *****************************")

            return {"message": error_msg}, 400
    
    def get_users():
        logger.warning(f"Coletando users ")
        logger.info('TESTING');
        # criando conexão com a base
        session = Session()
        # fazendo a busca
        users = session.query(User).all()

        if not users:
            # se não há users cadastrados
            return {"users": []}, 200
        else:
            logger.debug(f"%d rodutos econtrados" % len(users))
            # retorna a representação de user
            print(users)
            return apresenta_users(users), 200
    
    def get_user(query: UserBuscaSchema):
        name = query.name
        logger.debug(f"Coletando dados sobre user #{name}")
        # criando conexão com a base
        session = Session()
        # fazendo a busca
        user = session.query(User).filter(User.name == name).first()

        if not user:
            # se o user não foi encontrado
            error_msg = "User não encontrado na base :/"
            logger.warning(f"Erro ao buscar user '{name}', {error_msg}")
            return {"message": error_msg}, 404
        else:
            logger.debug(f"User econtrado: '{user.name}'")
            # retorna a representação de user
            return apresenta_user(user), 200
    
    def del_user(query: UserBuscaSchema):
        user_name = unquote(unquote(query.name))
        print(user_name)
        logger.debug(f"Deletando dados sobre user #{user_name}")
        # criando conexão com a base
        session = Session()
        # fazendo a remoção
        count = session.query(User).filter(User.name == user_name).delete()
        session.commit()

        if count:
            # retorna a representação da mensagem de confirmação
            logger.debug(f"Deletado user #{user_name}")
            return {"message": "User removido", "id": user_name}
        else:
            # se o user não foi encontrado
            error_msg = "User não encontrado na base :/"
            logger.warning(f"Erro ao deletar user #'{user_name}', {error_msg}")
            return {"message": error_msg}, 404