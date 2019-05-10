# Generated by Django 2.2 on 2019-05-03 11:46

from django.db import migrations
import enumchoicefield.fields
import quantity.units


class Migration(migrations.Migration):

    dependencies = [
        ('drafts', '0004_remove_goodondraft_end_use_case'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goodondraft',
            name='unit',
            field=enumchoicefield.fields.EnumChoiceField(default=quantity.units.Units(3), enum_class=quantity.units.Units, max_length=3),
        ),
    ]
