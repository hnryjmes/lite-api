import logging

from rest_framework import serializers

from conf.settings import BACKGROUND_TASK_ENABLED
from documents.tasks import scan_document_for_viruses


def process_document(document):
    if BACKGROUND_TASK_ENABLED:
        scan_document_for_viruses(str(document.id))
    else:
        try:
            scan_document_for_viruses.now(str(document.id))
        except Exception as e:
            logging.error(e)
            raise serializers.ValidationError({"document": e})
