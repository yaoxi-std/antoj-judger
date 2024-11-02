import os
import yaml
import logging

from .utils.report import *

from .utils import sandbox
from .utils.down import download_task
from .utils.result import Status


def judge(task: dict):
  initialize_judge_task(task)

  judge_result = current_judge_result()

  data_path, source_path = download_task(task)

  with open(os.path.join(data_path, "data-lock.yaml"), "r") as f:
    data = yaml.load(f, Loader=yaml.FullLoader)

  try:
    if data["type"] == "default":
      from .default import judge
      judge(data_path, source_path, data)
    elif data["type"] == "interactive":
      from .interactive import judge
      judge(data_path, source_path, data)
    elif data["type"] == "submit-answer":
      from .submit_answer import judge
      judge(data_path, source_path, data)
    elif data["type"] == "objective":
      from .objective import judge
      judge(data_path, source_path, data)
    elif data["type"] == "custom":
      from .custom import judge
      judge(data_path, source_path, data)
    else:
      judge_result.score = 0
      judge_result.status = Status.SystemError
      judge_result.message = "Unknown judge type: " + data["type"]

  except Exception as e:
    logging.error(e)

    judge_result.score = 0
    judge_result.status = Status.SystemError
    judge_result.message = "System error occurred during judging.\n" + str(e)

  report_judge_result(report=True, judged=True)
