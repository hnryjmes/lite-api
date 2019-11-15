# Generated by Django 2.2.4 on 2019-09-18 10:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("parties", "0001_initial"),
        ("queries", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="EndUserAdvisoryQuery",
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
                ("note", models.TextField(blank=True, default=None, null=True)),
                ("reasoning", models.TextField(blank=True, default=None, null=True)),
                (
                    "copy_of",
                    models.ForeignKey(
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="end_user_advisories.EndUserAdvisoryQuery",
                    ),
                ),
                (
                    "end_user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="euae_query",
                        to="parties.EndUser",
                    ),
                ),
            ],
            bases=("queries.query",),
        ),
    ]
