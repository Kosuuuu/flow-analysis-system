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

```bash
docker build -t flow-app .
docker run -p 8000:8000 flow-app
```
## Example request

Use `/docs` in Swagger UI and send JSON like:

```json
{
  "length_m": 10,
  "diameter_m": 0.05,
  "flow_rate_m3s": 0.002,
  "density_kgm3": 997,
  "viscosity_pas": 0.001,
  "friction_factor_mode": "auto",
  "manual_friction_factor": 0.02
}
```

## API docs
After starting the container, open:
`http://localhost:8000/docs`
