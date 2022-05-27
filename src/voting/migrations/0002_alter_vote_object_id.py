from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("voting", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="vote",
            name="object_id",
            field=models.TextField(),
        ),
    ]
