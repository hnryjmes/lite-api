import pytest
from django_test_migrations.migrator import Migrator
from django_test_migrations.contrib.unittest_case import MigratorTestCase


@pytest.mark.django_db()
class TestAddCaseSubStatusDraftRejectionLetter(MigratorTestCase):

    migrate_from = ("statuses", "0008_update_ogd_advice_name")
    migrate_to = ("statuses", "0009_add_draft_rejection_sub_status")

    def test_migration_0009_add_draft_rejection_sub_status(self):
        CaseSubStatus = self.new_state.apps.get_model("statuses", "CaseSubStatus")

        draft_rejection_sub_status = CaseSubStatus.objects.get(id="00000000-0000-0000-0000-000000000012")


        assert draft_rejection_sub_status.name == "Draft rejection letter"
