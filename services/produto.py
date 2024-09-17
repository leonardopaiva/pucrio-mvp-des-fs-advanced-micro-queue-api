from sqlalchemy.exc import IntegrityError
from urllib.parse import unquote
from model import Session, Produto, Comentario
from schemas.produto import ProdutoSchema, ProdutoBuscaSchema, ProdutoViewSchema, \
                            ListagemProdutosSchema, ProdutoDelSchema, apresenta_produtos, \
                            apresenta_produto, apresenta_produtos
from logger import logger

class ProdutoService:
    def add_produto(form: ProdutoSchema):
        produto = Produto(
            name=form.name,
            quantidade=form.quantidade,
            valor=form.valor)
        logger.debug(f"Adicionando produto de name: '{produto.name}'")
        try:
            # criando conexão com a base
            session = Session()
            # adicionando produto
            session.add(produto)
            # efetivando o camando de adição de novo item na tabela
            session.commit()
            logger.debug(f"Adicionado produto de name: '{produto.name}'")
            return apresenta_produto(produto), 200

        except IntegrityError as e:
            # como a duplicidade do name é a provável razão do IntegrityError
            error_msg = "Produto de mesmo name já salvo na base :/"
            logger.warning(f"Erro ao adicionar produto '{produto.name}', {error_msg}")
            return {"message": error_msg}, 409

        except Exception as e:
            # caso um erro fora do previsto
            error_msg = "Não foi possível salvar novo item :/"
            logger.warning("************************************* ERROR *****************************")
            logger.warning(f"Erro ao adicionar produto '{produto.name}', {error_msg}, ** ERROR: ")
            logger.warning("*************************************        *****************************")
            return {"message": error_msg}, 400
    
    def get_produtos():
        logger.debug(f"Coletando produtos ")
        # criando conexão com a base
        session = Session()
        # fazendo a busca
        produtos = session.query(Produto).all()

        if not produtos:
            # se não há produtos cadastrados
            return {"produtos": []}, 200
        else:
            logger.debug(f"%d rodutos econtrados" % len(produtos))
            # retorna a representação de produto
            print(produtos)
            return apresenta_produtos(produtos), 200
    
    def get_produto(query: ProdutoBuscaSchema):
        produto_name = query.name
        logger.debug(f"Coletando dados sobre produto #{produto_name}")
        # criando conexão com a base
        session = Session()
        # fazendo a busca
        produto = session.query(Produto).filter(Produto.id == produto_name).first()

        if not produto:
            # se o produto não foi encontrado
            error_msg = "Produto não encontrado na base :/"
            logger.warning(f"Erro ao buscar produto '{produto_name}', {error_msg}")
            return {"message": error_msg}, 404
        else:
            logger.debug(f"Produto econtrado: '{produto.name}'")
            # retorna a representação de produto
            return apresenta_produto(produto), 200


#             @app.get('/produto', tags=[produto_tag],
#          responses={"200": ProdutoViewSchema, "404": ErrorSchema})
# def get_produto(query: ProdutoBuscaSchema):
#     """Faz a busca por um Produto a partir do id do produto

#     Retorna uma representação dos produtos e comentários associados.
#     """
#     produto_id = query.id
#     logger.debug(f"Coletando dados sobre produto #{produto_id}")
#     # criando conexão com a base
#     session = Session()
#     # fazendo a busca
#     produto = session.query(Produto).filter(Produto.id == produto_id).first()

#     if not produto:
#         # se o produto não foi encontrado
#         error_msg = "Produto não encontrado na base :/"
#         logger.warning(f"Erro ao buscar produto '{produto_id}', {error_msg}")
#         return {"mesage": error_msg}, 404
#     else:
#         logger.debug(f"Produto econtrado: '{produto.nome}'")
#         # retorna a representação de produto
#         return apresenta_produto(produto), 200
    
    def del_produto(query: ProdutoBuscaSchema):
        produto_name = unquote(unquote(query.name))
        print(produto_name)
        logger.debug(f"Deletando dados sobre produto #{produto_name}")
        # criando conexão com a base
        session = Session()
        # fazendo a remoção
        count = session.query(Produto).filter(Produto.name == produto_name).delete()
        session.commit()

        if count:
            # retorna a representação da mensagem de confirmação
            logger.debug(f"Deletado produto #{produto_name}")
            return {"message": "Produto removido", "name": produto_name}
        else:
            # se o produto não foi encontrado
            error_msg = "Produto não encontrado na base :/"
            logger.warning(f"Erro ao deletar produto #'{produto_name}', {error_msg}")
            return {"message": error_msg}, 404