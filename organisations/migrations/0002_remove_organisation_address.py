# Generated by Django 2.2 on 2019-04-30 15:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organisations', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organisation',
            name='address',
        ),
    ]
