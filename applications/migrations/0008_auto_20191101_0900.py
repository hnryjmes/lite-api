# Generated by Django 2.2.4 on 2019-11-01 09:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0007_auto_20191031_1542'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='baseapplication',
            options={'ordering': ['-created_at']},
        ),
    ]
