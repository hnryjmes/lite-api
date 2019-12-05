from parameterized import parameterized
from rest_framework import status
from rest_framework.reverse import reverse

from cases.models import Case
from queries.end_user_advisories.models import EndUserAdvisoryQuery
from static.statuses.enums import CaseStatusEnum
from static.statuses.libraries.get_case_status import get_case_status_by_status
from test_helpers.clients import DataTestClient


class EndUserAdvisoryViewTests(DataTestClient):
    def test_view_end_user_advisory_queries(self):
        """
        Ensure that the user can view all end user advisory queries
        """
        query = self.create_end_user_advisory("a note", "because I am unsure", self.organisation)

        response = self.client.get(reverse("queries:end_user_advisories:end_user_advisories"), **self.exporter_headers)
        response_data = response.json()["end_user_advisories"]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response_data), 1)

        response_data = response_data[0]
        self.assertEqual(response_data["note"], query.note)
        self.assertEqual(response_data["reasoning"], query.reasoning)

        end_user_data = response_data["end_user"]
        self.assertEqual(end_user_data["sub_type"]["key"], query.end_user.sub_type)

        self.assertEqual(end_user_data["name"], query.end_user.name)
        self.assertEqual(end_user_data["website"], query.end_user.website)
        self.assertEqual(end_user_data["address"], query.end_user.address)
        self.assertEqual(end_user_data["country"]["id"], query.end_user.country.id)

    def test_view_end_user_advisory_query_on_organisation(self):
        """
        Ensure that the user can view an end user advisory query
        """
        query = self.create_end_user_advisory("a note", "because I am unsure", self.organisation)

        response = self.client.get(
            reverse("queries:end_user_advisories:end_user_advisory", kwargs={"pk": query.id}), **self.exporter_headers
        )
        response_data = response.json()["end_user_advisory"]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data["note"], query.note)
        self.assertEqual(response_data["reasoning"], query.reasoning)
        self.assertEqual(response_data["nature_of_business"], query.nature_of_business)
        self.assertEqual(response_data["contact_name"], query.contact_name)
        self.assertEqual(response_data["contact_email"], query.contact_email)
        self.assertEqual(response_data["contact_telephone"], query.contact_telephone)
        self.assertEqual(response_data["contact_job_title"], query.contact_job_title)

        end_user_data = response_data["end_user"]
        self.assertEqual(end_user_data["sub_type"]["key"], query.end_user.sub_type)
        self.assertEqual(end_user_data["name"], query.end_user.name)
        self.assertEqual(end_user_data["website"], query.end_user.website)
        self.assertEqual(end_user_data["address"], query.end_user.address)
        self.assertEqual(end_user_data["country"]["id"], query.end_user.country.id)


