# Generated by Django 3.2.20 on 2023-07-27 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0057_auto_20230505_1209'),
    ]

    operations = [
        migrations.AddField(
            model_name='advice',
            name='is_refusal_note',
            field=models.BooleanField(default=False),
        ),
    ]
