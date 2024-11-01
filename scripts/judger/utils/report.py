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
  from . import tuoj
  tuoj.report_judge_result(report, judged)
