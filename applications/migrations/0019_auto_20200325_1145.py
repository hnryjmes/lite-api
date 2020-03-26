# Generated by Django 2.2.11 on 2020-03-25 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("applications", "0018_auto_20200324_0952"),
    ]

    operations = [
        migrations.AddField(
            model_name="openapplication",
            name="is_shipped_waybill_or_lading",
            field=models.BooleanField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="openapplication",
            name="non_waybill_or_lading_route_details",
            field=models.TextField(blank=True, default=None, max_length=2000, null=True),
        ),
        migrations.AddField(
            model_name="standardapplication",
            name="is_shipped_waybill_or_lading",
            field=models.BooleanField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="standardapplication",
            name="non_waybill_or_lading_route_details",
            field=models.TextField(blank=True, default=None, max_length=2000, null=True),
        ),
    ]
