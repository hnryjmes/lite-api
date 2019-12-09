# Generated by Django 2.2.4 on 2019-12-05 16:06

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("documents", "0001_initial"),
        ("countries", "0001_initial"),
        ("organisations", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Party",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("name", models.TextField(blank=True, default=None)),
                ("address", models.TextField(blank=True, default=None)),
                ("website", models.URLField(blank=True, default=None)),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("consignee", "Consignee"),
                            ("end_user", "End User"),
                            ("ultimate_end_user", "Ultimate End User"),
                            ("third_party", "Third Party"),
                        ],
                        max_length=20,
                    ),
                ),
                ("country", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="countries.Country")),
                (
                    "organisation",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="organisation_party",
                        to="organisations.Organisation",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Consignee",
            fields=[
                (
                    "party_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="parties.Party",
                    ),
                ),
                (
                    "sub_type",
                    models.CharField(
                        choices=[
                            ("government", "Government"),
                            ("commercial", "Commercial Organisation"),
                            ("individual", "Individual"),
                            ("other", "Other"),
                        ],
                        default="other",
                        max_length=20,
                    ),
                ),
            ],
            bases=("parties.party",),
        ),
        migrations.CreateModel(
            name="EndUser",
            fields=[
                (
                    "party_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="parties.Party",
                    ),
                ),
                (
                    "sub_type",
                    models.CharField(
                        choices=[
                            ("government", "Government"),
                            ("commercial", "Commercial Organisation"),
                            ("individual", "Individual"),
                            ("other", "Other"),
                        ],
                        default="other",
                        max_length=20,
                    ),
                ),
            ],
            bases=("parties.party",),
        ),
        migrations.CreateModel(
            name="ThirdParty",
            fields=[
                (
                    "party_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="parties.Party",
                    ),
                ),
                (
                    "sub_type",
                    models.CharField(
                        choices=[
                            ("intermediate_consignee", "Intermediate Consignee"),
                            ("additional_end_user", "Additional End User"),
                            ("agent", "Agent"),
                            ("submitter", "Authorised Submitter"),
                            ("consultant", "Consultant"),
                            ("contact", "Contact"),
                            ("exporter", "Exporter"),
                            ("other", "Other"),
                        ],
                        default="other",
                        max_length=22,
                    ),
                ),
            ],
            bases=("parties.party",),
        ),
        migrations.CreateModel(
            name="UltimateEndUser",
            fields=[
                (
                    "party_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="parties.Party",
                    ),
                ),
                (
                    "sub_type",
                    models.CharField(
                        choices=[
                            ("government", "Government"),
                            ("commercial", "Commercial Organisation"),
                            ("individual", "Individual"),
                            ("other", "Other"),
                        ],
                        default="other",
                        max_length=20,
                    ),
                ),
            ],
            bases=("parties.party",),
        ),
        migrations.CreateModel(
            name="PartyDocument",
            fields=[
                (
                    "document_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="documents.Document",
                    ),
                ),
                ("party", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="parties.Party")),
            ],
            bases=("documents.document",),
        ),
    ]
