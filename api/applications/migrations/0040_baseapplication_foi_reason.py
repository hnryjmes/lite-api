# Generated by Django 2.2.17 on 2020-11-20 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("applications", "0039_auto_20201104_1047"),
    ]

    operations = [
        migrations.AddField(
            model_name="baseapplication", name="foi_reason", field=models.TextField(blank=True, null=True),
        ),
    ]
