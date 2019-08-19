from django.urls import reverse
from rest_framework import status

from static.countries.models import Country
from test_helpers.clients import DataTestClient


class CountriesOnDraftTests(DataTestClient):

    COUNTRIES_COUNT = 10

    def setUp(self):
        super().setUp()
        self.draft = self.create_standard_draft(self.exporter_user.organisation)

        self.url = reverse('drafts:countries', kwargs={'pk': self.draft.id})

    def test_add_countries_to_a_draft_success(self):
        data = {
            'countries': Country.objects.all()[:self.COUNTRIES_COUNT].values_list('id', flat=True)
        }

        response = self.client.post(self.url, data, **self.exporter_headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get(self.url, **self.exporter_headers).json()
        self.assertEqual(len(response['countries']), self.COUNTRIES_COUNT)

    def test_add_countries_to_a_draft_failure(self):
        """
        Incorrect values
        """
        data = {
            'countries': ['1234']
        }

        response = self.client.post(self.url, data, **self.exporter_headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.get(self.url, **self.exporter_headers).json()
        self.assertEqual(len(response['countries']), 0)

    def test_add_countries_to_another_orgs_draft_failure(self):
        """
        Ensure that a user cannot add countries to another organisation's draft
        """
        organisation_2 = self.create_organisation()
        self.draft = self.create_standard_draft(organisation_2)
        self.url = reverse('drafts:countries', kwargs={'pk': self.draft.id})

        data = {
            'countries': Country.objects.all()[:self.COUNTRIES_COUNT].values_list('id', flat=True)
        }

        response = self.client.post(self.url, data, **self.exporter_headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.get(self.url, **self.exporter_headers).json()
        self.assertEqual(len(response['countries']), 0)
