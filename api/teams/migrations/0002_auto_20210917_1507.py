# Generated by Django 3.1.12 on 2021-09-17 14:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0001_squashed_0003_auto_20210325_0812'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='is_department',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='team',
            name='parent',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='teams.team'),
        ),
    ]
