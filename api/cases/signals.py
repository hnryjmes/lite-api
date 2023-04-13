from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from api.applications.notify import notify_caseworker_countersign_return
from api.cases.models import Case
from api.staticdata.statuses.enums import CaseStatusEnum
from api.staticdata.statuses.libraries.get_case_status import get_case_status_by_status
from api.workflow.flagging_rules_automation import apply_flagging_rules_to_case


@receiver(post_save, sender=Case)
def case_post_save_handler(sender, instance, raw=False, **kwargs):
    if not settings.FEATURE_C5_ROUTING_ENABLED:
        return

    if raw:
        return

    if not instance.id:
        return

    status_changed = instance._previous_status != instance.status
    status_draft = instance.status == get_case_status_by_status(CaseStatusEnum.DRAFT)
    new_status_terminal = instance.status.is_terminal
    if status_changed and not status_draft and not new_status_terminal:
        apply_flagging_rules_to_case(instance)
        _check_for_countersign_rejection(instance)
    instance._previous_status = instance.status


def _check_for_countersign_rejection(case):
    if (
        settings.FEATURE_COUNTERSIGN_ROUTING_ENABLED
        and case.status.status == CaseStatusEnum.UNDER_FINAL_REVIEW
        and case._previous_status.status == CaseStatusEnum.FINAL_REVIEW_SECOND_COUNTERSIGN
    ):
        # send notification as advice has been rejected by countersigner
        notify_caseworker_countersign_return(case)
