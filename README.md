#LAMBDA - Serverless Function Platform  
**UE22CS351B: Cloud Computing Project**  
Team: SRNs 341, 346, 353, 359  

---

## Project Overview

A serverless platform similar to AWS Lambda that allows users to:

- Deploy and execute Python or JavaScript functions on-demand
- Choose between Docker and gVisor virtualization runtimes
- Monitor execution metrics like response time, error count, etc.
- Interact via a clean Streamlit-based UI

---

## System Architecture

- **Frontend**: Streamlit app for function deployment, management & dashboard
- **Backend**: FastAPI server with CRUD APIs + execution endpoint
- **Executor**: Docker-based runner to securely run user functions
- **Database**: MySQL (via SQLAlchemy) for storing function metadata and metrics
- **Virtualization**: Docker and gVisor support, configurable per execution

```
 Project Structure:
🔹 backend/
🔹 ├── app/
🔹 │   ├── main.py (FastAPI app)
🔹 │   ├── models.py, schemas.py, crud.py
🔹 │   └── database.py
🔹 docker/
🔹 ├── base_images/python, javascript/ (Dockerfiles + handlers)
🔹 └── functions/ (Uploaded user functions)
🔹 executor/
🔹 └── runner.py (Function runner using Docker CLI)
🔹 frontend/
🔹 └── app.py (Streamlit dashboard)
```

---

### Setup Instructions

> Tested on: WSL2 + Docker + Python 3.12 + MySQL

###  Install dependencies
```bash
cd backend && pip install -r requirements.txt
cd ../frontend && pip install -r requirements.txt
```

###  Set up MySQL
```sql
CREATE DATABASE lambda_functions;
```

Update `backend/app/database.py` with your credentials.

###  Build base Docker images
```bash
docker build -t lambda-python ./docker/base_images/python
docker build -t lambda-javascript ./docker/base_images/javascript
```

###  Test Docker + gVisor
```bash
docker run --rm --runtime=runsc hello-world
```

###  Run backend
```bash
cd backend/app
uvicorn app.main:app --reload
```

### Run frontend
```bash
cd frontend
streamlit run app.py
```

---

## Features

- Deploy Python/JS functions from the frontend
- Execute them with optional CLI-style args
- Select runtime (`use_gvisor: true/false`)
- Metrics collection for every run (time, error, etc.)
- Monitoring dashboard with bar & line charts
- Auth token required to access metrics dashboard

---

##  API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/functions` | GET / POST | List or create function metadata |
| `/functions/{id}` | DELETE / PUT | Delete or update a function |
| `/functions/execute` | POST | Execute a function with `id`, `args`, `use_gvisor` |
| `/metrics` | GET | Get all raw metrics (🔐 Auth required) |
| `/metrics/summary` | GET | Aggregated metrics summary (🔐 Auth required) |

---

##  Security

- Metrics APIs are protected using a **Bearer Token** (`secret123`)
- Streamlit dashboard requires token to view metrics

---

##  Sample End-to-End Test Log

| Step | Action | Result |
|------|--------|--------|
| ✅ | Create Python function (`hello.py`) | Success |
| ✅ | Execute with `args=["Alice"]` | Output: `Hello, Alice!` |
| ✅ | Execute with `use_gvisor: true` | Output successful |
| ✅ | Run timeout test (`infinite.py`) | Error: timeout triggered |
| ✅ | Dashboard access (wrong token) | Blocked |
| ✅ | Dashboard access (valid token) | Metrics shown |
| ✅ | View MySQL table | Metrics stored correctly |

---

##  Technologies Used

- **FastAPI** – REST API server
- **Docker** – Virtualized container execution
- **gVisor** – Sandbox runtime
- **MySQL** – Data storage
- **Streamlit** – Interactive frontend UI
- **SQLAlchemy** – ORM for DB interaction

---

##  Team Members

| Name | SRN |
|------|-----|
| Member 1 | PES2UG22CS341 |
| Member 2 | PES2UG22CS346 |
| Member 3 | PES2UG22CS353 |
| Member 4 | PES2UG22CS359 |

---

##  Status

> ✅ **Week 1**: Core infra + Docker function execution  
> ✅ **Week 2**: Routing, warm-up, gVisor support, metrics  
> ✅ **Week 3**: Frontend UI, dashboard, integration, auth  

> 📦 Fully working system with clean docs, token protection, visual monitoring, and two runtime options!
```

