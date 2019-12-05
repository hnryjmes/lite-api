# Generated by Django 2.2.4 on 2019-12-03 09:10

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Document",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=1000)),
                ("s3_key", models.CharField(default=None, max_length=1000)),
                ("size", models.IntegerField(blank=True, null=True)),
                ("virus_scanned_at", models.DateTimeField(blank=True, null=True)),
                ("safe", models.NullBooleanField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
