from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect

from schemas import *
from services import *
# from routes import *
from flask_cors import CORS

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
produto_tag = Tag(name="Produto", description="Adição, visualização e remoção de produtos à base (testado)") #testado
event_tag = Tag(name="Event", description="Adição, visualização e remoção de events à base (testado)") #testado
user_tag = Tag(name="User", description="Adição, visualização e remoção de users à base (testado)")  # testado
doctor_tag = Tag(name="Doctor", description="Adição, visualização e remoção de doctors à base (testado)") # testado
specialty_tag = Tag(name="Specialty", description="Adição, visualização e remoção de Specialties à base (testado)") #testado
location_tag = Tag(name="Location", description="Adição, visualização e remoção de locations à base (testado)") # testado
comentario_tag = Tag(name="Comentario", description="Adição de um comentário à um doctor ou event cadastrado na base")

@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')

#///////////////////////////////////////////////////////////////////////////////////////
#PRODUTOS
#///////////////////////////////////////////////////////////////////////////////////////
@app.post('/produto', tags=[produto_tag],
          responses={"200": ProdutoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_produto(form: ProdutoSchema):
    """Adiciona um novo Produto à base de dados

    Retorna uma representação dos produtos e comentários associados.
    """
    return ProdutoService.add_produto(form)


@app.get('/produtos', tags=[produto_tag],
         responses={"200": ListagemProdutosSchema, "404": ErrorSchema})
def get_produtos():
    """Faz a busca por todos os Produto cadastrados

    Retorna uma representação da listagem de produtos.
    """
    return ProdutoService.get_produtos()


@app.get('/produto', tags=[produto_tag],
         responses={"200": ProdutoViewSchema, "404": ErrorSchema})
def get_produto(query: ProdutoBuscaSchema):
    """Faz a busca por um Produto a partir do id do produto

    Retorna uma representação dos produtos e comentários associados.
    """
    return ProdutoService.get_produto(query)


@app.delete('/produto', tags=[produto_tag],
            responses={"200": ProdutoDelSchema, "404": ErrorSchema})
def del_produto(query: ProdutoBuscaSchema):
    """Deleta um Produto a partir do nome de produto informado

    Retorna uma mensagem de confirmação da remoção.
    """
    return ProdutoService.del_produto(query)
    


#///////////////////////////////////////////////////////////////////////////////////////
#EVENTS
#///////////////////////////////////////////////////////////////////////////////////////
@app.post('/event', tags=[event_tag],
          responses={"200": EventViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_event(form: EventSchema):
    """Adiciona um novo Event à base de dados

    Retorna uma representação dos events e comentários associados.
    """
    return EventService.add_event(form)


@app.get('/events', tags=[event_tag],
         responses={"200": ListagemEventsSchema, "404": ErrorSchema})
def get_events():
    """Faz a busca por todos os Event cadastrados

    Retorna uma representação da listagem de events.
    """
    return EventService.get_events()


@app.get('/event', tags=[event_tag],
         responses={"200": EventViewSchema, "404": ErrorSchema})
def get_event(query: EventBuscaSchema):
    """Faz a busca por um Event a partir do id do event

    Retorna uma representação dos events e comentários associados.
    """
    return EventService.get_event(query)


@app.delete('/event', tags=[event_tag],
            responses={"200": EventDelSchema, "404": ErrorSchema})
def del_event(query: EventBuscaSchema):
    """Deleta um Event a partir do name de event informado

    Retorna uma mensagem de confirmação da remoção.
    """
    return EventService.del_event(query)

#///////////////////////////////////////////////////////////////////////////////////////
#SPECIALTIES
#///////////////////////////////////////////////////////////////////////////////////////
@app.post('/specialty', tags=[specialty_tag],
          responses={"200": SpecialtyViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_specialty(form: SpecialtySchema):
    """Adiciona um novo Specialty à base de dados

    Retorna uma representação dos specialties e comentários associados.
    """
    return SpecialtyService.add_specialty(form)


@app.get('/specialties', tags=[specialty_tag],
         responses={"200": ListagemSpecialtiesSchema, "404": ErrorSchema})
def get_specialties():
    """Faz a busca por todos os Specialty cadastrados

    Retorna uma representação da listagem de specialties.
    """
    return SpecialtyService.get_specialties()
    


@app.get('/specialty', tags=[specialty_tag],
         responses={"200": SpecialtyViewSchema, "404": ErrorSchema})
def get_specialty(query: SpecialtyBuscaSchema):
    """Faz a busca por um Specialty a partir do name do specialty

    Retorna uma representação dos specialties e comentários associados.
    """
    return SpecialtyService.get_specialty(query)


@app.delete('/specialty', tags=[specialty_tag],
            responses={"200": SpecialtyDelSchema, "404": ErrorSchema})
def del_specialty(query: SpecialtyBuscaSchema):
    """Deleta um Specialty a partir do name de specialty informado

    Retorna uma mensagem de confirmação da remoção.
    """
    return SpecialtyService.del_specialty(query)

#///////////////////////////////////////////////////////////////////////////////////////
#LOCATIONS
#///////////////////////////////////////////////////////////////////////////////////////
@app.post('/location', tags=[location_tag],
          responses={"200": LocationViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_location(form: LocationSchema):
    """Adiciona um novo Location à base de dados

    Retorna uma representação dos locations e comentários associados.
    """
    return LocationService.add_location(form)


@app.get('/locations', tags=[location_tag],
         responses={"200": ListagemLocationsSchema, "404": ErrorSchema})
def get_locations():
    """Faz a busca por todos os Location cadastrados

    Retorna uma representação da listagem de locations.
    """
    return LocationService.get_locations()    


@app.get('/location', tags=[location_tag],
         responses={"200": LocationViewSchema, "404": ErrorSchema})
def get_location(query: LocationBuscaSchema):
    """Faz a busca por um Location a partir do id do location

    Retorna uma representação dos locations e comentários associados.
    """
    return LocationService.get_location(query)


@app.delete('/location', tags=[location_tag],
            responses={"200": LocationDelSchema, "404": ErrorSchema})
def del_location(query: LocationBuscaSchema):
    """Deleta um Location a partir do name de location informado

    Retorna uma mensagem de confirmação da remoção.
    """
    return LocationService.del_location(query)

#///////////////////////////////////////////////////////////////////////////////////////
#DOCTORS
#///////////////////////////////////////////////////////////////////////////////////////
@app.post('/doctor', tags=[doctor_tag],
          responses={"200": DoctorViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_doctor(form: DoctorSchema):
    """Adiciona um novo Doctor à base de dados

    Retorna uma representação dos doctors e comentários associados.
    """
    return DoctorService.add_doctor(form)


@app.get('/doctors', tags=[doctor_tag],
         responses={"200": ListagemDoctorsSchema, "404": ErrorSchema})
def get_doctors():
    """Faz a busca por todos os Doctor cadastrados

    Retorna uma representação da listagem de doctors.
    """
    return DoctorService.get_doctors()


@app.get('/doctor', tags=[doctor_tag],
         responses={"200": DoctorViewSchema, "404": ErrorSchema})
def get_doctor(query: DoctorBuscaSchema):
    """Faz a busca por um Doctor a partir do id do doctor

    Retorna uma representação dos doctors e comentários associados.
    """
    return DoctorService.get_doctor(query)


@app.delete('/doctor', tags=[doctor_tag],
            responses={"200": DoctorDelSchema, "404": ErrorSchema})
def del_doctor(query: DoctorBuscaSchema):
    """Deleta um Doctor a partir do name de doctor informado

    Retorna uma mensagem de confirmação da remoção.
    """
    return DoctorService.del_doctor(query)

    
#///////////////////////////////////////////////////////////////////////////////////////
#USERS
#///////////////////////////////////////////////////////////////////////////////////////
@app.post('/user', tags=[user_tag],
          responses={"200": UserViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_user(form: UserSchema):
    """Adiciona um novo User à base de dados

    Retorna uma representação dos users e comentários associados.
    """
    return UserService.add_user(form)


@app.get('/users', tags=[user_tag],
         responses={"200": ListagemUsersSchema, "404": ErrorSchema})
def get_users():
    """Faz a busca por todos os User cadastrados

    Retorna uma representação da listagem de users.
    """
    UserService.get_users()


@app.get('/user', tags=[user_tag],
         responses={"200": UserViewSchema, "404": ErrorSchema})
def get_user(query: UserBuscaSchema):
    """Faz a busca por um User a partir do id do user

    Retorna uma representação dos users e comentários associados.
    """
    return UserService.get_user(query)


@app.delete('/user', tags=[user_tag],
            responses={"200": UserDelSchema, "404": ErrorSchema})
def del_user(query: UserBuscaSchema):
    """Deleta um User a partir do name de user informado

    Retorna uma mensagem de confirmação da remoção.
    """
    return UserService.del_user(query)


#///////////////////////////////////////////////////////////////////////////////////////
#COMENTARIOS
#///////////////////////////////////////////////////////////////////////////////////////
@app.post('/comentario/doctor', tags=[comentario_tag],
          responses={"200": DoctorViewSchema, "404": ErrorSchema})
def add_comentario_doctor(form: ComentarioSchema):
    """Adição de um novo comentário à um doctor cadastrado na base identificado pelo id

    Retorna uma representação do doctor e comentários associados.
    """
    return DoctorService.add_comentario(form)

@app.post('/comentario/event', tags=[comentario_tag],
          responses={"200": DoctorViewSchema, "404": ErrorSchema})
def add_comentario_event(form: ComentarioSchema):
    """Adição de um novo comentário à um event cadastrado na base identificado pelo id

    Retorna uma representação do event e comentários associados.
    """
    return EventService.add_comentario(form)
    