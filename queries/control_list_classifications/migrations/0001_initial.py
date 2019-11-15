# Generated by Django 2.2.4 on 2019-09-10 12:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("queries", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ControlListClassificationQuery",
            fields=[
                (
                    "query_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="queries.Query",
                    ),
                ),
                ("details", models.TextField(blank=True, default=None, null=True)),
                ("comment", models.TextField(blank=True, default=None, null=True)),
                (
                    "report_summary",
                    models.TextField(blank=True, default=None, null=True),
                ),
            ],
            bases=("queries.query",),
        ),
    ]
