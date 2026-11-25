import firebase_admin

from firebase_admin import auth
from firebase_admin import credentials

from app.core.config import settings


if not firebase_admin._apps:
    firebase_admin.initialize_app(
        credentials.Certificate(
            {
                "type": "service_account",
                "project_id": settings.FIREBASE_PROJECT_ID,
                "client_email": settings.FIREBASE_CLIENT_EMAIL,
                "private_key": settings.FIREBASE_PRIVATE_KEY.replace(
                    "\\n",
                    "\n",
                ),
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        )
    )


firebase_auth = auth