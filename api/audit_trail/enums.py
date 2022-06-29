from api.common.enums import LiteEnum, autostr
from lite_content.lite_api import audit


class AuditType(LiteEnum):
    CREATED = autostr()
    OGL_CREATED = autostr()
    OGL_FIELD_EDITED = autostr()
    OGL_MULTI_FIELD_EDITED = autostr()
    ADD_FLAGS = autostr()
    REMOVE_FLAGS = autostr()
    GOOD_REVIEWED = autostr()
    GOOD_ADD_FLAGS = autostr()
    GOOD_REMOVE_FLAGS = autostr()
    GOOD_ADD_REMOVE_FLAGS = autostr()
    DESTINATION_ADD_FLAGS = autostr()
    DESTINATION_REMOVE_FLAGS = autostr()
    ADD_GOOD_TO_APPLICATION = autostr()
    REMOVE_GOOD_FROM_APPLICATION = autostr()
    ADD_GOOD_TYPE_TO_APPLICATION = autostr()
    REMOVE_GOOD_TYPE_FROM_APPLICATION = autostr()
    UPDATE_APPLICATION_END_USE_DETAIL = autostr()
    UPDATE_APPLICATION_TEMPORARY_EXPORT = autostr()
    REMOVED_SITES_FROM_APPLICATION = autostr()
    ADD_SITES_TO_APPLICATION = autostr()
    REMOVED_EXTERNAL_LOCATIONS_FROM_APPLICATION = autostr()
    ADD_EXTERNAL_LOCATIONS_TO_APPLICATION = autostr()
    REMOVED_COUNTRIES_FROM_APPLICATION = autostr()
    ADD_COUNTRIES_TO_APPLICATION = autostr()
    ADD_ADDITIONAL_CONTACT_TO_CASE = autostr()
    MOVE_CASE = autostr()
    ASSIGN_CASE = autostr()
    ASSIGN_USER_TO_CASE = autostr()
    REMOVE_CASE = autostr()
    REMOVE_CASE_FROM_ALL_QUEUES = autostr()
    REMOVE_CASE_FROM_ALL_USER_ASSIGNMENTS = autostr()
    CLC_RESPONSE = autostr()
    PV_GRADING_RESPONSE = autostr()
    CREATED_CASE_NOTE = autostr()
    ECJU_QUERY = autostr()
    UPDATED_STATUS = autostr()
    UPDATED_APPLICATION_NAME = autostr()
    UPDATE_APPLICATION_LETTER_REFERENCE = autostr()
    UPDATE_APPLICATION_F680_CLEARANCE_TYPES = autostr()
    ADDED_APPLICATION_LETTER_REFERENCE = autostr()
    REMOVED_APPLICATION_LETTER_REFERENCE = autostr()
    ASSIGNED_COUNTRIES_TO_GOOD = autostr()
    REMOVED_COUNTRIES_FROM_GOOD = autostr()
    CREATED_FINAL_ADVICE = autostr()
    CLEARED_FINAL_ADVICE = autostr()
    CREATED_TEAM_ADVICE = autostr()
    CLEARED_TEAM_ADVICE = autostr()
    REVIEW_COMBINE_ADVICE = autostr()
    CREATED_USER_ADVICE = autostr()
    CLEARED_USER_ADVICE = autostr()
    ADD_PARTY = autostr()
    REMOVE_PARTY = autostr()
    UPLOAD_PARTY_DOCUMENT = autostr()
    DELETE_PARTY_DOCUMENT = autostr()
    UPLOAD_APPLICATION_DOCUMENT = autostr()
    DELETE_APPLICATION_DOCUMENT = autostr()
    UPLOAD_CASE_DOCUMENT = autostr()
    GENERATE_CASE_DOCUMENT = autostr()
    ADD_CASE_OFFICER_TO_CASE = autostr()
    REMOVE_CASE_OFFICER_FROM_CASE = autostr()
    GRANTED_APPLICATION = autostr()
    REINSTATED_APPLICATION = autostr()
    FINALISED_APPLICATION = autostr()
    UNASSIGNED_QUEUES = autostr()
    UNASSIGNED = autostr()
    CREATED_DOCUMENT_TEMPLATE = autostr()
    UPDATED_LETTER_TEMPLATE_NAME = autostr()
    ADDED_LETTER_TEMPLATE_CASE_TYPES = autostr()
    UPDATED_LETTER_TEMPLATE_CASE_TYPES = autostr()
    REMOVED_LETTER_TEMPLATE_CASE_TYPES = autostr()
    ADDED_LETTER_TEMPLATE_DECISIONS = autostr()
    UPDATED_LETTER_TEMPLATE_DECISIONS = autostr()
    REMOVED_LETTER_TEMPLATE_DECISIONS = autostr()
    UPDATED_LETTER_TEMPLATE_PARAGRAPHS = autostr()
    REMOVED_LETTER_TEMPLATE_PARAGRAPHS = autostr()
    ADDED_LETTER_TEMPLATE_PARAGRAPHS = autostr()
    UPDATED_LETTER_TEMPLATE_LAYOUT = autostr()
    UPDATED_LETTER_TEMPLATE_PARAGRAPHS_ORDERING = autostr()
    UPDATED_LETTER_TEMPLATE_INCLUDE_DIGITAL_SIGNATURE = autostr()
    CREATED_PICKLIST = autostr()
    UPDATED_PICKLIST_TEXT = autostr()
    UPDATED_PICKLIST_NAME = autostr()
    DEACTIVATE_PICKLIST = autostr()
    REACTIVATE_PICKLIST = autostr()
    UPDATED_EXHIBITION_DETAILS_TITLE = autostr()
    UPDATED_EXHIBITION_DETAILS_START_DATE = autostr()
    UPDATED_EXHIBITION_DETAILS_REQUIRED_BY_DATE = autostr()
    UPDATED_EXHIBITION_DETAILS_REASON_FOR_CLEARANCE = autostr()
    UPDATED_ROUTE_OF_GOODS = autostr()
    UPDATED_ORGANISATION = autostr()
    CREATED_ORGANISATION = autostr()
    REGISTER_ORGANISATION = autostr()
    REJECTED_ORGANISATION = autostr()
    APPROVED_ORGANISATION = autostr()
    REMOVED_FLAG_ON_ORGANISATION = autostr()
    ADDED_FLAG_ON_ORGANISATION = autostr()
    RERUN_ROUTING_RULES = autostr()
    ENFORCEMENT_CHECK = autostr()
    UPDATED_SITE = autostr()
    CREATED_SITE = autostr()
    UPDATED_SITE_NAME = autostr()
    COMPLIANCE_SITE_CASE_CREATE = autostr()
    COMPLIANCE_SITE_CASE_NEW_LICENCE = autostr()
    ADDED_NEXT_REVIEW_DATE = autostr()
    EDITED_NEXT_REVIEW_DATE = autostr()
    REMOVED_NEXT_REVIEW_DATE = autostr()
    COMPLIANCE_VISIT_CASE_CREATED = autostr()
    COMPLIANCE_VISIT_CASE_UPDATED = autostr()
    COMPLIANCE_PEOPLE_PRESENT_CREATED = autostr()
    COMPLIANCE_PEOPLE_PRESENT_UPDATED = autostr()
    COMPLIANCE_PEOPLE_PRESENT_DELETED = autostr()
    UPDATED_GOOD_ON_DESTINATION_MATRIX = autostr()
    LICENCE_UPDATED_GOOD_USAGE = autostr()
    OGEL_REISSUED = autostr()
    LICENCE_UPDATED_STATUS = autostr()
    DOCUMENT_ON_ORGANISATION_CREATE = autostr()
    DOCUMENT_ON_ORGANISATION_DELETE = autostr()
    DOCUMENT_ON_ORGANISATION_UPDATE = autostr()
    REPORT_SUMMARY_UPDATED = autostr()
    COUNTERSIGN_ADVICE = autostr()
    UPDATED_SERIAL_NUMBERS = autostr()
    PRODUCT_REVIEWED = autostr()
    LICENCE_UPDATED_PRODUCT_USAGE = autostr()
    CREATED_FINAL_RECOMMENDATION = autostr()
    GENERATE_DECISION_LETTER = autostr()

    def human_readable(self):
        """
        Return a human readable version of the audit type

        If a human readable string exists in content return that,
        else return an auto generated string (i.e. correct capitalisation, no underscores)
        """
        if hasattr(audit, self.name):
            return getattr(audit, self.name)
        value = self.value.replace("_", " ")
        return value.capitalize()
