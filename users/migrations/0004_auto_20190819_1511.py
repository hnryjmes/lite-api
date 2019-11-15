# Generated by Django 2.2.4 on 2019-08-19 15:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("organisations", "0001_initial"),
        ("users", "0003_auto_20190724_1334"),
    ]

    operations = [
        migrations.RemoveField(model_name="baseuser", name="status",),
        migrations.RemoveField(model_name="exporteruser", name="organisation",),
        migrations.AddField(
            model_name="govuser",
            name="status",
            field=models.CharField(
                choices=[("Active", "Active"), ("Deactivated", "Deactivated")],
                default="Active",
                max_length=20,
            ),
        ),
        migrations.CreateModel(
            name="UserOrganisationRelationship",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("Active", "Active"), ("Deactivated", "Deactivated")],
                        default="Active",
                        max_length=20,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "organisation",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="organisations.Organisation",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="users.ExporterUser",
                    ),
                ),
            ],
        ),
    ]
