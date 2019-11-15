# Generated by Django 2.2.4 on 2019-09-05 14:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("organisations", "0001_initial"),
        ("statuses", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Query",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("submitted_at", models.DateTimeField(auto_now_add=True)),
                (
                    "organisation",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="organisations.Organisation",
                    ),
                ),
                (
                    "status",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="query_status",
                        to="statuses.CaseStatus",
                    ),
                ),
            ],
            options={"ordering": ["-submitted_at"],},
        ),
    ]
