# Generated by Django 2.2.4 on 2019-09-05 10:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('queues', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='queue',
            options={'ordering': ['name']},
        ),
    ]
