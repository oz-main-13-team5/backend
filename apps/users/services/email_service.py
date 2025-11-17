from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string


class EmailService:
    @staticmethod
    def send_verification_email(email: str, code: str):
        subject = "[이게뭐약]에서 요청하신 인증 코드입니다."
        context = {
            "site_name": "이게뭐약",
            "code": code,
        }

        # HTML 템플릿 렌더링
        html_message = render_to_string("email/verification_email.html", context)

        msg = EmailMultiAlternatives(
            subject=subject,
            from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None),
            to=[email],
        )
        msg.attach_alternative(html_message, "text/html")
        msg.send()
