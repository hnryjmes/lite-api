from parameterized import parameterized

from django.urls import reverse

from rest_framework import status

from api.applications.libraries.case_status_helpers import get_case_statuses
from api.applications.enums import NSGListType
from api.applications.tests.factories import GoodOnApplicationFactory
from api.goods.tests.factories import GoodFactory, FirearmFactory
from api.staticdata.statuses.enums import CaseStatusEnum
from api.staticdata.statuses.libraries.get_case_status import get_case_status_by_status
from lite_content.lite_api import strings
from test_helpers.clients import DataTestClient


class EditGoodOnApplicationsTests(DataTestClient):
    def test_edit_a_good_on_applicaton(self):
        self.create_draft_standard_application(self.organisation)
        self.good_on_application.firearm_details = FirearmFactory.create()
        self.good_on_application.save()

        url = reverse(
            "applications:good_on_application",
            kwargs={"obj_pk": self.good_on_application.id},
        )

        response = self.client.put(
            url,
            data={
                "firearm_details": {
                    "year_of_manufacture": 1990,
                    "calibre": "1mm",
                },
            },
            **self.exporter_headers,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.good_on_application.refresh_from_db()
        self.assertEqual(
            self.good_on_application.firearm_details.year_of_manufacture,
            1990,
        )
        self.assertEqual(
            self.good_on_application.firearm_details.calibre,
            "1mm",
        )

    def test_edit_a_good_on_applicaton_read_only(self):
        application = self.create_draft_standard_application(self.organisation)
        uneditable_status = get_case_statuses(read_only=True)[0]
        application.status = get_case_status_by_status(uneditable_status)
        application.save()

        self.good_on_application.firearm_details = FirearmFactory.create()
        self.good_on_application.save()

        original_year_of_manufacture = self.good_on_application.firearm_details.year_of_manufacture
        original_calibre = self.good_on_application.firearm_details.calibre

        url = reverse(
            "applications:good_on_application",
            kwargs={"obj_pk": self.good_on_application.id},
        )

        response = self.client.put(
            url,
            data={
                "firearm_details": {
                    "year_of_manufacture": 1990,
                    "calibre": "1mm",
                },
            },
            **self.exporter_headers,
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), {"errors": [strings.Applications.Generic.READ_ONLY]})

        self.good_on_application.refresh_from_db()
        self.assertEqual(
            self.good_on_application.firearm_details.year_of_manufacture,
            original_year_of_manufacture,
        )
        self.assertEqual(
            self.good_on_application.firearm_details.calibre,
            original_calibre,
        )

    def test_edit_a_good_on_applicaton_invalid_organisation(self):
        another_organisation, _ = self.create_organisation_with_exporter_user()
        application = self.create_draft_standard_application(another_organisation)
        application.save()

        self.good_on_application.firearm_details = FirearmFactory.create()
        self.good_on_application.save()

        original_year_of_manufacture = self.good_on_application.firearm_details.year_of_manufacture
        original_calibre = self.good_on_application.firearm_details.calibre

        url = reverse(
            "applications:good_on_application",
            kwargs={"obj_pk": self.good_on_application.id},
        )

        response = self.client.put(
            url,
            data={
                "firearm_details": {
                    "year_of_manufacture": 1990,
                    "calibre": "1mm",
                },
            },
            **self.exporter_headers,
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), {"errors": [strings.Applications.Generic.INVALID_ORGANISATION]})

        self.good_on_application.refresh_from_db()
        self.assertEqual(
            self.good_on_application.firearm_details.year_of_manufacture,
            original_year_of_manufacture,
        )
        self.assertEqual(
            self.good_on_application.firearm_details.calibre,
            original_calibre,
        )


