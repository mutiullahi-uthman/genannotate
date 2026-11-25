# GenAnnotate

GenAnnotate is a role-aware web application for managing annotation datasets and codebooks, assigning records, reviewing annotations, and tracking imports and exports. It consists of a Next.js frontend and a FastAPI backend, with PostgreSQL for application data, Redis/Celery for background jobs, Firebase Authentication, and Google Cloud Storage for files.

## Features

- Role-aware navigation and protected backend operations
- Dataset, annotation queue, and review workflows
- Codebook and user management
- Import and export job tracking with automatic progress refresh
- Dashboard charts, reusable data tables, loading states, and toast/error feedback
- Persistent dark mode

## Architecture

| Component | Location | Technology |
| --- | --- | --- |
| Web application | `frontend/` | Next.js 16, React, TypeScript |
| REST API | `backend/app/` | FastAPI, SQLAlchemy |
| Database and schema migrations | `backend/` | PostgreSQL, Alembic |
| Background jobs | `backend/app/tasks/` | Celery, Redis |
| Authentication | Frontend and backend | Firebase Authentication and Admin SDK |
| File storage | Backend | Google Cloud Storage |

The frontend is served at `http://localhost:3000`. The Compose setup exposes the API at `http://localhost:8001`; its interactive API documentation is at `http://localhost:8001/docs`.

## Requirements

- Docker Desktop with Docker Compose (recommended for the backend services)
- Node.js 20.9 or newer and npm
- Firebase project credentials for authentication
- A Google Cloud Storage bucket and Google Cloud credentials
- Google Cloud CLI for local Application Default Credentials

The backend Docker image uses Python 3.14. A local Python setup should use Python 3.14 to match it.

## Getting started with Docker

Run these commands from the repository root in PowerShell:

1. Create local environment files from the committed templates:

   ```powershell
   Copy-Item backend\.env.example backend\.env
   Copy-Item frontend\.env.example frontend\.env
   ```

