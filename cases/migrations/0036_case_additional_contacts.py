# Generated by Django 2.2.13 on 2020-06-12 14:21

from django.db import migrations, models

from api.parties.enums import PartyType


def forward_migration(apps, schema_editor):
    Case = apps.get_model("cases", "Case")
    PartyOnApplication = apps.get_model("applications", "PartyOnApplication")

    parties_on_app = PartyOnApplication.objects.filter(party__type=PartyType.ADDITIONAL_CONTACT)

    for party_on_app in parties_on_app:
        case = Case.objects.get(id=party_on_app.application_id)
        case.additional_contacts.add(party_on_app.party)

    parties_on_app.delete()


def backwards_migration(apps, schema_editor):
    pass
    # I made this pass since we would lose data for backwards migrating this step regardless.


class Migration(migrations.Migration):

    dependencies = [
        ("parties", "0007_auto_20200317_1730"),
        ("cases", "0035_auto_20200611_1246"),
    ]

    operations = [
        migrations.AddField(
            model_name="case", name="additional_contacts", field=models.ManyToManyField(to="parties.Party"),
        ),
        migrations.RunPython(forward_migration),
    ]
