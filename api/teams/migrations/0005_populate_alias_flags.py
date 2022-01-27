# Generated by Django 3.2.11 on 2022-01-27 09:47

from django.db import migrations


def populate_alias(apps, schema_editor):
    flags = {
        '67b9a4a3-6f3d-4511-8a19-23ccff221a74': 'FCO',
        '58e77e47-42c8-499f-a58d-94f94541f8c6': 'LICENSING_UNIT',
        'b7640925-2577-4c24-8081-b85bd635b62a': 'MOD_ECJU',
        '2e5fab3c-4599-432e-9540-74ccfafb18ee': 'MOD_DI',
        '4c62ce4a-18f8-4ada-8d18-4b53a565250f': 'MOD_DSR',
        '809eba0f-f197-4f0f-949b-9af309a844fb': 'MOD_DSTL',
        'a06aec31-47d7-443b-860d-66ab0c6d7cfd': 'MOD_WECA',
    }
    Team = apps.get_model('teams', 'Team')
    for f in flags.keys():
        team = Team.objects.filter(id=f)
        if team.exists():
            team.update(alias=flags[f])


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0004_team_alias'),
    ]

    operations = [
        migrations.RunPython(populate_alias, migrations.RunPython.noop),
    ]
