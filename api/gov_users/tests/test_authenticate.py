from django.urls import reverse
from rest_framework import status

from api.gov_users.enums import GovUserStatuses
from test_helpers.clients import DataTestClient
from api.users.models import GovUser


class GovUserAuthenticateTests(DataTestClient):

    url = reverse("gov_users:authenticate")

    def test_authentication_success(self):
        """
        Authorises user then checks the token which is sent is valid upon another request
        """
        data = {
            "email": self.gov_user.email,
            "first_name": self.gov_user.first_name,
            "last_name": self.gov_user.last_name,
        }

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert (
            GovUser.objects.filter(baseuser_ptr__email=self.gov_user.email).first().first_name
            == self.gov_user.first_name
        )
        assert (
            GovUser.objects.filter(baseuser_ptr__email=self.gov_user.email).first().last_name == self.gov_user.last_name
        )
        assert GovUser.objects.filter(baseuser_ptr__email=self.gov_user.email).first().pending is False

    def test_cannot_authenticate_gov_user_with_empty_data(self):
        data = {
            "email": None,
        }

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cannot_authenticate_gov_user_with_incorrect_details(self):
        data = {
            "email": "something@random.com",
        }

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_a_deactivated_user_cannot_log_in(self):
        self.gov_user.status = GovUserStatuses.DEACTIVATED
        self.gov_user.save()
        data = {
            "email": self.gov_user.email,
            "first_name": self.gov_user.first_name,
            "last_name": self.gov_user.last_name,
        }

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
