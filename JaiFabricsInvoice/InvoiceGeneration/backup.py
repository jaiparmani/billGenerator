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
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )


def run_daily_backup():
    """Export the database to Excel and push it (with db.sqlite3) to GitHub.

    Returns a dict describing what happened, so callers (the scheduler,
    or the manual trigger API) can report the outcome.
    """
    logger.info("Daily backup: starting")
    result = {"exported": False, "committed": False, "pushed": False, "message": ""}

    try:
        call_command("export_to_excel", skip_checks=True)
        result["exported"] = True
    except Exception as exc:
        logger.exception("Daily backup: export_to_excel failed")
        result["message"] = f"export_to_excel failed: {exc}"
        return result

    try:
        _run_git("add", ".")

        nothing_changed = subprocess.run(
            ["git", "diff", "--cached", "--quiet"], cwd=REPO_ROOT
        ).returncode == 0
        if nothing_changed:
            logger.info("Daily backup: nothing changed, skipping commit")
            result["message"] = "nothing changed since last backup"
            return result

        timestamp = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
        _run_git("commit", "-m", f"Automatic backup {timestamp}")
        result["committed"] = True

        branch = _run_git("rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
        _run_git("push", "origin", f"HEAD:{branch}")
        result["pushed"] = True
        result["message"] = "pushed successfully"
        logger.info("Daily backup: pushed successfully")
    except subprocess.CalledProcessError as exc:
        logger.error(
            "Daily backup: git step failed: %s\nstdout=%s\nstderr=%s",
            exc.cmd, exc.stdout, exc.stderr,
        )
        result["message"] = f"git {' '.join(exc.cmd[1:])} failed: {exc.stderr}"
    except Exception as exc:
        logger.exception("Daily backup: unexpected error during git step")
        result["message"] = f"unexpected error: {exc}"

    return result
