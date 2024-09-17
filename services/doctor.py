from sqlalchemy.exc import IntegrityError
from urllib.parse import unquote
from model import Session, Doctor, Comentario
from schemas.doctor import DoctorSchema, DoctorBuscaSchema, \
                            apresenta_doctors, \
                            apresenta_doctor, apresenta_doctors
from logger import logger

class DoctorService:
    def add_doctor(form: DoctorSchema):
        doctor = Doctor(
            name=form.name,
            email=form.email,
            phone=form.phone,
            observation=form.observation,
            location_id=form.location_id,
            specialty_id=form.specialty_id)
        
        logger.debug(f"Adicionando doctor de name: '{doctor.name}'")

        try:
            # criando conexão com a base
            session = Session()
            # adicionando doctor
            session.add(doctor)
            # efetivando o camando de adição de novo item na tabela
            session.commit()
            logger.debug(f"Adicionado doctor de name: '{doctor.name}'")
            return apresenta_doctor(doctor), 200

        except IntegrityError as e:
            # como a duplicidade do name é a provável razão do IntegrityError
            error_msg = "Doctor de mesmo name já salvo na base :/"
            logger.warning(f"Erro ao adicionar doctor '{doctor.name}', {error_msg}, {e}")
            return {"message": error_msg}, 409

        except Exception as e:
            # caso um erro fora do previsto
            error_msg = "Não foi possível salvar novo item :/"
            logger.warning(f"Erro ao adicionar doctor '{doctor.name}', {error_msg}, {e}")
            return {"message": error_msg}, 400
    
    def get_doctors():
        logger.debug(f"Coletando doctors ")
        # criando conexão com a base
        session = Session()
        # fazendo a busca
        doctors = session.query(Doctor).all()

        if not doctors:
            # se não há doctors cadastrados
            return {"doctors": []}, 200
        else:
            logger.debug(f"%d rodutos econtrados" % len(doctors))
            # retorna a representação de doctor
            print(doctors)
            return apresenta_doctors(doctors), 200
    
    def get_doctor(query: DoctorBuscaSchema):
        doctor_name = query.name
        logger.debug(f"Coletando dados sobre doctor #{doctor_name}")
        # criando conexão com a base
        session = Session()
        # fazendo a busca
        doctor = session.query(Doctor).filter(Doctor.name == doctor_name).first()

        if not doctor:
            # se o doctor não foi encontrado
            error_msg = "Doctor não encontrado na base :/"
            logger.warning(f"Erro ao buscar doctor '{doctor_name}', {error_msg}")
            return {"message": error_msg}, 404
        else:
            logger.debug(f"Doctor econtrado: '{doctor.name}'")
            # retorna a representação de doctor
            return apresenta_doctor(doctor), 200
    
    def del_doctor(query: DoctorBuscaSchema):
        doctor_name = unquote(unquote(query.name))
        print(doctor_name)
        logger.debug(f"Deletando dados sobre doctor #{doctor_name}")
        # criando conexão com a base
        session = Session()
        # fazendo a remoção
        count = session.query(Doctor).filter(Doctor.name == doctor_name).delete()
        session.commit()

        if count:
            # retorna a representação da mensagem de confirmação
            logger.debug(f"Deletado doctor #{doctor_name}")
            return {"message": "Doctor removido", "id": doctor_name}
        else:
            # se o doctor não foi encontrado
            error_msg = "Doctor não encontrado na base :/"
            logger.warning(f"Erro ao deletar doctor #'{doctor_name}', {error_msg}")
            return {"message": error_msg}, 404
    
    def add_comentario(form):
        try:
            doctor_id  = form.doctor_id

            if not doctor_id:
                error_msg = "Doctor id inválido :/"
                logger.warning(f"Operação inválida '{doctor_id}', {error_msg}")
                return {"message": error_msg}, 404
            
            logger.debug(f"Adicionando comentários ao doctor #{doctor_id}")
            # criando conexão com a base
            session = Session()
            # fazendo a busca pelo produto
            doctor = session.query(Doctor).filter(Doctor.id == doctor_id).first()

            if not doctor:
                # se produto não encontrado
                error_msg = "Doctor não encontrado na base :/"
                logger.warning(f"Erro ao adicionar comentário ao produto '{doctor_id}', {error_msg}")
                return {"message": error_msg}, 404

            # criando o comentário
            texto = form.texto
            comentario = Comentario(texto)

            # adicionando o comentário ao produto
            doctor.adiciona_comentario(comentario)
            session.commit()

            logger.debug(f"Adicionado comentário ao doctor #{doctor_id}")

            # retorna a representação de doctor
            return apresenta_doctor(doctor), 200
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