# Smart Healthcare Management System (SHMS)

An enterprise-grade, production-ready Hospital Information Management System (HIMS) and Clinical Decision Support System. Developed as an isolated, standalone modular application.

---

## 🏥 Architecture & Tech Stack

```
   ┌──────────────────────────────────────────────────────────┐
   │                    React 19 Frontend                     │
   └─────────────┬──────────────────────────────┬─────────────┘
                 │ (REST API)                   │ (REST API)
                 ▼                              ▼
   ┌───────────────────────────┐  ┌───────────────────────────┐
   │   Spring Boot 3 Backend   │  │   Python FastAPI AI Hub   │
   └─────────────┬─────────────┘  └─────────────┬─────────────┘
                 │ (JPA/JDBC)                   │ (Local OCR / ML)
                 ▼                              ▼
   ┌──────────────────────────────────────────────────────────┐
   │            MySQL 8 Database / Fallback SQLite            │
   └──────────────────────────────────────────────────────────┘
```

- **Frontend**: React 19, TypeScript, Vite, Tailwind CSS, shadcn/ui, Google Material Icons.
- **Backend Service**: Java 21, Spring Boot 3, Spring JPA, Hibernate, Spring Security.
- **AI Microservices**: Python FastAPI, Symptom Checker, Disease Risk Predictor, OCR Report Summarizer.
- **Data Persistence**: MySQL 8 (Primary) with automated transparent fallback to SQLite (`healthcare.db`).

---

## 📂 Directory Structure

```
SmartHealthcare/
├── Dockerfile                  # Streamlit HIMS dashboard Docker config
├── docker-compose.yml          # Multi-container orchestration config
├── database.sql                # SQL schema initialization (28 tables)
├── db.py                       # MySQL + SQLite transparent fallback connector
├── auth.py                     # BCrypt authentication and audit logger
├── app.py                      # Interactive Streamlit clinical interface
├── requirements.txt            # Streamlit dashboard Python requirements
├── ai-fastapi/                 # Python FastAPI AI microservice
│   ├── Dockerfile
│   ├── main.py                 # Disease risk, symptom checker, OCR routes
│   └── requirements.txt
├── backend-spring/             # Java Spring Boot 3 backend module
│   ├── src/main/java/          # JPA entity mappings & Application entry
│   ├── src/main/resources/     # Datasource application.properties
│   └── pom.xml                 # Maven build dependencies
├── frontend-react/             # React 19 Vite web app workspace
│   ├── src/                    # App.tsx dashboard and CSS styles
│   └── package.json
└── tests/                      # Unit testing suite
    └── test_healthcare.py      # Database and pathway validation tests
```

---

## ⚙️ Setup & Running Instructions

### Prerequisites
- Node.js v20+ & npm
- Python 3.10+
- Java 21 & Maven 3.9+
- Docker & Docker Compose (Optional)

### Option 1: Standalone Running (Local CLI)

1. **Run Unit Tests**:
   ```bash
   py -m unittest discover -s tests -p "test_*.py"
   ```

2. **Start FastAPI AI Microservice**:
   ```bash
   py -m uvicorn ai-fastapi.main:app --host 127.0.0.1 --port 8000 --reload
   ```

3. **Start Streamlit Dashboard**:
   ```bash
   py -m streamlit run app.py
   ```

4. **Start React Frontend**:
   ```bash
   cd frontend-react
   npm run dev
   ```

### Option 2: Orchestrated Running (Docker)
Build and spin up MySQL, FastAPI, and the dashboard concurrently:
```bash
docker-compose up --build
```

---

## 🔑 Default Credentials
- **System Administrator**: `ADMIN` / `ADMIN`
- **Clinical Admin**: `Sindiri` / `Aryan@AS_1622`
- **General Doctor**: `Aryan` / `ADMIN`