2. Set `GCS_BUCKET_NAME=genannotate` in `backend\.env` (or use your bucket's exact name). Configure Google Cloud credentials with Application Default Credentials:

   ```powershell
   gcloud auth application-default login
   ```

   The Compose API and worker mount the Windows ADC file (`%APPDATA%\gcloud\application_default_credentials.json`) read-only. When running the backend directly, the Google Cloud client uses ADC from the current user's environment. In deployed environments, prefer a workload identity or attached service account with access to the bucket rather than a downloaded service-account key.

3. Edit both `.env` files and replace the example Firebase web app/Admin SDK values. Firebase sign-in also requires the appropriate sign-in provider to be enabled and `localhost` to be authorized in Firebase.

   `FIREBASE_PRIVATE_KEY` in `backend\.env` should use escaped `\n` sequences between key lines. Do not commit either `.env` file or put real credentials in the example files.

   Keep the bucket private; the backend accesses objects through Google Cloud credentials. The upload API returns the object's canonical URL, which is not anonymously accessible unless you explicitly configure public access.

4. Start the backend, database, migrations, Redis, and Celery worker:

   ```powershell
   docker compose -f backend\docker-compose.yml up --build
   ```

   Compose runs `alembic upgrade head` before starting the API and worker. The API is available at `http://localhost:8001`.

5. In a separate terminal, install frontend dependencies and start Next.js:

   ```powershell
   Set-Location frontend
   npm ci
   npm run dev
   ```

   Open `http://localhost:3000`.

Stop the Compose services with `docker compose -f backend\docker-compose.yml down`. The named PostgreSQL volume is retained. To also remove the local database data, use `docker compose -f backend\docker-compose.yml down -v`.

The Compose file's default PostgreSQL username and password are for local development only. Set `POSTGRES_USER`, `POSTGRES_PASSWORD`, and `POSTGRES_DB` appropriately before using this setup in a shared or production environment.

## Local backend development

You can run PostgreSQL and Redis through Compose while running the API directly. From the repository root:

```powershell
docker compose -f backend\docker-compose.yml up -d postgres redis
Set-Location backend
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

Ensure `backend\.env` contains valid credentials and local connection URLs (`localhost` for PostgreSQL and Redis). In a second terminal, start the worker from `backend\` with the same virtual environment:

```powershell
celery -A app.tasks.celery_app worker --loglevel=info
```

For frontend development, create `frontend\.env` from its example, then run `npm ci` and `npm run dev` from `frontend\`.

## Environment variables

The complete variable lists and placeholder values are in [`backend/.env.example`](backend/.env.example) and [`frontend/.env.example`](frontend/.env.example).

### Backend

| Variable | Purpose |
| --- | --- |
| `DATABASE_URL` | SQLAlchemy database connection |
| `REDIS_URL` | Redis connection |
| `CELERY_BROKER_URL` | Celery task broker |
| `CELERY_RESULT_BACKEND` | Celery result storage |
| `FIREBASE_PROJECT_ID` | Firebase project identifier |
| `FIREBASE_CLIENT_EMAIL` | Firebase Admin service-account email |
| `FIREBASE_PRIVATE_KEY` | Firebase Admin service-account private key |
| `GCS_BUCKET_NAME` | Google Cloud Storage bucket used for uploaded files |
| `FRONTEND_ORIGINS` | JSON array of allowed frontend origins for browser API requests |

### Frontend

| Variable | Purpose |
| --- | --- |
| `NEXT_PUBLIC_API_URL` | Backend API base URL |
| `NEXT_PUBLIC_FIREBASE_API_KEY` | Firebase web-app API key |
| `NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN` | Firebase Authentication domain |
| `NEXT_PUBLIC_FIREBASE_PROJECT_ID` | Firebase project identifier |
| `NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET` | Firebase Storage bucket |
| `NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID` | Firebase messaging sender ID |
| `NEXT_PUBLIC_FIREBASE_APP_ID` | Firebase web-app ID |

`NEXT_PUBLIC_*` values are included in the browser bundle; do not put server credentials in them. Keep Firebase Admin credentials private. The repository ignore rules exclude local environment files and credential artifacts while allowing the `.env.example` templates to be tracked.

## Application routes

| Route | Purpose |
| --- | --- |
| `/login` | Sign in |
| `/dashboard` | Work overview and charts |
| `/datasets` | Browse and manage datasets |
| `/queue` | Annotation queue |
| `/review` | Review workflow |
| `/reports` | Reports |
| `/exports` | Export jobs and history |
| `/codebooks` | Codebook management |
| `/users` | User and role management |

Some navigation items and operations are limited by the signed-in user's role. New Firebase users are provisioned as annotators by default; administrators manage user roles and status through the user-management workflow. Backend permission checks remain authoritative.

| Role | Main capabilities |
| --- | --- |
| Admin | All backend permissions, including user management |
| Supervisor | Assign records, approve reviews, manage codebooks, create datasets, and generate exports |
| Research lead | Manage codebooks, create datasets, and generate exports |
| Annotator | Annotation workflow without management permissions |

## Imports and background jobs

Dataset uploads accept CSV, XLSX, and JSON. Required fields, aliases, and validation rules are documented in [`backend/IMPORT_FORMAT.md`](backend/IMPORT_FORMAT.md). Import and export jobs run through Celery; keep the worker running for jobs to complete. Active job progress is refreshed by polling the API every two seconds.

The import workflow uses a `QUEUED` job state. Apply the Alembic migrations before using this workflow; the Docker Compose startup does this automatically.

## Checks and tests

From `frontend\`:

```powershell
npm run lint
npm run build
```

From `backend\`, with backend dependencies installed:

```powershell
python -m unittest discover -s tests -v
```

The backend tests use Python's `unittest` runner.

## Repository layout

```text
backend/
  app/                 FastAPI application, APIs, models, and Celery tasks
  migrations/          Alembic migrations
  tests/               Backend tests
  docker-compose.yml   Local PostgreSQL, Redis, migration, API, and worker services
frontend/
  src/app/             Next.js routes
  src/components/      Shared UI and application shell
  src/lib/             API, authentication, and client utilities
```
