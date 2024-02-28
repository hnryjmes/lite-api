from django.db import models


class RecommendationChoiceType(models.TextChoices):
    VERY_SATISFIED = "VERY_SATISFIED", "VERY_SATISFIED"
    SATISFIED = "SATISFIED", "SATISFIED"
    NEITHER = "NEITHER", "NEITHER"
    DISSATISFIED = "DISSATISFIED", "DISSATISFIED"
    VERY_DISSATISFIED = "VERY_DISSATISFIED", "VERY_DISSATISFIED"


class HelpfulGuidanceEnum(models.TextChoices):
    STRONGLY_DISAGREE = "STRONGLY_DISAGREE", "STRONGLY_DISAGREE"
    DISAGREE = "DISAGREE", "DISAGREE"
    NEITHER = "NEITHER", "NEITHER"
    AGREE = "AGREE", "AGREE"
    STRONGLY_AGREE = "STRONGLY_AGREE", "STRONGLY_AGREE"


class UserAccountEnum(models.TextChoices):
    ALREADY_HAD_ACCOUNT = "ALREADY_HAD_ACCOUNT", "ALREADY_HAD_ACCOUNT"
    VERY_DIFFICULT = "VERY_DIFFICULT", "VERY_DIFFICULT"
    DIFFICULT = "DIFFICULT", "DIFFICULT"
    NEITHER = "NEITHER", "NEITHER"
    EASY = "EASY", "EASY"
    VERY_EASY = "VERY_EASY", "VERY_EASY"


class ExperiencedIssueEnum(models.TextChoices):
    NO_ISSUE = "NO_ISSUE", "NO_ISSUE"
    NOT_FIND_LOOKING_FOR = "NOT_FIND_LOOKING_FOR", "NOT_FIND_LOOKING_FOR"
    DIFFICULT_TO_NAVIGATE = "DIFFICULT_TO_NAVIGATE", "DIFFICULT_TO_NAVIGATE"
    SYSTEM_LACKS_FEATURE = "SYSTEM_LACKS_FEATURE", "SYSTEM_LACKS_FEATURE"
    UNABLE_TO_LOAD_REFRESH_ENTER = "UNABLE_TO_LOAD_REFRESH_ENTER", "UNABLE_TO_LOAD_REFRESH_ENTER"
    OTHER = "OTHER", "OTHER"
    SYSTEM_SLOW = "SYSTEM_SLOW", "SYSTEM_SLOW"
    SUBMITTING_APPLICATION_UNCLEAR = "SUBMITTING_APPLICATION_UNCLEAR", "SUBMITTING_APPLICATION_UNCLEAR"


class UserJourney(models.TextChoices):
    BETA_FEEDBACK_BANNER = "BETA_FEEDBACK BANNER", "BETA_FEEDBACK BANNER"
    APPLICATION_SUBMISSION = "APPLICATION_SUBMISSION", "APPLICATION_SUBMISSION"
