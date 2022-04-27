from api.flags.enums import SystemFlags
from parameterized import parameterized
from api.goods.enums import GoodStatus
from test_helpers.clients import DataTestClient
from api.applications.tests.factories import GoodOnApplicationFactory
from django.urls import reverse


class GoodPrecedentsListViewTests(DataTestClient):
    def setUp(self):
        super().setUp()

        # Create a common good
        self.good = self.create_good("A good", self.organisation)
        self.good.flags.add(SystemFlags.WASSENAAR)
        # Create an application
        self.draft_1 = self.create_draft_standard_application(self.organisation)
        self.gona_1 = GoodOnApplicationFactory(
            good=self.good, application=self.draft_1, quantity=5, report_summary="test"
        )
        self.case = self.submit_application(self.draft_1)
        self.case.queues.set([self.queue])

        # Create another application
        self.draft_2 = self.create_draft_standard_application(self.organisation)
        self.gona_2 = GoodOnApplicationFactory(good=self.good, application=self.draft_2)
        self.submit_application(self.draft_2)
        self.url = reverse("cases:good_precedents", kwargs={"pk": self.case.id})

    @parameterized.expand(
        [(GoodStatus.DRAFT, 0), (GoodStatus.SUBMITTED, 0), (GoodStatus.QUERY, 0), (GoodStatus.VERIFIED, 2)]
    )
    def test_get(self, status, count):
        self.good.status = status
        self.good.save()
        response = self.client.get(self.url, **self.gov_headers)
        assert response.status_code == 200
        json = response.json()
        assert json["count"] == count
        if count > 0:
            # Check the first gona b/c it is more interesting
            gona = json["results"][0]
            assert gona["id"] == str(self.gona_1.id)
            assert gona["good"] == str(self.good.id)
            assert gona["application"] == str(self.draft_1.id)
            assert gona["reference"] == self.draft_1.reference_code
            assert gona["destinations"] == ["GB"]
            assert gona["wassenaar"]
            assert gona["quantity"] == 5.0
            assert gona["report_summary"] == "test"