class EndUserAdvisoryCreateTests(DataTestClient):
    url = reverse("queries:end_user_advisories:end_user_advisories")

    def test_create_end_user_advisory_query(self):
        """
        Ensure that a user can create an end user advisory, and that it creates a case
        when doing so
        """
        data = {
            "end_user": {
                "sub_type": "government",
                "name": "Ada",
                "website": "https://gov.uk",
                "address": "123",
                "country": "GB",
            },
            "note": "I Am Easy to Find",
            "reasoning": "Lack of hairpin turns",
            "nature_of_business": "guns",
            "contact_name": "Steven",
            "contact_email": "steven@gov.com",
            "contact_job_title": "director",
            "contact_telephone": "0123456789",
        }

        response = self.client.post(self.url, data, **self.exporter_headers)
        response_data = response.json()["end_user_advisory"]

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_data["note"], data["note"])
        self.assertEqual(response_data["reasoning"], data["reasoning"])
        self.assertEqual(response_data["contact_email"], data["contact_email"])
        self.assertEqual(response_data["contact_telephone"], data["contact_telephone"])
        self.assertEqual(response_data["contact_job_title"], data["contact_job_title"])

        end_user_data = response_data["end_user"]
        self.assertEqual(end_user_data["sub_type"]["key"], data["end_user"]["sub_type"])
        self.assertEqual(end_user_data["name"], data["end_user"]["name"])
        self.assertEqual(end_user_data["website"], data["end_user"]["website"])
        self.assertEqual(end_user_data["address"], data["end_user"]["address"])
        self.assertEqual(end_user_data["country"]["id"], data["end_user"]["country"])
        self.assertEqual(Case.objects.count(), 1)

    def test_create_copied_end_user_advisory_query(self):
        """
        Ensure that a user can duplicate an end user advisory, it links to the previous
        query and that it creates a case when doing so
        """
        query = self.create_end_user_advisory("Advisory", "", self.organisation)
        data = {
            "end_user": {
                "sub_type": "government",
                "name": "Ada",
                "website": "https://gov.uk",
                "address": "123",
                "country": "GB",
            },
            "note": "I Am Easy to Find",
            "reasoning": "Lack of hairpin turns",
            "copy_of": query.id,
            "nature_of_business": "guns",
            "contact_name": "Steven",
            "contact_email": "steven@gov.com",
            "contact_job_title": "director",
            "contact_telephone": "0123456789",
        }

        response = self.client.post(self.url, data, **self.exporter_headers)
        response_data = response.json()["end_user_advisory"]

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_data["note"], data["note"])
        self.assertEqual(response_data["reasoning"], data["reasoning"])
        self.assertEqual(response_data["copy_of"], str(data["copy_of"]))

        end_user_data = response_data["end_user"]
        self.assertEqual(end_user_data["sub_type"]["key"], data["end_user"]["sub_type"])
        self.assertEqual(end_user_data["name"], data["end_user"]["name"])
        self.assertEqual(end_user_data["website"], data["end_user"]["website"])
        self.assertEqual(end_user_data["address"], data["end_user"]["address"])
        self.assertEqual(end_user_data["country"]["id"], data["end_user"]["country"])
        self.assertEqual(Case.objects.count(), 2)

    @parameterized.expand(
        [
            ("com", "person", "http://gov.co.uk", "place street", "GB", "", "",),  # invalid end user type
            ("commercial", "", "", "nowhere", "GB", "", ""),  # name is empty
            ("government", "abc", "abc", "nowhere", "GB", "", "",),  # invalid web address
            ("government", "abc", "", "", "GB", "", ""),  # empty address
            ("government", "abc", "", "nowhere", "ALP", "", ""),  # invalid country code
            ("", "", "", "", "", "", ""),  # empty dataset
        ]
    )
    def test_create_end_user_advisory_query_failure(
        self, end_user_type, name, website, address, country, note, reasoning
    ):
        data = {
            "end_user": {
                "type": end_user_type,
                "name": name,
                "website": website,
                "address": address,
                "country": country,
            },
            "note": note,
            "reasoning": reasoning,
        }

        response = self.client.post(self.url, data, **self.exporter_headers)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_end_user_advisory_query_for_organisation_failure(self):
        """
        Fail to create organisation advisory with missing fields
        """
        data = {
            "end_user": {
                "sub_type": "commercial",
                "name": "Ada",
                "website": "https://gov.uk",
                "address": "123",
                "country": "GB",
            },
            "note": "I Am Easy to Find",
            "reasoning": "Lack of hairpin turns",
            "contact_email": "steven@gov.com",
            "contact_telephone": "0123456789",
            "nature_of_business": "",
            "contact_name": "",
            "contact_job_title": "",
        }

        response = self.client.post(self.url, data, **self.exporter_headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        errors = response.json()["errors"]

        self.assertEqual(errors.get("nature_of_business"), ["This field may not be blank"])
        self.assertEqual(errors.get("contact_name"), ["This field may not be blank"])
        self.assertEqual(errors.get("contact_job_title"), ["This field may not be blank"])

    def test_create_end_user_advisory_query_for_government_failure(self):
        """
        Fail to create gov advisory with missing fields
        """
        data = {
            "end_user": {
                "sub_type": "commercial",
                "name": "Ada",
                "website": "https://gov.uk",
                "address": "123",
                "country": "GB",
            },
            "note": "I Am Easy to Find",
            "reasoning": "Lack of hairpin turns",
            "contact_email": "steven@gov.com",
            "contact_telephone": "0123456789",
            "contact_name": "",
            "contact_job_title": "",
        }

        response = self.client.post(self.url, data, **self.exporter_headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        errors = response.json()["errors"]

        self.assertEqual(errors.get("contact_name"), ["This field may not be blank"])
        self.assertEqual(errors.get("contact_job_title"), ["This field may not be blank"])

    def test_create_end_user_advisory_query_for_government(self):
        """
        Successfully creates gov advisory
        """
        data = {
            "end_user": {
                "sub_type": "government",
                "name": "Ada",
                "website": "https://gov.uk",
                "address": "123",
                "country": "GB",
            },
            "note": "I Am Easy to Find",
            "reasoning": "Lack of hairpin turns",
            "contact_email": "steven@gov.com",
            "contact_telephone": "0123456789",
            "contact_name": "steven",
            "contact_job_title": "director",
        }

        response = self.client.post(self.url, data, **self.exporter_headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_end_user_advisory_query_for_individual(self):
        """
        Successfully create individual advisory
        """
        data = {
            "end_user": {
                "sub_type": "individual",
                "name": "Ada",
                "website": "https://gov.uk",
                "address": "123",
                "country": "GB",
            },
            "note": "I Am Easy to Find",
            "reasoning": "Lack of hairpin turns",
            "contact_email": "steven@gov.com",
            "contact_telephone": "0123456789",
        }

        response = self.client.post(self.url, data, **self.exporter_headers)
        response_data = response.json()["end_user_advisory"]

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_data["note"], data["note"])
        self.assertEqual(response_data["reasoning"], data["reasoning"])
        self.assertEqual(response_data["contact_email"], data["contact_email"])
        self.assertEqual(response_data["contact_telephone"], data["contact_telephone"])

        end_user_data = response_data["end_user"]
        self.assertEqual(end_user_data["sub_type"]["key"], data["end_user"]["sub_type"])
        self.assertEqual(end_user_data["name"], data["end_user"]["name"])
        self.assertEqual(end_user_data["website"], data["end_user"]["website"])
        self.assertEqual(end_user_data["address"], data["end_user"]["address"])
        self.assertEqual(end_user_data["country"]["id"], data["end_user"]["country"])
        self.assertEqual(Case.objects.count(), 1)


class EndUserAdvisoryUpdate(DataTestClient):
    def setUp(self):
        super().setUp()
        self.end_user_advisory = self.create_end_user_advisory_case(
            "end_user_advisory", "my reasons", organisation=self.organisation
        )
        self.url = reverse("queries:end_user_advisories:end_user_advisory", kwargs={"pk": self.end_user_advisory.id},)

    def test_update_end_user_advisory_status_success(self):
        data = {"status": CaseStatusEnum.RESUBMITTED}

        response = self.client.put(self.url, data, **self.gov_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        new_end_user_advisory = EndUserAdvisoryQuery.objects.get(pk=self.end_user_advisory.id)
        case_status = get_case_status_by_status(CaseStatusEnum.RESUBMITTED)
        self.assertEqual(new_end_user_advisory.status, case_status)
