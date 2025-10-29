from django.core.mail import send_mail
from django.conf import settings


class EmailService:
    @staticmethod
    def send_verification_email(email: str, code: str):
        subject = "[이게뭐약]에서 요청하신 인증 코드입니다."
        message = (
            f"안녕하세요. 가입을 위해 아래의 코드를 사이트에서 입력해주세요.\n\n"
            f"인증 코드: {code}\n"
            f"해당 코드는 발송 후 3분간 유효합니다."
        )
        send_mail(
            subject=subject,
            message=message,
            from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None),
            recipient_list=[email],
            fail_silently=False,
        )
