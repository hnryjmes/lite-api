# Generated by Django 2.2.4 on 2019-10-01 16:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('control_list_classifications', '0003_auto_20190913_1536'),
        ('goods', '0002_auto_20191001_1603'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='controllistclassificationquery',
            name='comment',
        ),
        migrations.RemoveField(
            model_name='controllistclassificationquery',
            name='report_summary',
        ),
    ]
