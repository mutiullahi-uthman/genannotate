# GenAnnotate frontend

The Next.js app is in `src/app` and runs at `http://localhost:3000`.

## Setup

Copy `backend/.env.example` to `backend/.env` and
`frontend/.env.example` to `frontend/.env`. Replace the placeholder Firebase
and Azure values before starting the services. Local `.env` files and private
key files are ignored by Git; do not commit real credentials.

- `NEXT_PUBLIC_API_URL` — FastAPI base URL (for local Docker Compose, `http://localhost:8001`)
- `NEXT_PUBLIC_FIREBASE_API_KEY`
- `NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN`
- `NEXT_PUBLIC_FIREBASE_PROJECT_ID`
- `NEXT_PUBLIC_FIREBASE_APP_ID`
- `NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET`
- `NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID`

Firebase Google sign-in creates a local annotator profile on first login. An administrator can then assign roles and change account status from **Users**. Administrative API routes enforce permissions on the backend; hiding navigation items is only a usability layer.

## Features

- The theme toggle follows the system preference until a user chooses light or dark mode; the choice is stored in local storage.
- API failures appear as Sonner toasts. App-level failures have retry boundaries.
- Import and export status tables poll every two seconds while jobs are active.
- Codebooks can be edited while in draft, published once they have labels, and archived. Published codebooks are immutable.
- Dashboard charts use the reports API and are available to administrators, supervisors, and research leads.

## Development

```bash
npm install
npm run dev
npm run lint
npm run build
```
