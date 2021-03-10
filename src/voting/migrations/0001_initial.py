from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ("contenttypes", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Vote",
            fields=[
                (
                    "id",
                    models.AutoField(
                        primary_key=True,
                        auto_created=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("object_id", models.PositiveIntegerField()),
                ("vote", models.SmallIntegerField(choices=[(1, "+1"), (-1, "-1")])),
                (
                    "time_stamp",
                    models.DateTimeField(
                        editable=False, default=django.utils.timezone.now
                    ),
                ),
                (
                    "content_type",
                    models.ForeignKey(
                        to="contenttypes.ContentType", on_delete=models.CASCADE
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE
                    ),
                ),
            ],
            options={
                "db_table": "votes",
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name="vote",
            unique_together=set([("user", "content_type", "object_id")]),
        ),
    ]
