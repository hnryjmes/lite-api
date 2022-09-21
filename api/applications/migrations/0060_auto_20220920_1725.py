# Generated by Django 3.2.15 on 2022-09-20 16:25

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("applications", "0059_alter_goodonapplication_unit"),
    ]

    operations = [
        migrations.AddField(
            model_name="standardapplication",
            name="f1686_approval_date",
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name="standardapplication",
            name="f1686_contracting_authority",
            field=models.CharField(blank=True, default=None, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="standardapplication",
            name="f1686_reference_number",
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="standardapplication",
            name="f680_reference_number",
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="standardapplication",
            name="is_f1686_approval_document_available",
            field=models.BooleanField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="standardapplication",
            name="other_security_approval_details",
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="standardapplication",
            name="security_approvals",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(
                    choices=[("F680", "F680"), ("F1686", "F1686"), ("Other", "Other")], max_length=255
                ),
                blank=True,
                null=True,
                size=None,
            ),
        ),
    ]
