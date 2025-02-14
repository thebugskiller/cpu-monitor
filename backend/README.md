# 🚀 FastAPI CPU Usage Tracker API

This project is a FastAPI-based API that allows user authentication and tracks CPU usage for specific test runs. It uses MongoDB for data storage and Docker for deployment.

---

## 📜 **Table of Contents**
1. [Features](#-features)
2. [Tech Stack](#-tech-stack)
3. [Installation](#️-installation)
4. [Environment Variables](#-environment-variables)
5. [API Endpoints](#-api-endpoints)
6. [Future Enhancement Work](#-future-enhancement-work)

---

## 🚀 **Features**
- User authentication with username and password (cookie-based session).
- Create and manage test runs.
- Write CPU usage data linked to specific test runs.
- Read CPU usage data for a given test run.

---

## 🛠️ **Tech Stack**
- **Backend:** FastAPI (Python)
- **Database:** MongoDB
- **ORM:** Beanie
- **Schema Builder:** Pydantic
- **Containerization:** Docker

---

## ⚙️ **Installation**

1. **Clone the repository:**
```bash
git clone https://github.com/thebugskiller/cpu-monitor.git
cd cpu-monitor
cd backend
```

2. **Setup environment variables:**
Create a `.env` file in the root directory:
Add required environment variables mentioned in `.env.example` file


### *Manual Installation*

1. **Create a virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up MongoDB:**  
Ensure MongoDB is running locally or provide an Atlas connection string.

4. **Start Fast API server:**
```bash
fastapi dev main.py
```

---

### *Docker Setup*

1. **Build Docker image:**
```bash
docker-compose up --build
```

2. **Check logs:**
```bash
docker logs container_id
```

---

## 🚦 **API Endpoints**

### Swagger UI documentation
http://localhost:8000/docs

### 🔐 Authentication
1. **User Registration:** `POST /auth/register`
2. **User Login:** `POST /auth/login`
3. **User Logout:** `POST /auth/logout`
4. **User Profile:** `GET /auth/profile` [protected]


---

### 📊 Test Runs & CPU Usage
1. **Create Test Run:** `POST /monitor/testruns` [protected]
2. **Write CPU Usage:** `POST /monitor/cpu-usage/{testrun_id}` [protected]
3. **Read CPU Usage:** `GET /monitor/cpu-usage/{testrun_id}` [protected]

---

## 🚀 **Future Enhancement Work**
- **Rate Limiting:** Prevent abuse by limiting the number of API requests per user.
- **Indexing:** Add indexes to frequently queried fields like username, test_run_id, and timestamp for faster lookups.
- **Pagination:** Implement pagination for test runs and CPU usage endpoints to avoid large responses.
- **Caching:** Use Redis or Memory Cache for frequently accessed data (e.g., user sessions).
- **Kubernetes:** If deploying at scale, use Kubernetes for orchestration.
- **CI/CD:** Set up GitHub Actions or GitLab CI/CD for automated testing and deployment.


 
 
 
 
 
 