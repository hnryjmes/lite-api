# Generated by Django 2.2.4 on 2019-09-14 14:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('queries', '0001_initial'),
        ('cases', '0004_auto_20190912_1553'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='clc_query',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='ecju_query',
        ),
        migrations.AddField(
            model_name='notification',
            name='query',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='queries.Query'),
        ),
    ]
