# Fluid Flow Analysis System

Simple API for calculating flow parameters in pipes.

## Tech stack
- Python (FastAPI)
- Docker

## Features
- Calculates Reynolds number
- Calculates pressure loss (Darcy-Weisbach)
- REST API with JSON input/output

## Run with Docker

docker build -t flow-app .
docker run -p 8000:8000 flow-app

## API docs
After starting the container, open:
http://localhost:8000/docs