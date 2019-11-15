from uuid import UUID


class Permissions:
    MANAGE_FINAL_ADVICE = "MANAGE_FINAL_ADVICE"
    MANAGE_TEAM_ADVICE = "MANAGE_TEAM_ADVICE"
    REVIEW_GOODS = "REVIEW_GOODS"
    ADMINISTER_ROLES = "ADMINISTER_ROLES"


class Roles:
    DEFAULT_ROLE_ID = UUID("00000000-0000-0000-0000-000000000001")
    SUPER_USER_ROLE_ID = UUID("00000000-0000-0000-0000-000000000002")
