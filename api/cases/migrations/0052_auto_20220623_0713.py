# Generated by Django 3.1.8 on 2022-06-23 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cases", "0051_auto_20211028_1327"),
    ]

    operations = [
        migrations.AlterField(
            model_name="casenote",
            name="text",
            field=models.TextField(blank=True, default=None, null=True),
        ),
    ]
