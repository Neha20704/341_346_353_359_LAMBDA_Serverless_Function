#  Lambda - Serverless Function Platform | Setup & Log

## Team Members
- 341 - Meghana 
- 346 - Neha
- 353 - Nida
- 359 - Nikhita

---

##  Environment Setup

### OS & Virtualization
- OS: Windows 11 with WSL 2 (Ubuntu)
- Virtualization: Docker (with Docker Desktop disabled)
- Used `docker` service directly from WSL
- Enabled **gVisor** as second runtime via `runsc`

### Docker & gVisor Verification
```bash
$ docker info | grep runsc
Runtimes: io.containerd.runc.v2 runc runsc
```

```bash
$ docker run --rm --runtime=runsc hello-world
Docker with gVisor works!
```

---

## Project Structure

```
lambda_serverless/
│
├── backend/                ← FastAPI + SQLAlchemy
│   └── app/
│       ├── main.py
│       ├── models.py
│       ├── schemas.py
│       ├── crud.py
│       └── database.py
│
├── executor/               ← runner.py execution engine
│   └── runner.py
│
├── docker/
│   ├── base_images/
│   │   ├── python/Dockerfile + handler.py
│   │   └── javascript/Dockerfile + handler.js
│   └── functions/
│       ├── python/hello.py, arithmetic.py, infinite.py
│       └── javascript/hello.js, arithmetic.js
│
├── frontend/               ← Streamlit UI
│   └── app.py
│
└── README.md + setup_log.md
```

---

## Initial Setup

```bash
# Clone Repo
git clone https://github.com/your-team/lambda-serverless.git
cd lambda-serverless

# Create virtual environments
python3 -m venv venv
source venv/bin/activate

# Install FastAPI deps
cd backend
pip install -r requirements.txt

# Set up MySQL
sudo service mysql start
# (Configured in database.py with user/pass/db)

# Docker base images
cd docker/base_images/python
docker build -t lambda-python .

cd ../javascript
docker build -t lambda-javascript .
```

---

## Testing Locally

```bash
# Start backend API
cd backend/app
uvicorn main:app --reload

# Run executor test
cd executor
python3 run_tests.py

# Start Streamlit frontend
cd frontend
streamlit run app.py
```

---

## gVisor Runtime Test

```bash
# Run with default Docker (runc)
docker run --rm --runtime=runc -v "$PWD/docker/functions:/functions" \
  -e FUNCTION_FILE=python/hello.py lambda-python

# Run with gVisor (runsc)
docker run --rm --runtime=runsc -v "$PWD/docker/functions:/functions" \
  -e FUNCTION_FILE=python/hello.py lambda-python
```

---

## Database Tables

### `functions`
| id | name     | language | route         | timeout |
|----|----------|----------|---------------|---------|
| 1  | hello    | python   | hello.py      | 5       |

### `metrics`
| id | function_id | timestamp           | exec_time | error | msg     |
|----|-------------|---------------------|-----------|-------|---------|
| 1  | 1           | 2025-04-20 13:02:58 | 0.421     | false | NULL    |

---

## Final Checklist

- [x] Backend working (CRUD, Execution)
- [x] Frontend: Create, List, Execute, Delete, Update
- [x] Execution engine with gVisor toggle
- [x] Metrics collection + dashboard
- [x] Authentication added to metrics
- [x] End-to-end testing done
- [x] Documentation complete

---
