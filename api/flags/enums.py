from api.core.constants import GovPermissions


class FlagLevels:
    CASE = "Case"
    ORGANISATION = "Organisation"
    GOOD = "Good"
    DESTINATION = "Destination"
    PARTY_ON_APPLICATION = "PartyOnApplication"

    choices = [
        (CASE, "Case"),
        (ORGANISATION, "Organisation"),
        (GOOD, "Good"),
        (DESTINATION, "Destination"),
        (PARTY_ON_APPLICATION, "PartyOnApplication"),
    ]


class FlagStatuses:
    ACTIVE = "Active"
    DEACTIVATED = "Deactivated"

    choices = [
        (ACTIVE, "Active"),
        (DEACTIVATED, "Deactivated"),
    ]


class FlagColours:
    DEFAULT = "default"
    RED = "red"
    YELLOW = "yellow"
    GREEN = "green"
    BLUE = "blue"
    PURPLE = "purple"
    ORANGE = "orange"
    BROWN = "brown"
    TURQUOISE = "turquoise"
    PINK = "pink"

    choices = [
        (DEFAULT, "Default"),
        (RED, "Red"),
        (YELLOW, "Yellow"),
        (GREEN, "Green"),
        (BLUE, "Blue"),
        (PURPLE, "Purple"),
        (ORANGE, "Orange"),
        (BROWN, "Brown"),
        (TURQUOISE, "Turquoise"),
        (PINK, "Pink"),
    ]


class FlagPermissions:
    DEFAULT = "Anyone"
    AUTHORISED_COUNTERSIGNER = "Authorised countersigner"
    HEAD_OF_LICENSING_UNIT_COUNTERSIGNER = "Head of Licensing Unit countersigner"

    choices = [
        (DEFAULT, "Anyone"),
        (AUTHORISED_COUNTERSIGNER, "Authorised countersigner"),
        (HEAD_OF_LICENSING_UNIT_COUNTERSIGNER, "Head of Licensing Unit countersigner"),
    ]

    PERMISSIONS_MAPPING = {
        AUTHORISED_COUNTERSIGNER: GovPermissions.REMOVE_AUTHORISED_COUNTERSIGNER_FLAGS,
        HEAD_OF_LICENSING_UNIT_COUNTERSIGNER: GovPermissions.REMOVE_HEAD_OF_LICENSING_UNIT_FLAGS,
    }


