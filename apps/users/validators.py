import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class CustomPasswordValidator:
    def validate(self, password, user=None):
        if not re.search(r"[A-Za-z]", password):
            raise ValidationError(
                _("비밀번호에 최소 한 개의 영문자가 포함되어야 합니다.")
            )
        if not re.search(r"\d", password):
            raise ValidationError(
                _("비밀번호에 최소 한 개의 숫자가 포함되어야 합니다.")
            )
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise ValidationError(
                _("비밀번호에 최소 한 개의 특수문자가 포함되어야 합니다.")
            )

    def get_help_text(self):
        return _("비밀번호는 영문자, 숫자, 특수문자를 최소 하나씩 포함해야 합니다.")
