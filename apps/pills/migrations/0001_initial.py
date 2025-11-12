from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="PillItem",
            fields=[
                (
                    "item_seq",
                    models.CharField(max_length=20, primary_key=True, serialize=False),
                ),
                ("entp_name", models.TextField()),
                ("item_name", models.TextField()),
                ("efcy_qesitm", models.TextField()),
                ("use_method_qesitm", models.TextField()),
                ("atpn_warn_qesitm", models.TextField()),
                ("intrc_qesitm", models.TextField()),
                ("se_qesitm", models.TextField()),
                ("deposit_method_qesitm", models.TextField()),
                ("item_image_url", models.TextField()),
            ],
        ),
    ]
