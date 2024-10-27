import json
import time
import logging
import requests

import config

from scripts.judger.utils.result import JudgeResult, as_dict


_judge_task = None
_judge_result = None
_last_report_time = None


def initialize_judge_task(task: dict):
  global _judge_task
  global _judge_result
  global _last_report_time

  _judge_task = task
  _judge_result = JudgeResult()
  _last_report_time = None

  report_judge_result()


def current_judge_task() -> dict:
  return _judge_task


def current_judge_result() -> JudgeResult | None:
  return _judge_result


def report_judge_result(report=False, judged=False) -> bool:
  report = report or judged

  logging.debug("Judge Result:", _judge_result)

  global _last_report_time
  current_time = time.time()

  if (not report and _last_report_time and
          current_time - _last_report_time < config.JUDGER_REPORT_TIME):
    return
  _last_report_time = current_time

  payload = {
      "id": _judge_task["id"],
      "token": config.WEB_TOKEN,
      "judged": judged,
      **as_dict(_judge_result),
  }

  logging.info("Report Judge Result: ", json.dumps(payload))

  r = requests.post(config.REPORT_URL, json=payload)

  if r.status_code != 200 or r.json()["status"] != "success":
    logging.error("Failed to report judge result: ", r.text)
    return False

  return True
