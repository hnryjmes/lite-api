# Generated by Django 2.2.12 on 2020-05-19 15:41

from django.db import migrations, models
import django.db.models.deletion


def forward_migration(apps, schema_editor):
    ControlListEntry = apps.get_model("control_list_entries", "ControlListEntry")
    ControlListEntry.objects.filter(is_decontrolled=True).delete()


def reverse_migration(apps, schema_editor):
    # To fully reverse migrate the code above you would need to allow decontrolled to be seedable again,
    # and rerun seeding.
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("control_list_entries", "0003_auto_20200519_1048"),
    ]

    operations = [
        migrations.RunPython(forward_migration, reverse_migration),
    ]
