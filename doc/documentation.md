# p2rest - Documentation
## Table of Contents
1. [Introduction](#introduction)
2. [Configuration](#configuration)
3. [Endpoints](#endpoints)
4. [Swagger documentation](#swagger-documentation)

## Introduction
Here you may find relevant information on how to install and use this application

## Docker Build
In order to create a docker container from sources the following command can be used. The proxy build args can be
omitted if you are NOT behind a corporate proxy. (You need to e in the root folder of the project where the 
dockerfile is located)
```
docker build . --build-arg http_proxy=http://<proxyuser>:<proxypass>@<proxyhost>:<proxyport> --build-arg https_proxy=http://<proxyuser>:<proxypass>@<proxyhost>:<proxyport> -t p2rest:latest
```


## Run it
In order to run the application you have the possibility to start the docker container or for testing purposes
you can start a local instance

### Running Docker 
When you have build the container yourselve then you can use the following command
```
docker run p2rest:latest -p:8080:8080
```

### Running locally
If you want to test the application locally you can start it directly via python. 
First you need to install the requirements listed in the requirements.txt file (in the root folder). 
This can be either done in a global python instance or (which is prefered) in a venv. 

Once the requirements are installed you can start the application with:
```
python wsgi.py
```

## Configuration
ToDo

## Endpoints
ToDo

## Swagger documentation
ToDo