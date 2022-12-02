# Generated by Django 3.1.8 on 2021-06-30 14:45

from django.db import migrations, models


class Migration(migrations.Migration):
    def populate_control_list_entries(apps, schema_editor):
        ratings = (
            "1C35023",
            "1C35029",
            "1C3504",
            "1C35065",
            "1C35066",
            "1C35067",
            "1C35068",
            "1C35069",
            "1C35070",
            "1C35071",
            "1C35072",
            "1C35073",
            "1C35074",
            "1C35075",
            "1C35076",
            "1C35077",
            "1C35078",
            "1C35079",
            "1C35080",
            "1C35081",
            "1C35082",
            "1C35083",
            "1C35084",
            "1C35085",
            "1C35086",
            "1C35087",
            "1C35088",
            "1C35089",
        )
        ControlListEntry = apps.get_model("control_list_entries", "ControlListEntry")
        for rating in ratings:
            ControlListEntry.objects.create(
                rating=rating, text=rating, parent_id=None, category="End-Use", controlled=True
            )

    dependencies = [
        ("control_list_entries", "0003_controllistentry_new_entries_20221124"),
    ]

    operations = [
        migrations.RunPython(populate_control_list_entries, migrations.RunPython.noop),
    ]
