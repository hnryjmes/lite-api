from datetime import datetime

from django.urls import reverse
from freezegun import freeze_time
from rest_framework import status

from test_helpers.clients import DataTestClient
from api.goods.enums import GoodStatus
from api.goods.tests.factories import GoodFactory
from api.applications.models import GoodOnApplication
from api.staticdata.regimes.models import RegimeEntry
from api.staticdata.report_summaries.models import ReportSummarySubject, ReportSummaryPrefix
from api.staticdata.statuses.models import CaseStatus


class MakeAssessmentsViewTests(DataTestClient):
    def setUp(self):
        super().setUp()
        self.application = self.create_draft_standard_application(organisation=self.organisation)
        self.case = self.submit_application(self.application)
        self.good = GoodFactory(organisation=self.organisation)
        self.good_on_application = GoodOnApplication.objects.create(
            good=self.good, application=self.application, quantity=10, value=500
        )

    def test_empty_data_success(self):
        url = reverse("assessments:make_assessments", kwargs={"case_pk": self.case.id})
        data = []
        response = self.client.put(url, data, **self.gov_headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @freeze_time("2023-11-03 12:00:00")
    def test_valid_data_updates_records(self):
        url = reverse("assessments:make_assessments", kwargs={"case_pk": self.case.id})
        good_on_application = self.good_on_application
        regime_entry = RegimeEntry.objects.first().id
        report_summary_prefix = ReportSummaryPrefix.objects.first()
        report_summary_subject = ReportSummarySubject.objects.first()
        data = [
            {
                "id": self.good_on_application.id,
                "control_list_entries": ["ML1"],
                "regime_entries": [regime_entry],
                "report_summary_prefix": report_summary_prefix.id,
                "report_summary_subject": report_summary_subject.id,
                "is_good_controlled": True,
                "comment": "some comment",
                "report_summary": "some string we expect to be overwritten",
                "is_ncsc_military_information_security": True,
            }
        ]
        response = self.client.put(url, data, **self.gov_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        good_on_application.refresh_from_db()
        all_cles = [cle.rating for cle in good_on_application.control_list_entries.all()]
        assert all_cles == ["ML1"]
        all_regime_entries = [regime_entry.id for regime_entry in good_on_application.regime_entries.all()]
        assert all_regime_entries == [regime_entry]
        assert good_on_application.report_summary_prefix_id == report_summary_prefix.id
        assert good_on_application.report_summary_subject_id == report_summary_subject.id
        assert good_on_application.is_good_controlled == True
        assert good_on_application.comment == "some comment"
        assert good_on_application.is_ncsc_military_information_security == True
        assert good_on_application.report_summary == f"{report_summary_prefix.name} {report_summary_subject.name}"
        assert good_on_application.assessed_by == self.gov_user
        assert good_on_application.assessment_date.isoformat() == "2023-11-03T12:00:00+00:00"

        good = good_on_application.good
        assert good.status == GoodStatus.VERIFIED
        assert [cle.rating for cle in good.control_list_entries.all()] == ["ML1"]
        assert good_on_application.report_summary == f"{report_summary_prefix.name} {report_summary_subject.name}"
        assert good.report_summary_prefix_id == report_summary_prefix.id
        assert good.report_summary_subject_id == report_summary_subject.id

    def test_terminal_case_400(self):
        self.application.status = CaseStatus.objects.get(status="finalised")
        self.application.save()
        url = reverse("assessments:make_assessments", kwargs={"case_pk": self.case.id})
        data = [
            {
                "id": self.good_on_application.id,
                "control_list_entries": ["ML1"],
                "is_good_controlled": True,
                "comment": "some comment",
                "report_summary": "some legacy summary",
                "is_ncsc_military_information_security": True,
            }
        ]
        response = self.client.put(url, data, **self.gov_headers)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
