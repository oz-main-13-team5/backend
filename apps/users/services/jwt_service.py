import jwt
from datetime import datetime, timedelta
from django.conf import settings

class JWTService:
    @staticmethod
    def generate_access_token(user_id):
        return jwt.encode({
            "user_id": str(user_id),
            "exp": datetime.utcnow() + timedelta(hours=1)
        }, settings.SECRET_KEY, algorithm="HS256")
