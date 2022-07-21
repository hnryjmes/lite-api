from unittest import mock

from faker import Faker
from rest_framework.test import APITestCase

from api.applications.models import BaseApplication
from api.cases.notify import (
    notify_exporter_ecju_query,
    notify_exporter_licence_issued,
    notify_exporter_licence_refused,
    notify_exporter_licence_refused,
)
from api.compliance.tests.factories import ComplianceSiteCaseFactory, ComplianceVisitCaseFactory
from api.licences.enums import LicenceStatus
from api.licences.tests.factories import LicenceFactory
from api.users.tests.factories import ExporterUserFactory
from api.staticdata.statuses.enums import CaseStatusEnum
from api.staticdata.statuses.libraries.get_case_status import get_case_status_by_status
from gov_notify.enums import TemplateType
from gov_notify.payloads import ExporterECJUQuery, ExporterLicenceIssued, ExporterLicenceRefused
from test_helpers.clients import DataTestClient


class NotifyTests(DataTestClient):
    def setUp(self):
        super().setUp()
        self.case = self.create_standard_application_case(self.organisation)
        self.licence = LicenceFactory(case=self.case)

    @mock.patch("api.cases.notify.send_email")
    def test_notify_licence_issued(self, mock_send_email):
        expected_payload = ExporterLicenceIssued(
            user_first_name=self.exporter_user.first_name,
            application_reference=self.licence.case.reference_code,
            exporter_frontend_url="https://exporter.lite.service.localhost.uktrade.digital/",
        )

        notify_exporter_licence_issued(self.licence)

        mock_send_email.assert_called_with(
            self.exporter_user.email,
            TemplateType.EXPORTER_LICENCE_ISSUED,
            expected_payload,
        )

    @mock.patch("api.cases.notify.send_email")
    def test_notify_licence_refused(self, mock_send_email):
        expected_payload = ExporterLicenceRefused(
            user_first_name=self.exporter_user.first_name,
            application_reference=self.case.reference_code,
            exporter_frontend_url="https://exporter.lite.service.localhost.uktrade.digital/",
        )

        notify_exporter_licence_refused(self.case)

        mock_send_email.assert_called_with(
            self.exporter_user.email,
            TemplateType.EXPORTER_LICENCE_REFUSED,
            expected_payload,
        )

    @mock.patch("api.cases.notify.send_email")
    def test_notify_exporter_ecju_query(self, mock_send_email):
        application = self.create_open_application_case(self.organisation)
        application.submitted_by = ExporterUserFactory()
        application.save()

        notify_exporter_ecju_query(application.pk)

        expected_payload = ExporterECJUQuery(
            exporter_first_name=application.submitted_by.first_name,
            case_reference=application.reference_code,
            exporter_frontend_url="https://exporter.lite.service.localhost.uktrade.digital/",
        )
        mock_send_email.assert_called_with(
            application.submitted_by.email,
            TemplateType.EXPORTER_ECJU_QUERY,
            expected_payload,
        )
        assert mock_send_email.called == 1
