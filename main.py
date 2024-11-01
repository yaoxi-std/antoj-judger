import sys
import json
import time
import signal
import requests
import logging

import config
import scripts

from scripts import judger
from scripts.judger.utils.sandbox import terminate_all


def fetch_info() -> dict:
  r = requests.get(config.INFO_URL)

  if r.status_code != 200:
    raise Exception("Failed to fetch info: " + r.text)

  return r.json()


def fetch_task() -> dict:
  r = requests.post(config.TASK_URL, json={"token": config.WEB_TOKEN})

  if r.status_code != 200:
    raise Exception("Failed to fetch task: " + r.text)

  return r.json()


def judge_task(task: dict):
  logging.info("Fetched task: " + json.dumps(task))

  judger.judge(task)


def main():
  info = fetch_info()

  for lang in info["languages"]:
    if lang not in scripts.LANGUAGES:
      raise Exception(f"Unsupported language: {lang}")

  for checker in info["internal-checkers"]:
    if checker not in scripts.INTERNAL_CHECKERS:
      raise Exception(f"Unsupported internal checker: {checker}")

  idle = 1

  while True:
    task = fetch_task()
    logging.info(task)
    if task["id"] != -1:
      idle = 1
      judge_task(task)
    else:
      time.sleep(idle)
      idle = min(idle * 2, config.JUDGER_IDLE_TIME)


def handle_sigint(signum, frame):
  logging.info("\nSIGINT received. Exiting...")
  terminate_all()
  sys.exit(0)


if __name__ == '__main__':
  signal.signal(signal.SIGINT, handle_sigint)
  signal.signal(signal.SIGTERM, handle_sigint)

  while True:
    try:
      main()
    except Exception as e:
      logging.exception(e)
      logging.error(f"Internal error. Retrying in {
                    config.JUDGER_IDLE_TIME}s...")
      time.sleep(config.JUDGER_IDLE_TIME)
