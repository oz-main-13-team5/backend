from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class PillItem(models.Model):
    item_seq = models.CharField(max_length=20, primary_key=True)  # 품목기준코드
    entp_name = models.TextField()  # 업체명
    item_name = models.TextField()  # 제품명
    efcy_qesitm = models.TextField()  # 효능
    use_method_qesitm = models.TextField()
    atpn_warn_qesitm = models.TextField()
    intrc_qesitm = models.TextField()
    se_qesitm = models.TextField()
    deposit_method_qesitm = models.TextField()
    item_image_url = models.TextField()

    def __str__(self):
        return f"{self.item_name}({self.item_seq})"
