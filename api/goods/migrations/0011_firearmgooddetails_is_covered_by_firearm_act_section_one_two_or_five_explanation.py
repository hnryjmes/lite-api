# Generated by Django 3.2.12 on 2022-04-01 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("goods", "0010_auto_20220328_1348"),
    ]

    operations = [
        migrations.AddField(
            model_name="firearmgooddetails",
            name="is_covered_by_firearm_act_section_one_two_or_five_explanation",
            field=models.TextField(blank=True, default=""),
        ),
    ]
