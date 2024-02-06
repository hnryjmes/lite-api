from django.urls import reverse
from parameterized import parameterized
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN

from api.applications.models import BaseApplication
from api.cases.enums import CaseTypeSubTypeEnum
from lite_content.lite_api import strings
from test_helpers.clients import DataTestClient


class DeleteApplication(DataTestClient):
    def setUp(self):
        super().setUp()
        self.applications = {
            CaseTypeSubTypeEnum.STANDARD: self.create_draft_standard_application(self.organisation),
            CaseTypeSubTypeEnum.HMRC: self.create_hmrc_query(self.organisation),
        }
        self.users = {"EXPORTER": self.exporter_headers, "GOV": self.gov_headers, "HMRC": self.hmrc_exporter_headers}

    @parameterized.expand(
        [
            (CaseTypeSubTypeEnum.STANDARD, "EXPORTER"),
            (CaseTypeSubTypeEnum.HMRC, "HMRC"),
        ]
    )
    def test_delete_draft_application_as_valid_user_success(self, application_type, user):
        """
        Tests that applications can be deleted by their owners when in a draft state
        """
        draft = self.applications[application_type]
        headers = self.users[user]
        number_of_applications = BaseApplication.objects.all().count()
        url = reverse("applications:application", kwargs={"pk": draft.id})

        response = self.client.delete(url, **headers)

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.json()["status"], strings.Applications.Generic.DELETE_DRAFT_APPLICATION)
        self.assertEqual(number_of_applications - 1, BaseApplication.objects.all().count())
        self.assertTrue(draft not in BaseApplication.objects.all())

    @parameterized.expand(
        [
            (CaseTypeSubTypeEnum.STANDARD, "GOV"),
            (CaseTypeSubTypeEnum.HMRC, "EXPORTER"),
        ]
    )
    def test_delete_draft_application_as_invalid_user_failure(self, application_type, user):
        """
        Tests that applications cannot be deleted by users who do not own the application
        """
        draft = self.applications[application_type]
        headers = self.users[user]
        number_of_applications = BaseApplication.objects.all().count()
        url = reverse("applications:application", kwargs={"pk": draft.id})

        response = self.client.delete(url, **headers)

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
        self.assertEqual(number_of_applications, BaseApplication.objects.all().count())

    @parameterized.expand(
        [
            (CaseTypeSubTypeEnum.STANDARD, "EXPORTER"),
            (CaseTypeSubTypeEnum.HMRC, "HMRC"),
        ]
    )
    def test_delete_submitted_application_failure(self, application_type, user):
        """
        Tests that applications cannot be deleted after they have been submitted
        """
        application = self.applications[application_type]
        headers = self.users[user]
        self.submit_application(application)
        number_of_applications = BaseApplication.objects.all().count()
        url = reverse("applications:application", kwargs={"pk": application.id})

        response = self.client.delete(url, **headers)

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["errors"], strings.Applications.Generic.DELETE_SUBMITTED_APPLICATION_ERROR)
        self.assertEqual(number_of_applications, BaseApplication.objects.all().count())
