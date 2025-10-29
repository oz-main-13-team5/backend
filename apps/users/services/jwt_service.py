import hashlib, datetime
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken as JWTRefreshToken
from apps.users.models.refresh_token import RefreshToken

class JWTService:

    @staticmethod
    def generate_token_pair(user):
        jwt_refresh = JWTRefreshToken.for_user(user)
        jwt_access = jwt_refresh.access_token

        refresh_str = str(jwt_refresh)
        hashed_refresh = hashlib.sha256(refresh_str.encode()).hexdigest()

        RefreshToken.objects.create(
            user=user,
            token_hash=hashed_refresh,
            expired_at=timezone.now() + datetime.timedelta(days=14),
        )

        return {
            "access": str(jwt_access),
            "refresh": refresh_str,
        }

    @staticmethod
    def blacklist_token(raw_refresh_token):
        hashed_refresh = hashlib.sha256(raw_refresh_token.encode()).hexdigest()
        try:
            token = RefreshToken.objects.get(token_hash=hashed_refresh)
            token.blacklist()
        except RefreshToken.DoesNotExist:
            pass
