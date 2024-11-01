import logging
import requests

from .report import *
from .result import Status, JudgeResult

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


def report_judge_result(report, judged):
  judge_task = current_judge_task()
  judge_result = current_judge_result()
  results = {}
  
  logging.debug(judge_result)
  
  if judge_result.status == Status.SystemError:
    results["Compilation"] = {
        "status": "System Error",
        "ext_info": {
            "Compilation Info": judge_result.message
        },
        "is_final": judged
    }
  elif judge_result.status == Status.CompileError:
    results["Compilation"] = {
        "status": "Compilation Error",
        "ext_info": {
            "Compilation Info": judge_result.message
        },
        "is_final": judged
    }
  elif judge_result.status not in [Status.Waiting, Status.Compiling]:
    results["Compilation"] = {
        "status": "Compilation Success",
        "ext_info": {
            "Compilation Info": judge_result.message
        },
        "is_final": judged
    }

  for i, subtask in judge_result.subtasks.items():
    results[i] = {
        "status": TUOJ_STATUS[subtask.status],
        "time": subtask.max_time * 1000,
        "memory": subtask.max_memory * 1024,
        "score": subtask.score,
        "ext_info": {
            "Judge Info": "\n".join([f"Case {i + 1}: {TUOJ_STATUS[case.status]} {case.score}" for i, case in enumerate(subtask.cases)])
        },
        "is_final": judged
    }

  frm = {
      "run_id": judge_task["id"],
      "token": config.WEB_TOKEN,
      "results": results
  }
  
  logging.debug(frm)
  
  requests.post(config.REPORT_URL, json=frm)
  
