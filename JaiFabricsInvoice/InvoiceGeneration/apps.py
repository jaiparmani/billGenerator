import logging
import os
import sys

from django.apps import AppConfig

logger = logging.getLogger("InvoiceGeneration.backup")


class InvoicegenerationConfig(AppConfig):
    name = 'InvoiceGeneration'

    def ready(self):
        argv = sys.argv
        via_manage = bool(argv) and 'manage.py' in argv[0]

        if via_manage and 'runserver' not in argv:
            # migrate, makemigrations, test, shell, export_to_excel, etc.
            return
        if 'runserver' in argv and os.environ.get('RUN_MAIN') != 'true':
            # autoreloader's watcher process, not the actual server
            return

        try:
            from . import scheduler
            scheduler.start()
        except Exception:
            logger.exception("Failed to start the daily backup scheduler")
