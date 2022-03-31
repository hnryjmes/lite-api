# Generated by Django 3.2.12 on 2022-03-25 10:28

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("goods", "0008_remove_firearmgooddetails_has_identification_markings"),
    ]

    operations = [
        migrations.AddField(
            model_name="firearmgooddetails",
            name="category",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(
                    choices=[
                        ("NON_AUTOMATIC_SHOTGUN", "Non automatic shotgun"),
                        ("NON_AUTOMATIC_RIM_FIRED_RIFLE", "Non automatic rim-fired rifle"),
                        ("NON_AUTOMATIC_RIM_FIRED_HANDGUN", "Non automatic rim-fired handgun"),
                        ("RIFLE_MADE_BEFORE_1938", "Rifle made before 1938"),
                        ("COMBINATION_GUN_MADE_BEFORE_1938", "Combination gun made before 1938"),
                        ("NONE", "None of the above"),
                    ],
                    max_length=255,
                ),
                blank=True,
                null=True,
                size=None,
            ),
        ),
    ]
