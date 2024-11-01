import os
import logging
from urllib.parse import urljoin

DEBUG = os.getenv("DEBUG", "false") == "true"

if DEBUG:
  logging.basicConfig(level=logging.DEBUG)

WEB_HOST = os.getenv("WEB_HOST", "http://localhost:8010")
WEB_TOKEN = os.getenv("WEB_TOKEN", "farfarfaraway")

INFO_URL = urljoin(WEB_HOST, "/api/judge/info")
TASK_URL = urljoin(WEB_HOST, "/api/judge/task")
REPORT_URL = urljoin(WEB_HOST, "/api/judge/report")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TMP_PATH = os.getenv("TMP_DIR", os.path.join(BASE_DIR, "tmp"))
DATA_PATH = os.getenv("DATA_PATH", os.path.join(BASE_DIR, "data"))

TESTLIB_PATH = os.getenv("TESTLIB_PATH", os.path.join(BASE_DIR, "include", "testlib.h"))
CHECKER_PATH = os.getenv("CHECKER_PATH", os.path.join(BASE_DIR, "scripts", "checker"))

SUBMIT_PATH = os.getenv(
    "SUBMIT_PATH", os.path.join(TMP_PATH, "submit"))
SANDBOX_DATA_PATH = os.getenv(
    "SANDBOX_DATA_PATH", os.path.join(TMP_PATH, "sandbox"))
HOST_SANDBOX_DATA_PATH = os.getenv("HOST_SANDBOX_DATA_PATH", SANDBOX_DATA_PATH)

JUDGER_IDLE_TIME = float(os.getenv("JUDGER_IDLE_TIME", 5))
JUDGER_REPORT_TIME = float(os.getenv("JUDGER_REPORT_TIME", 1))

ALLOW_CUSTOM_JUDGER = os.getenv("ALLOW_CUSTOM_JUDGER", "false") == "true" or DEBUG

if not os.path.exists(TMP_PATH):
  os.makedirs(TMP_PATH)
if not os.path.exists(DATA_PATH):
  os.makedirs(DATA_PATH)

logging.info(f"WEB_HOST: {WEB_HOST}")
logging.info(f"WEB_TOKEN: {WEB_TOKEN}")
