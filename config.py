import os
from urllib.parse import urljoin

DEBUG = os.getenv("DEBUG", "false") == "true"

WEB_HOST = os.getenv("WEB_HOST", "http://localhost:8010")
WEB_TOKEN = os.getenv("WEB_TOKEN", "MyRatingIs1064")

INFO_URL = urljoin(WEB_HOST, "/api/judge/info")
FETCH_URL = urljoin(WEB_HOST, "/api/judge/task")
UPDATE_URL = urljoin(WEB_HOST, "/api/judge/update")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TMP_PATH = os.getenv("TMP_DIR", os.path.join(BASE_DIR, "tmp"))
DATA_PATH = os.getenv("DATA_PATH", os.path.join(BASE_DIR, "data"))

TESTLIB_PATH = os.getenv("TESTLIB_PATH", os.path.join(BASE_DIR, "scripts", "testlib.h"))
CHECKER_PATH = os.getenv("CHECKER_PATH", os.path.join(BASE_DIR, "scripts", "checker"))

SUBMIT_PATH = os.getenv(
    "SUBMIT_PATH", os.path.join(TMP_PATH, "submit"))
SANDBOX_DATA_PATH = os.getenv(
    "SANDBOX_DATA_PATH", os.path.join(TMP_PATH, "sandbox"))
HOST_SANDBOX_DATA_PATH = os.getenv("HOST_SANDBOX_DATA_PATH", SANDBOX_DATA_PATH)

JUDGER_IDLE_TIME = 5

if not os.path.exists(TMP_PATH):
  os.makedirs(TMP_PATH)
if not os.path.exists(DATA_PATH):
  os.makedirs(DATA_PATH)

print(f"WEB_HOST: {WEB_HOST}")
print(f"WEB_TOKEN: {WEB_TOKEN}")