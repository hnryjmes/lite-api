from rest_framework import status
from rest_framework.reverse import reverse

from cases.enums import CaseTypeEnum
from letter_templates.models import LetterTemplate
from picklists.enums import PickListStatus, PicklistType
from static.letter_layouts.models import LetterLayout
from test_helpers.clients import DataTestClient


class LetterTemplatesListTests(DataTestClient):
    def setUp(self):
        super().setUp()
        self.picklist_item = self.create_picklist_item(
            "#1", self.team, PicklistType.LETTER_PARAGRAPH, PickListStatus.ACTIVE
        )
        self.letter_layout = LetterLayout.objects.first()
        self.letter_template = LetterTemplate.objects.create(name="SIEL", layout=self.letter_layout,)
        self.letter_template.case_types.set([CaseTypeEnum.CLC_QUERY, CaseTypeEnum.END_USER_ADVISORY_QUERY])
        self.letter_template.letter_paragraphs.add(self.picklist_item)

    def test_get_letter_templates_success(self):
        url = reverse("letter_templates:letter_templates")

        response = self.client.get(url, **self.gov_headers)
        response_data = response.json()["results"][0]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data["id"], str(self.letter_template.id))
        self.assertEqual(response_data["name"], self.letter_template.name)
        self.assertEqual(response_data["layout"]["id"], str(self.letter_layout.id))
        self.assertEqual(response_data["letter_paragraphs"], [str(self.picklist_item.id)])
        self.assertIn(CaseTypeEnum.CLC_QUERY, str(response_data["case_types"]))
        self.assertIn(CaseTypeEnum.END_USER_ADVISORY_QUERY, str(response_data["case_types"]))
        self.assertIsNotNone(response_data.get("created_at"))
        self.assertIsNotNone(response_data.get("last_modified_at"))

    def test_get_letter_templates_for_case_success(self):
        url = reverse("letter_templates:letter_templates")
        self.letter_template.case_types.set([CaseTypeEnum.APPLICATION])
        case = self.create_standard_application_case(self.organisation)

        response = self.client.get(url + "?case=" + str(case.id), **self.gov_headers)
        response_data = response.json()["results"][0]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data["id"], str(self.letter_template.id))
        self.assertEqual(response_data["name"], self.letter_template.name)
        self.assertEqual(response_data["layout"]["id"], str(self.letter_layout.id))
        self.assertEqual(response_data["letter_paragraphs"], [str(self.picklist_item.id)])
        self.assertIn(CaseTypeEnum.APPLICATION, str(response_data["case_types"]))
        self.assertIsNotNone(response_data.get("created_at"))
        self.assertIsNotNone(response_data.get("last_modified_at"))

    def test_get_letter_template_success(self):
        url = reverse("letter_templates:letter_template", kwargs={"pk": str(self.letter_template.id)})
        response = self.client.get(url, **self.gov_headers)
        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        template = response_data["template"]
        self.assertEqual(template["id"], str(self.letter_template.id))
        self.assertEqual(template["name"], self.letter_template.name)
        self.assertEqual(template["layout"]["id"], str(self.letter_layout.id))
        self.assertEqual(template["letter_paragraphs"], [str(self.picklist_item.id)])
        self.assertIn(CaseTypeEnum.CLC_QUERY, str(template["case_types"]))
        self.assertIn(CaseTypeEnum.END_USER_ADVISORY_QUERY, str(template["case_types"]))
        self.assertIsNotNone(template.get("created_at"))
        self.assertIsNotNone(template.get("last_modified_at"))

    def test_get_letter_template_with_preview_success(self):
        url = reverse("letter_templates:letter_template", kwargs={"pk": str(self.letter_template.id)})
        url += "?generate_preview=True"

        response = self.client.get(url, **self.gov_headers)
        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("preview" in response_data)
        preview = response_data["preview"]
        for tag in ["<style>", "</style>"]:
            self.assertTrue(tag in preview)
        self.assertTrue(self.picklist_item.text in preview)

    def test_get_letter_template_with_text_success(self):
        url = reverse("letter_templates:letter_template", kwargs={"pk": str(self.letter_template.id)})
        url += "?text=True"

        response = self.client.get(url, **self.gov_headers)
        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("text" in response_data)
        self.assertTrue(self.picklist_item.text in response_data["text"])
