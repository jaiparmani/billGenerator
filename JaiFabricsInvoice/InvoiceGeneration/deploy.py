"""Server-side auto-deploy: git pull + pip install + reload.

Triggered by the deploy-pythonanywhere.yml GitHub Actions workflow on
every push to master, via the token-protected /api/deploy-webhook/
endpoint. Closes the loop that previously required manually running
`git pull` + `pip install` + clicking Reload on PythonAnywhere after
every push.

Reload uses PythonAnywhere's documented trick of touching the app's
WSGI file - their process manager watches its mtime and reloads the
app on change. This works on every plan tier (unlike the official
reload API, which is gated on some plans) and needs no extra secret
beyond the one that already protects this endpoint.
"""

import logging
import os
import subprocess
import sys

from django.conf import settings

logger = logging.getLogger("InvoiceGeneration.deploy")

REPO_ROOT = os.path.dirname(settings.BASE_DIR)
REQUIREMENTS_PATH = os.path.join(settings.BASE_DIR, "requirements.txt")

# Standard PythonAnywhere convention for a <username>.pythonanywhere.com app.
# Override via env var if the actual filename differs.
WSGI_RELOAD_FILE = os.environ.get(
    "PA_WSGI_FILE",
    "/var/www/jaiparmani411_pythonanywhere_com_wsgi.py",
)


def _run(*args):
    return subprocess.run(
        list(args),
        cwd=REPO_ROOT,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )


def run_deploy():
    """Pull latest code, install any new/changed dependencies, reload.

    Returns a dict describing what happened, same shape as backup's
    run_daily_backup(), so the webhook can report the real outcome
    instead of a bare "OK".
    """
    logger.info("Deploy: starting")
    result = {"pulled": False, "pip_installed": False, "reloaded": False, "message": ""}

    try:
        _run("git", "pull", "origin", "master")
        result["pulled"] = True
    except subprocess.CalledProcessError as exc:
        logger.error("Deploy: git pull failed: %s", exc.stderr)
        result["message"] = "git pull failed: {}".format(exc.stderr)
        return result

    try:
        _run(sys.executable, "-m", "pip", "install", "-r", REQUIREMENTS_PATH)
        result["pip_installed"] = True
    except subprocess.CalledProcessError as exc:
        logger.error("Deploy: pip install failed: %s", exc.stderr)
        result["message"] = "pip install failed: {}".format(exc.stderr)
        return result

    try:
        os.utime(WSGI_RELOAD_FILE, None)
        result["reloaded"] = True
        result["message"] = "deployed and reloaded"
        logger.info("Deploy: success")
    except OSError as exc:
        logger.error("Deploy: reload (touch wsgi file) failed: %s", exc)
        result["message"] = (
            "pulled + installed, but reload failed: {} "
            "(check the PA_WSGI_FILE path)".format(exc)
        )

    return result
