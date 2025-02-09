import pytest
from django.urls import reverse
from parameterized import parameterized
from rest_framework import status

from api.cases.enums import AdviceType, AdviceLevel
from api.cases.models import Advice
from api.cases.tests.factories import TeamAdviceFactory
from api.core import constants
from api.core.helpers import convert_queryset_to_str
from api.goods.enums import PvGrading
from api.staticdata.statuses.enums import CaseStatusEnum
from api.staticdata.statuses.libraries.get_case_status import get_case_status_by_status
from api.teams.tests.factories import TeamFactory
from api.users.tests.factories import GovUserFactory
from test_helpers.clients import DataTestClient
from api.users.models import GovUser, Role


class CreateCaseTeamAdviceTests(DataTestClient):
    def setUp(self):
        super().setUp()

        self.standard_application = self.create_draft_standard_application(self.organisation)
        self.good = self.standard_application.goods.first().good
        self.standard_case = self.submit_application(self.standard_application)

        self.role = Role(name="team_level")
        self.role.permissions.set(
            [
                constants.GovPermissions.MANAGE_TEAM_ADVICE.name,
                constants.GovPermissions.MANAGE_TEAM_CONFIRM_OWN_ADVICE.name,
            ]
        )
        self.role.save()

        self.gov_user.role = self.role
        self.gov_user.save()

        self.gov_user_2 = GovUserFactory(baseuser_ptr__email="user@email.com", team=self.team, role=self.role)
        self.gov_user_3 = GovUserFactory(baseuser_ptr__email="users@email.com", team=self.team, role=self.role)

        self.open_application = self.create_draft_open_application(self.organisation)
        self.open_case = self.submit_application(self.open_application)

        self.standard_case_url = reverse("cases:team_advice", kwargs={"pk": self.standard_case.id})
        self.open_case_url = reverse("cases:team_advice", kwargs={"pk": self.open_case.id})

    def test_advice_is_concatenated_when_team_advice_first_created(self):
        """
        Team advice is created on first call
        """
        self.create_advice(self.gov_user, self.standard_case, "end_user", AdviceType.PROVISO, AdviceLevel.TEAM)
        self.create_advice(self.gov_user_2, self.standard_case, "end_user", AdviceType.PROVISO, AdviceLevel.TEAM)
        self.create_advice(self.gov_user, self.standard_case, "good", AdviceType.NO_LICENCE_REQUIRED, AdviceLevel.TEAM)
        self.create_advice(
            self.gov_user_2, self.standard_case, "good", AdviceType.NO_LICENCE_REQUIRED, AdviceLevel.TEAM
        )

        response = self.client.get(self.standard_case_url, **self.gov_headers)
        response_data = response.json()["advice"]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_data), 2)

        end_user, good = None, None
        for data in response_data:
            if data.get("end_user"):
                end_user = data.get("type").get("key")
            elif data.get("good"):
                good = data.get("type").get("key")

        self.assertEqual(end_user, AdviceType.PROVISO)
        self.assertEqual(good, AdviceType.NO_LICENCE_REQUIRED)

    def test_create_conflicting_team_advice_shows_all_fields(self):
        """
        The type should show conflicting if there are conflicting types in the advice on a single object
        """
        self.create_advice(self.gov_user, self.standard_case, "good", AdviceType.NO_LICENCE_REQUIRED, AdviceLevel.USER)
        self.create_advice(self.gov_user_2, self.standard_case, "good", AdviceType.REFUSE, AdviceLevel.USER)
        self.create_advice(self.gov_user_3, self.standard_case, "good", AdviceType.PROVISO, AdviceLevel.USER)

        response = self.client.get(self.standard_case_url, **self.gov_headers)
        response_data = response.json()["advice"][0]

        self.assertEqual(response_data.get("type").get("key"), "conflicting")
        self.assertEqual(response_data.get("proviso"), "I am easy to proviso")
        self.assertCountEqual(["1a", "1b", "1c"], response_data["denial_reasons"])

    # Normal restrictions on team advice items
    @parameterized.expand(
        [
            [AdviceType.APPROVE],
            [AdviceType.PROVISO],
            [AdviceType.REFUSE],
            [AdviceType.NO_LICENCE_REQUIRED],
            [AdviceType.NOT_APPLICABLE],
        ]
    )
    def test_create_end_user_case_team_advice(self, advice_type):
        """
        Tests that a gov user can create an approval/proviso/refuse/nlr/not_applicable
        piece of team level advice for an end user
        """
        data = {
            "text": "I Am Easy to Find",
            "note": "I Am Easy to Find",
            "type": advice_type,
            "end_user": str(self.standard_application.end_user.party.id),
        }

        if advice_type == AdviceType.PROVISO:
            data["proviso"] = "I am easy to proviso"

        if advice_type == AdviceType.REFUSE:
            data["denial_reasons"] = ["1a", "1b", "1c"]

        response = self.client.post(self.standard_case_url, **self.gov_headers, data=[data])
        response_data = response.json()["advice"][0]

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response_data["text"], data["text"])
        self.assertEqual(response_data["note"], data["note"])
        self.assertEqual(response_data["type"]["key"], data["type"])
        self.assertEqual(response_data["end_user"], data["end_user"])

        advice_object = Advice.objects.get()

        # Ensure that proviso details aren't added unless the type sent is PROVISO
        if advice_type != AdviceType.PROVISO:
            self.assertEqual(response_data["proviso"], None)
            self.assertEqual(advice_object.proviso, None)
        else:
            self.assertEqual(response_data["proviso"], data["proviso"])
            self.assertEqual(advice_object.proviso, data["proviso"])

        # Ensure that refusal details aren't added unless the type sent is REFUSE
        if advice_type != AdviceType.REFUSE:
            self.assertEqual(response_data["denial_reasons"], [])
            self.assertEqual(advice_object.denial_reasons.count(), 0)
        else:
            self.assertCountEqual(response_data["denial_reasons"], data["denial_reasons"])
            self.assertCountEqual(
                convert_queryset_to_str(advice_object.denial_reasons.values_list("id", flat=True)),
                data["denial_reasons"],
            )

    # User must have permission to create team advice
    def test_user_cannot_create_team_level_advice_without_permissions(self):
        """
        Tests that the right level of permissions are required
        """
        self.gov_user.role.permissions.set([])
        self.gov_user.save()
        response = self.client.get(self.standard_case_url, **self.gov_headers)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.post(self.standard_case_url, **self.gov_headers)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.delete(self.standard_case_url, **self.gov_headers)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_advice_from_another_team_not_collated(self):
        """
        When collating advice, only the user's team's advice should be collated
        """
        TeamAdviceFactory(user=self.gov_user, team=self.team, case=self.standard_case, good=self.good)
        team_2 = TeamFactory()
        self.gov_user_2.team = team_2
        self.gov_user_2.save()
        TeamAdviceFactory(user=self.gov_user_2, team=team_2, case=self.standard_case, good=self.good)

        response = self.client.get(self.standard_case_url, **self.gov_headers)
        response_data = response.json()["advice"]

        # Team 2's advice would conflict with team 1's if both were brought in
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_submit_user_level_advice_if_team_advice_exists(
        self,
    ):
        """
        Can submit lower tier advice if higher tier advice exists
        """
        TeamAdviceFactory(user=self.gov_user_2, team=self.team, case=self.standard_case, good=self.good)

        data = {
            "text": "I Am Easy to Find",
            "note": "I Am Easy to Find",
            "type": AdviceType.APPROVE,
            "end_user": str(self.standard_application.end_user.party.id),
        }

        response = self.client.post(
            reverse("cases:user_advice", kwargs={"pk": self.standard_case.id}), **self.gov_headers, data=[data]
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_can_submit_user_level_advice_if_team_advice_has_been_cleared_for_that_team_on_that_case(
        self,
    ):
        """
        No residual data is left to block lower tier advice being submitted after a clear
        """
        self.create_advice(self.gov_user_2, self.standard_case, "good", AdviceType.PROVISO, AdviceLevel.USER)

        self.client.delete(self.standard_case_url, **self.gov_headers)

        data = {
            "text": "I Am Easy to Find",
            "note": "I Am Easy to Find",
            "type": AdviceType.APPROVE,
            "end_user": str(self.standard_application.end_user.party.id),
        }

        response = self.client.post(
            reverse("cases:user_advice", kwargs={"pk": self.standard_case.id}), **self.gov_headers, data=[data]
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_and_delete_audit_trail_is_created_when_the_appropriate_actions_take_place(
        self,
    ):
        """
        Audit trail is created when clearing or combining advice
        """
        self.create_advice(
            self.gov_user, self.standard_case, "end_user", AdviceType.NO_LICENCE_REQUIRED, AdviceLevel.USER
        )
        self.create_advice(self.gov_user_2, self.standard_case, "good", AdviceType.REFUSE, AdviceLevel.USER)
        self.create_advice(self.gov_user_3, self.standard_case, "good", AdviceType.PROVISO, AdviceLevel.USER)

        self.client.get(self.standard_case_url, **self.gov_headers)
        self.client.delete(self.standard_case_url, **self.gov_headers)

        response = self.client.get(reverse("cases:activity", kwargs={"pk": self.standard_case.id}), **self.gov_headers)

        self.assertEqual(len(response.json()["activity"]), 3)

    # def test_creating_team_advice_does_not_overwrite_user_level_advice(self):
    #     """
    #     Because of the shared parent class, make sure the parent class "save" method is overridden by the child class
    #     """
    #     self.create_advice(self.gov_user, self.standard_case, "end_user", AdviceType.NO_LICENCE_REQUIRED, AdviceLevel.USER)
    #     self.create_advice(self.gov_user, self.standard_case, "end_user", AdviceType.NO_LICENCE_REQUIRED, AdviceLevel.TEAM)
    #
    #     self.client.get(self.standard_case_url, **self.gov_headers)
    #
    #     self.assertEqual(Advice.objects.count(), 2)

    @parameterized.expand(
        [
            [AdviceType.APPROVE],
            [AdviceType.PROVISO],
            [AdviceType.REFUSE],
            [AdviceType.NO_LICENCE_REQUIRED],
            [AdviceType.NOT_APPLICABLE],
        ]
    )
    def test_coalesce_merges_duplicate_advice_instead_of_appending_it_simple(self, advice_type):
        """
        Makes sure we strip out duplicates of advice on the same object
        """
        self.create_advice(self.gov_user_2, self.standard_case, "good", advice_type, AdviceLevel.USER)
        self.create_advice(self.gov_user_3, self.standard_case, "good", advice_type, AdviceLevel.USER)

        response = self.client.get(self.standard_case_url, **self.gov_headers)
        response_data = response.json()["advice"]

        self.assertNotIn("\n-------\n", response_data[0]["text"])

    def test_merge_user_advice_same_advice_type_same_pv_gradings(self):
        """
        Same advice type, same pv grading
        """
        pv_grading = PvGrading.UK_OFFICIAL
        self.create_advice(
            self.gov_user_2, self.standard_case, "good", AdviceType.APPROVE, AdviceLevel.USER, pv_grading
        )
        self.create_advice(
            self.gov_user_3, self.standard_case, "good", AdviceType.APPROVE, AdviceLevel.USER, pv_grading
        )

        response = self.client.get(self.standard_case_url, **self.gov_headers)
        response_data = response.json()["advice"]

        self.assertNotIn("\n-------\n", response_data[0]["text"])
        self.assertEqual(
            PvGrading.to_str(pv_grading), Advice.objects.get(id=response_data[0]["id"]).collated_pv_grading
        )

    def test_merge_user_advice_same_advice_type_different_pv_gradings(self):
        """
        Same advice types, different pv gradings
        """
        pv_grading = PvGrading.UK_OFFICIAL
        pv_grading_2 = PvGrading.UK_OFFICIAL_SENSITIVE
        self.create_advice(
            self.gov_user_2, self.standard_case, "good", AdviceType.APPROVE, AdviceLevel.USER, pv_grading
        )
        self.create_advice(
            self.gov_user_3, self.standard_case, "good", AdviceType.APPROVE, AdviceLevel.USER, pv_grading_2
        )

        response = self.client.get(self.standard_case_url, **self.gov_headers)
        response_data = response.json()["advice"]

        self.assertNotIn("\n-------\n", response_data[0]["text"])
        self.assertIn("\n-------\n", Advice.objects.get(id=response_data[0]["id"]).collated_pv_grading)

    def test_merge_user_advice_different_advice_type_different_pv_gradings(self):
        """
        Different advice type, different pv gradings
        """
        pv_grading = PvGrading.UK_OFFICIAL
        pv_grading_2 = PvGrading.UK_OFFICIAL_SENSITIVE
        self.create_advice(
            self.gov_user_2, self.standard_case, "good", AdviceType.APPROVE, AdviceLevel.USER, pv_grading
        )
        self.create_advice(
            self.gov_user_3, self.standard_case, "good", AdviceType.PROVISO, AdviceLevel.USER, pv_grading_2
        )

        response = self.client.get(self.standard_case_url, **self.gov_headers)
        response_data = response.json()["advice"]

        self.assertNotIn("\n-------\n", response_data[0]["text"])
        self.assertIn("\n-------\n", Advice.objects.get(id=response_data[0]["id"]).collated_pv_grading)

    def test_merge_user_advice_different_advice_type_same_pv_gradings(self):
        """
        Different advice type, same pv gradings
        """
        pv_grading = PvGrading.UK_OFFICIAL
        self.create_advice(
            self.gov_user_2, self.standard_case, "good", AdviceType.APPROVE, AdviceLevel.USER, pv_grading
        )
        self.create_advice(
            self.gov_user_3, self.standard_case, "good", AdviceType.PROVISO, AdviceLevel.USER, pv_grading
        )

        response = self.client.get(self.standard_case_url, **self.gov_headers)
        response_data = response.json()["advice"]

        self.assertNotIn("\n-------\n", response_data[0]["text"])
        self.assertEqual(
            PvGrading.to_str(pv_grading), Advice.objects.get(id=response_data[0]["id"]).collated_pv_grading
        )

    def test_when_user_advice_exists_combine_team_advice_with_confirm_own_advice_success(
        self,
    ):
        self.role.permissions.set([constants.GovPermissions.MANAGE_TEAM_CONFIRM_OWN_ADVICE.name])
        self.create_advice(self.gov_user, self.standard_case, "good", AdviceType.PROVISO, AdviceLevel.USER)

        response = self.client.get(
            reverse("cases:team_advice", kwargs={"pk": self.standard_case.id}), **self.gov_headers
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_when_user_advice_exists_clear_team_advice_with_confirm_own_advice_success(
        self,
    ):
        self.role.permissions.set([constants.GovPermissions.MANAGE_TEAM_CONFIRM_OWN_ADVICE.name])
        self.create_advice(self.gov_user, self.standard_case, "good", AdviceType.PROVISO, AdviceLevel.USER)

        response = self.client.delete(
            reverse("cases:team_advice", kwargs={"pk": self.standard_case.id}), **self.gov_headers
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_when_user_advice_exists_create_team_advice_with_confirm_own_advice_success(
        self,
    ):
        self.role.permissions.set([constants.GovPermissions.MANAGE_TEAM_CONFIRM_OWN_ADVICE.name])
        self.create_advice(self.gov_user, self.standard_case, "good", AdviceType.PROVISO, AdviceLevel.USER)
        data = {
            "text": "I Am Easy to Find",
            "note": "I Am Easy to Find",
            "type": AdviceType.APPROVE,
            "end_user": str(self.standard_application.end_user.party.id),
        }

        response = self.client.post(
            reverse("cases:team_advice", kwargs={"pk": self.standard_case.id}), **self.gov_headers, data=[data]
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @parameterized.expand(CaseStatusEnum.terminal_statuses())
    def test_cannot_create_team_advice_when_case_in_terminal_state(self, terminal_status):
        data = {
            "text": "I Am Easy to Find",
            "note": "I Am Easy to Find",
            "type": AdviceType.APPROVE,
            "end_user": str(self.standard_application.end_user.party.id),
        }

        self.standard_application.status = get_case_status_by_status(terminal_status)
        self.standard_application.save()

        response = self.client.post(self.standard_case_url, **self.gov_headers, data=[data])

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
