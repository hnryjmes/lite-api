from rest_framework.test import APITestCase

from health_check.exceptions import HealthCheckException

from api.document_data.health_checks import BackupDocumentDataHealthCheckBackend
from api.document_data.models import BackupLog


class TestBackupDocumentDataHealthcheckBackend(APITestCase):
    def setUp(self):
        super().setUp()

        self.backend = BackupDocumentDataHealthCheckBackend()

    def test_backup_document_data_healthcheck_no_backup_log(self):
        self.assertEqual(BackupLog.objects.count(), 0)
        self.assertIsNone(self.backend.check_status())

    # def test_backup_document_data_healthcheck_backend_not_run(self):
    #     with self.assertRaises(HealthCheckException) as exc:
    #         backend.check_status()
    #         self.assertEqual(exc.message_type, "backup document error")
    #         self.assertEqual(exc.message, "Backup not run today")
