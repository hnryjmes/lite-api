# Generated by Django 2.2.4 on 2019-10-31 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0006_auto_20191031_1333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baseapplication',
            name='last_modified_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
