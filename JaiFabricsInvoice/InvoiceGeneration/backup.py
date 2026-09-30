import logging
import os
import subprocess

from django.conf import settings
from django.core.management import call_command
from django.utils import timezone

logger = logging.getLogger("InvoiceGeneration.backup")

REPO_ROOT = os.path.dirname(settings.BASE_DIR)


def _run_git(*args):
    return subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )


def run_daily_backup():
    """Export the database to Excel and push it (with db.sqlite3) to GitHub."""
    logger.info("Daily backup: starting")

    try:
        call_command("export_to_excel", skip_checks=True)
    except Exception:
        logger.exception("Daily backup: export_to_excel failed")
        return

    try:
        _run_git("add", ".")

        nothing_changed = subprocess.run(
            ["git", "diff", "--cached", "--quiet"], cwd=REPO_ROOT
        ).returncode == 0
        if nothing_changed:
            logger.info("Daily backup: nothing changed, skipping commit")
            return

        timestamp = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
        _run_git("commit", "-m", f"Automatic backup {timestamp}")
        _run_git("push", "origin", "master")
        logger.info("Daily backup: pushed successfully")
    except subprocess.CalledProcessError as exc:
        logger.error(
            "Daily backup: git step failed: %s\nstdout=%s\nstderr=%s",
            exc.cmd, exc.stdout, exc.stderr,
        )
