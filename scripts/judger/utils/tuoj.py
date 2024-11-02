import logging
import requests

from .report import *
from .result import Status, CaseResult

TUOJ_STATUS = {
    Status.Waiting: "Waiting",
    Status.Compiling: "Running",
    Status.Running: "Running",
    Status.Accepted: "Accepted",
    Status.Skipped: "Skipped",
    Status.PartiallyCorrect: "Partially Correct",
    Status.OutputLimitExceeded: "Time Limit Exceeded",
    Status.TimeLimitExceeded: "Time Limit Exceeded",
    Status.MemoryLimitExceeded: "Memory Limit Exceeded",
    Status.WrongAnswer: "Wrong Answer",
    Status.RuntimeError: "Runtime Error",
    Status.FileError: "Runtime Error",
    Status.CompileError: "Compilation Error",
    Status.SystemError: "System Error",
}

SHORT_STATUS = {
    Status.Waiting: "?",
    Status.Compiling: "?",
    Status.Running: "?",
    Status.Accepted: "*",
    Status.Skipped: "-",
    Status.PartiallyCorrect: "p",
    Status.OutputLimitExceeded: "o",
    Status.TimeLimitExceeded: "t",
    Status.MemoryLimitExceeded: "m",
    Status.WrongAnswer: "x",
    Status.RuntimeError: "!",
    Status.FileError: "!",
    Status.SystemError: "?",
}


def parse_ext_info(cases: list[CaseResult]):
  return "".join([f"{SHORT_STATUS[case.status]}" for case in cases])


def report_judge_result(report, judged):
  judge_task = current_judge_task()
  judge_result = current_judge_result()
  results = {}

  logging.debug(judge_result)

  if judge_result.status in [Status.SystemError, Status.CompileError]:
    results["Compilation"] = {
        "status": TUOJ_STATUS[judge_result.status],
        "ext_info": judge_result.message,
        "is_final": judged
    }
  elif judge_result.status not in [Status.Waiting, Status.Compiling]:
    results["Compilation"] = {
        "status": "Compilation Success",
        "ext_info": judge_result.message,
        "is_final": judged
    }

  max_case = 0
  running_case = 0

  for i, subtask in judge_result.subtasks.items():
    max_case = max(max_case, i)
    if subtask.status == Status.Running:
      running_case = i
    results[i] = {
        "status": TUOJ_STATUS[subtask.status],
        "time": subtask.max_time * 1000,
        "memory": subtask.max_memory * 1024,
        "score": subtask.score,
        "ext_info": parse_ext_info(subtask.cases),
        "is_final": judged
    }

  if judge_result.status == Status.Running:
    status = f"Running on case {running_case or (max_case + 1)}"
  else:
    status = TUOJ_STATUS[judge_result.status]

  frm = {
      "run_id": judge_task["id"],
      "token": config.WEB_TOKEN,
      "status":  status,
      "results": results
  }

  logging.debug(frm)

  requests.post(config.REPORT_URL, json=frm)
