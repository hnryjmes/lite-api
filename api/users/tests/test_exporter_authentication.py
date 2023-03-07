from django.urls import reverse
from rest_framework import status

from test_helpers.clients import DataTestClient
from api.users.models import ExporterUser


class ExporterUserAuthenticateTests(DataTestClient):

    url = reverse("users:authenticate")

    def test_authentication_success(self):
        """
        Authorises user then checks the token which is sent is valid upon another request
        """
        data = {
            "email": self.exporter_user.email,
            "sub": "xyz123456",
            "user_profile": {"first_name": "Matt", "last_name": "Berninger"},
        }

        response = self.client.post(self.url, data)
        response_data = response.json()
        self.exporter_user.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        headers = {
            "HTTP_EXPORTER_USER_TOKEN": response_data["token"],
            "HTTP_ORGANISATION_ID": str(self.organisation.id),
        }

        self.assertEqual(self.exporter_user.first_name, data["user_profile"]["first_name"])
        self.assertEqual(self.exporter_user.last_name, data["user_profile"]["last_name"])
        self.assertFalse(self.exporter_user.pending)
        self.assertEqual(self.exporter_user.external_id, data["sub"])

        response = self.client.get(reverse("goods:goods"), **headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cannot_authenticate_user_with_empty_data(self):
        data = {"email": None, "user_profile": {"first_name": None, "last_name": None}}

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cannot_authenticate_user_with_incorrect_details(self):
        data = {"email": "something@random.com", "user_profile": {"first_name": "Bob", "last_name": "Dell"}}

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authentication_with_email_in_uppercase(self):
        data = {
            "email": self.exporter_user.email.upper(),
            "user_profile": {"first_name": "Matt", "last_name": "Berninger"},
        }

        response = self.client.post(self.url, data)
        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        headers = {
            "HTTP_EXPORTER_USER_TOKEN": response_data["token"],
            "HTTP_ORGANISATION_ID": str(self.organisation.id),
        }

        response = self.client.get(reverse("goods:goods"), **headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_already_existing_user_without_profile_payload_success(self):
        data = {
            "email": self.exporter_user.email,
            "sub": "xyz123456",
        }
        self.exporter_user.baseuser_ptr.first_name = "First"
        self.exporter_user.baseuser_ptr.last_name = "Last"
        self.exporter_user.baseuser_ptr.pending = True
        self.exporter_user.baseuser_ptr.save()

        response = self.client.post(self.url, data)
        response_data = response.json()
        self.exporter_user.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        headers = {
            "HTTP_EXPORTER_USER_TOKEN": response_data["token"],
            "HTTP_ORGANISATION_ID": str(self.organisation.id),
        }

        self.assertEqual(self.exporter_user.first_name, "First")
        self.assertEqual(self.exporter_user.last_name, "Last")
        self.assertTrue(self.exporter_user.pending)
        self.assertEqual(self.exporter_user.external_id, data["sub"])

        response = self.client.get(reverse("goods:goods"), **headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