class SystemFlags:
    REFUSAL_FLAG_ID = "00000000-0000-0000-0000-000000000001"
    GOOD_CLC_QUERY_ID = "00000000-0000-0000-0000-000000000002"
    GOOD_PV_GRADING_QUERY_ID = "00000000-0000-0000-0000-000000000003"
    GOOD_NOT_YET_VERIFIED_ID = "00000000-0000-0000-0000-000000000004"
    MILITARY_END_USE_ID = "00000000-0000-0000-0000-000000000005"
    WMD_END_USE_ID = "00000000-0000-0000-0000-000000000006"
    FIREARMS_ID = "00000000-0000-0000-0000-000000000007"
    MARITIME_ANTI_PIRACY_ID = "00000000-0000-0000-0000-000000000008"
    CRYPTOGRAPHIC_ID = "00000000-0000-0000-0000-000000000009"
    MEDIA_ID = "00000000-0000-0000-0000-000000000010"
    CONTINENTAL_ID = "00000000-0000-0000-0000-000000000011"
    DEALER_ID = "00000000-0000-0000-0000-000000000012"
    REFUSAL_FLAG_ID_2 = "00000000-0000-0000-0000-000000000013"
    ENFORCEMENT_CHECK_REQUIRED = "00000000-0000-0000-0000-000000000014"
    NUCLEAR_ID = "00000000-0000-0000-0000-000000000015"
    NAVY_ID = "00000000-0000-0000-0000-000000000016"
    ARMY_ID = "00000000-0000-0000-0000-000000000017"
    AIRFORCE_ID = "00000000-0000-0000-0000-000000000018"
    POLICE_ID = "00000000-0000-0000-0000-000000000019"
    MINISTRY_OF_INTERIOR_ID = "00000000-0000-0000-0000-000000000020"
    OTHER_SECURITY_FORCES_ID = "00000000-0000-0000-0000-000000000021"
    COMPANIES_REQUESTING_NUCL_ID = "00000000-0000-0000-0000-000000000022"
    MARITIME_ANTI_PIRACY_ID_2 = "00000000-0000-0000-0000-000000000023"
    AIRCRAFT_MANUFACTURERS_ID = "00000000-0000-0000-0000-000000000024"
    REGISTERED_FIREARM_DEALER_ID = "00000000-0000-0000-0000-000000000025"
    OIL_AND_GAS_ID = "00000000-0000-0000-0000-000000000026"
    PHARMACEUTICAL_OR_MEDICAL_ID = "00000000-0000-0000-0000-000000000027"
    MEDIA_OR_CONTRACT_ID = "00000000-0000-0000-0000-000000000028"
    PRIVATE_MILITARY_ID = "00000000-0000-0000-0000-000000000029"
    EDUCATION_ID = "00000000-0000-0000-0000-000000000030"
    EXPORTERS_OWN_USE_ID = "00000000-0000-0000-0000-000000000031"
    OTHER_CONTRACT_ID = "00000000-0000-0000-0000-000000000032"
    ENFORCEMENT_END_USER_MATCH = "00000000-0000-0000-0000-000000000033"
    ENFORCEMENT_CONSIGNEE_MATCH = "00000000-0000-0000-0000-000000000034"
    ENFORCEMENT_ULTIMATE_END_USER_MATCH = "00000000-0000-0000-0000-000000000035"
    ENFORCEMENT_THIRD_PARTY_MATCH = "00000000-0000-0000-0000-000000000036"
    ENFORCEMENT_SITE_MATCH = "00000000-0000-0000-0000-000000000037"
    ENFORCEMENT_ORGANISATION_MATCH = "00000000-0000-0000-0000-000000000038"
    SANCTION_UN_SC_MATCH = "00000000-0000-0000-0000-000000000039"
    SANCTION_OFSI_MATCH = "00000000-0000-0000-0000-000000000040"
    SANCTION_UK_MATCH = "00000000-0000-0000-0000-000000000041"
    ADVICE_COMPLETED_ID = "00000000-0000-0000-0000-000000000042"

    list = [
        REFUSAL_FLAG_ID,
        GOOD_CLC_QUERY_ID,
        GOOD_PV_GRADING_QUERY_ID,
        GOOD_NOT_YET_VERIFIED_ID,
        MILITARY_END_USE_ID,
        WMD_END_USE_ID,
        FIREARMS_ID,
        MARITIME_ANTI_PIRACY_ID,
        CRYPTOGRAPHIC_ID,
        MEDIA_ID,
        CONTINENTAL_ID,
        DEALER_ID,
        REFUSAL_FLAG_ID_2,
        ENFORCEMENT_CHECK_REQUIRED,
        NUCLEAR_ID,
        NAVY_ID,
        ARMY_ID,
        AIRFORCE_ID,
        POLICE_ID,
        MINISTRY_OF_INTERIOR_ID,
        OTHER_SECURITY_FORCES_ID,
        COMPANIES_REQUESTING_NUCL_ID,
        MARITIME_ANTI_PIRACY_ID_2,
        AIRCRAFT_MANUFACTURERS_ID,
        REGISTERED_FIREARM_DEALER_ID,
        OIL_AND_GAS_ID,
        PHARMACEUTICAL_OR_MEDICAL_ID,
        MEDIA_OR_CONTRACT_ID,
        PRIVATE_MILITARY_ID,
        EDUCATION_ID,
        EXPORTERS_OWN_USE_ID,
        OTHER_CONTRACT_ID,
        ENFORCEMENT_END_USER_MATCH,
        ENFORCEMENT_CONSIGNEE_MATCH,
        ENFORCEMENT_ULTIMATE_END_USER_MATCH,
        ENFORCEMENT_THIRD_PARTY_MATCH,
        ENFORCEMENT_SITE_MATCH,
        ENFORCEMENT_ORGANISATION_MATCH,
        SANCTION_UN_SC_MATCH,
        SANCTION_OFSI_MATCH,
        SANCTION_UK_MATCH,
        ADVICE_COMPLETED_ID,
    ]
