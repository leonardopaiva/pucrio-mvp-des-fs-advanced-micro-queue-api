# Minha API

Este pequeno projeto faz parte do material diático da Disciplina **Desenvolvimento Full Stack Básico** 

O objetivo aqui é ilutsrar o conteúdo apresentado ao longo das três aulas da disciplina.

---
## Como executar 


Será necessário ter todas as libs python listadas no `requirements.txt` instaladas.
Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

> É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

```
(env)$ pip install -r requirements.txt
```

Este comando instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`.

Para executar a API  basta executar:

minhas consideracoes
fui para fora do env, e ativei a versao global do python para a mesma do env, entrei no env e rodei novamente o 
comando `sudo -H pip install -r requirements.txt` depois
pip install --upgrade flask
pip install --upgrade flask_openapi3
comandos uteis
meu_app_api pyenv deactivate 
➜  meu_app_api pyenv activate myenv

```
(env)$ flask run --host 0.0.0.0 --port 5000
```

Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
automaticamente após uma mudança no código fonte. 

```
(env)$ flask run --host 0.0.0.0 --port 5000 --reload
```

Abra o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador para verificar o status da API em execução.



/* 
	MVP - PUCRS
*/

# MVP Overview

The purpose of this app is to allow the user to register medical appointments and view them on a map or in list format.  

I tried to reorganize the app.py by separating some responsibilities, I left only the definition of the routes, and I moved the functions to a separate file, the 'services' of each module.  

## About This Project

This is the first MVP of the Full Stack Development Postgraduate Program at PUCRS University, Rio de Janeiro.

**Student**: Leonardo Souza Paiva  
**Portfolio**: [www.leonardopaiva.com](http://www.leonardopaiva.com)  
**API URL pucrio-mvp-des-fs-basico-api**: [APP URL](https://github.com/leonardopaiva/pucrio-mvp-des-fs-basico-app)