import logging
from typing import Optional

from gov_notify.payloads import EmailData
from api.core.celery_tasks import send_email as celery_send_email


def send_email(email_address, template_type, data: Optional[EmailData] = None):
    """
    Send an email using the gov notify service via celery.
    """
    data = data.as_dict() if data else None
    logging.info("sending email via celery")
    return celery_send_email.apply_async([email_address, template_type.template_id, data])
