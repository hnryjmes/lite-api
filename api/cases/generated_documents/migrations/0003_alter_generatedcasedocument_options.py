# Generated by Django 3.2.19 on 2023-09-11 14:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("generated_documents", "0002_alter_generatedcasedocument_advice_type"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="generatedcasedocument",
            options={"ordering": ["created_at"]},
        ),
    ]
