# Generated by Django 3.2.22 on 2023-11-01 12:08
import csv
import logging
from pathlib import Path
from django.conf import settings
from django.db import migrations

logger = logging.getLogger(__name__)


def read_updates_csv(filename):
    with open(filename, newline="") as csvfile:
        fieldnames = [
            "id",
            "report_summary",
            "suggested_prefix",
            "suggested_prefix_id",
            "suggested_subject",
            "suggested_subject_id",
        ]
        reader = csv.DictReader(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        next(reader, None)  # skip the headers
        yield from reader


class Migration(migrations.Migration):
    @classmethod
    def get_csv_path(cls):
        # Allow overriding the path to the CSV file for testing purposes
        # (migrations are challenging to patch with mocks)
        return (
            Path(settings.CONTENT_DATA_MIGRATION_DIR)
            / "applications"
            / "0077_back_populate_product_report_summary_prefix_and_suffix.csv"
        ).as_posix()

    def unpopulate_report_prefix_and_subject(apps, schema_editor):
        GoodOnApplication = apps.get_model("applications", "GoodOnApplication")
        for row in read_updates_csv(Migration.get_csv_path()):
            good_on_application_pk = row["id"]
            try:
                good_on_application = GoodOnApplication.objects.get(id=good_on_application_pk)
            except GoodOnApplication.DoesNotExist:
                logger.warning("GoodOnApplication with id %s does not exist", good_on_application_pk)
            else:
                good_on_application.report_summary_prefix_id = None
                good_on_application.report_summary_subject_id = None
                good_on_application.save()
                logger.info("GoodOnApplication with id %s reverted", good_on_application_pk)

    def populate_report_prefix_and_subject(apps, schema_editor):
        GoodOnApplication = apps.get_model("applications", "GoodOnApplication")
        for row in read_updates_csv(Migration.get_csv_path()):
            good_on_application_pk = row["id"]
            report_prefix_id = row["suggested_prefix_id"]
            report_subject_id = row["suggested_subject_id"]
            try:
                good_on_application = GoodOnApplication.objects.get(id=good_on_application_pk)
            except GoodOnApplication.DoesNotExist:
                logger.warning("GoodOnApplication with id %s does not exist", good_on_application_pk)
                continue

            if good_on_application.report_summary_prefix_id is not None:
                logger.warning(
                    "GoodOnApplication with id %s already has a report summary prefix, skipping...",
                    good_on_application_pk,
                )
                continue
            elif good_on_application.report_summary_subject_id is not None:
                logger.warning(
                    "GoodOnApplication with id %s already has a report summary subject, skipping...",
                    good_on_application_pk,
                )
                continue

            good_on_application.report_summary_prefix_id = report_prefix_id
            good_on_application.report_summary_subject_id = report_subject_id
            good_on_application.save()
            logger.info(
                "GoodOnApplication with id %s updated prefix=%s, subject=%s",
                good_on_application_pk,
                report_prefix_id,
                report_subject_id,
            )

    dependencies = [
        ("applications", "0076_back_populate_product_report_summary_prefix_and_suffix"),
    ]

    operations = [
        migrations.RunPython(populate_report_prefix_and_subject, unpopulate_report_prefix_and_subject),
    ]