class GovUserEditGoodOnApplicationsTests(DataTestClient):
    def test_edit_trigger_list_assessment_and_nca(self):
        "Test updating trigger list assessment on multiple products on application"
        draft = self.create_draft_standard_application(self.organisation)
        application = self.submit_application(draft, self.exporter_user)
        self.good_on_application2 = GoodOnApplicationFactory(
            application=application,
            good=GoodFactory(organisation=self.organisation, is_good_controlled=True),
        )
        good_on_applications = [self.good_on_application, self.good_on_application2]

        for good_on_application in good_on_applications:
            self.assertEqual(good_on_application.nsg_list_type, "")
            self.assertIsNone(good_on_application.is_trigger_list_guidelines_applicable)
            self.assertIsNone(good_on_application.is_nca_applicable)
            self.assertEqual(good_on_application.nsg_assessment_note, "")

        url = reverse(
            "applications:good_on_application_update_internal",
            kwargs={"pk": application.id},
        )

        data = [
            {
                "id": self.good_on_application.id,
                "application": application.id,
                "good": self.good_on_application.good.id,
                "nsg_list_type": NSGListType.TRIGGER_LIST,
                "is_trigger_list_guidelines_applicable": True,
                "is_nca_applicable": False,
                "nsg_assessment_note": "Trigger list product1",
            },
            {
                "id": self.good_on_application2.id,
                "application": application.id,
                "good": self.good_on_application2.good.id,
                "nsg_list_type": NSGListType.TRIGGER_LIST,
                "is_trigger_list_guidelines_applicable": False,
                "is_nca_applicable": True,
                "nsg_assessment_note": "Trigger list product2",
            },
        ]

        response = self.client.put(url, data=data, **self.gov_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = response.json()

        for index, item in enumerate(response["data"]):
            self.assertEqual(item["nsg_list_type"]["key"], data[index]["nsg_list_type"])
            self.assertEqual(
                item["is_trigger_list_guidelines_applicable"], data[index]["is_trigger_list_guidelines_applicable"]
            )
            self.assertEqual(item["is_nca_applicable"], data[index]["is_nca_applicable"])
            self.assertEqual(item["nsg_assessment_note"], data[index]["nsg_assessment_note"])

        for index, obj in enumerate(good_on_applications):
            obj.refresh_from_db()
            self.assertEqual(obj.nsg_list_type, data[index]["nsg_list_type"])
            self.assertEqual(
                obj.is_trigger_list_guidelines_applicable, data[index]["is_trigger_list_guidelines_applicable"]
            )
            self.assertEqual(obj.is_nca_applicable, data[index]["is_nca_applicable"])
            self.assertEqual(obj.nsg_assessment_note, data[index]["nsg_assessment_note"])

    @parameterized.expand(CaseStatusEnum.terminal_statuses())
    def test_edit_good_on_terminal_status_application_forbidden(self, terminal_status):
        draft = self.create_draft_standard_application(self.organisation)
        application = self.submit_application(draft, self.exporter_user)
        self.good_on_application2 = GoodOnApplicationFactory(
            application=application,
            good=GoodFactory(organisation=self.organisation, is_good_controlled=True),
        )
        url = reverse(
            "applications:good_on_application_update_internal",
            kwargs={"pk": application.id},
        )

        application.status = get_case_status_by_status(terminal_status)
        application.save()

        response = self.client.put(
            url,
            data=[
                {
                    "id": self.good_on_application.id,
                    "application": application.id,
                    "good": self.good_on_application.good.id,
                    "nsg_list_type": NSGListType.TRIGGER_LIST,
                    "is_trigger_list_guidelines_applicable": True,
                    "is_nca_applicable": True,
                    "nsg_assessment_note": "Trigger list product1",
                },
                {
                    "id": self.good_on_application2.id,
                    "application": application.id,
                    "good": self.good_on_application2.good.id,
                    "nsg_list_type": NSGListType.TRIGGER_LIST,
                    "is_trigger_list_guidelines_applicable": False,
                    "is_nca_applicable": True,
                    "nsg_assessment_note": "Trigger list product2",
                },
            ],
            **self.gov_headers,
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_edit_good_on_application_bad_request(self):
        draft = self.create_draft_standard_application(self.organisation)
        application = self.submit_application(draft, self.exporter_user)

        url = reverse(
            "applications:good_on_application_update_internal",
            kwargs={"pk": application.id},
        )

        response = self.client.put(
            url,
            data=[
                {
                    "id": self.good_on_application.id,
                    "application": application.id,
                    "good": self.good_on_application.good.id,
                    "nsg_list_type": "INVALID_LIST_TYPE",
                    "is_trigger_list_guidelines_applicable": False,
                    "is_nca_applicable": True,
                    "nsg_assessment_note": "Trigger list product1",
                },
            ],
            **self.gov_headers,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = response.json()
        self.assertEqual(response["errors"][0]["nsg_list_type"], ['"INVALID_LIST_TYPE" is not a valid choice.'])
