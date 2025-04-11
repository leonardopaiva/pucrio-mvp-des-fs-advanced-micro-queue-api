# Micro Queue API
 
---

# Overview
 
The purpose of this microservice is to manage operations related to the app's synchronization queue. Currently, it processes the queue, determines the route, and calls the micro appointments API to save the data with POST, PUT or DELETE.
 
## How to Run the MVP with all micro services
 
This project also comes with a Dockerfile, which provides an additional option for starting up. To better understand how to use it, please refer to the docker-compose.yml in the gateway api repository of this MVP.  
 
For the entire MVP to work, the microservices must be executed using a docker-compose.yml file. This microservice can be run individually, but it depends on the micro appointment API to operate.  
 
To learn how to run the full MVP, visit the gateway api repository at the provided link.

## Local and Env Variables

- When runing this micro service with docker using the docker-compose.yml from gateway api reposity the env variables will from there will be used.
 
## How to Run Only This Microservice
 
You must have all the Python libraries listed in requirements.txt installed.  
After cloning the repository, navigate to the root directory through the terminal to execute the commands below.
 
> It is strongly recommended to use virtual environments such as virtualenv (https://virtualenv.pypa.io/en/latest/installation.html).
 
```
(env)$ pip install -r 'requirements.txt'
```
 
This command installs the dependencies/libraries listed in the requirements.txt file.
 
To run the API, simply execute:
 
```
(env)$ flask run --host 0.0.0.0 --port 5000
````

or
 
```
(env)$ flask run --host 0.0.0.0 --port 5000 --reload
```

Open [http://localhost:5000/#/](http://localhost:5000/#/) in your browser to check the API status.
  

# Thanks to the MVP professors

Thanks to the MVP professors, Marisa Silva, Dieinison Braga and Carlos Rocha.

## About This Project
 
This is the third MVP of the Full Stack Development Postgraduate Program at PUCRS University, Rio de Janeiro.
 
**Student**: Leonardo Souza Paiva  
**Portfolio**: [www.leonardopaiva.com](http://www.leonardopaiva.com)
