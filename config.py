import os

#Estas configs serão carregadas das variaveis de ambiente definidas no docker-compose.yml
#Exemplo, caso não encontre a variável MICRO_APPOINTMENTS_URL 
#será definido MICRO_APPOINTMENTS_URL como http://192.168.56.101:5044
MICRO_APPOINTMENTS_URL = os.getenv("MICRO_APPOINTMENTS_URL", "http://192.168.56.101:5044")
MICRO_DOCTORS_URL = os.getenv("MICRO_DOCTORS_URL", "http://localhost:6001")
MICRO_ADDRESS_URL = os.getenv("MICRO_ADDRESS_URL", "http://localhost:6002")
