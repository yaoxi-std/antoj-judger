import os

import config

from .utils.lang import select_language
from .utils.report import judge_task, judge_result, report
from .utils.sandbox import Sandbox
from .utils.status import merge_status

MAX_DISPLAY_BYTES = 128


def judge(data_path: str, source_path: str, data: dict):
  sandbox = Sandbox()

  judge_result["status"] = "Compiling"
  report()

  # Compile checker

  if data["checker"]["type"] == "default":
    from .languages import cpp17
    checker = cpp17
    sandbox.push(os.path.join(config.CHECKER_PATH,
                 data["checker"]["name"] + ".cpp"), "checker.cpp")
  else:
    checker = select_language(data["checker"]["language"])
    sandbox.push(os.path.join(
        data_path, data["checker"]["name"]), checker.source("checker"))

  sandbox.push(config.TESTLIB_PATH, "testlib.h")

  status, _, _, _ = sandbox.exec(checker.compile("checker"),
                                 stdout="compile.log", stderr="compile.log",
                                 time_limit=10, memory_limit=2048)

  if status != "Accepted":
    judge_result["status"] = "System Error"
    judge_result["score"] = 0

    if status == "Time Limit Exceeded":
      judge_result["message"] = "Checker compilation time exceeded.\n"
    judge_result["message"] += sandbox.read("compile.log")

    sandbox.terminate()
    report()
    return

  sandbox.pull(checker.executable("checker"),
               os.path.join(source_path, checker.executable("checker")))
  sandbox.clean()

  # Compile source

  language = select_language(
      lang := judge_task["submitFiles"][0]["language"])

  sandbox.push(os.path.join(source_path, "code"), language.source("code"))
  for file in data["extraSourceFiles"]:
    if file["language"] == lang:
      sandbox.push(os.path.join(data_path, file["name"]), file["dest"])

  status, _, _, _ = sandbox.exec(language.compile("code"),
                                 stdout="compile.log", stderr="compile.log",
                                 time_limit=10, memory_limit=2048)

  if status != "Accepted":
    judge_result["status"] = "Compile Error"
    judge_result["score"] = 0

    if status == "Time Limit Exceeded":
      judge_result["message"] = "Compile Time Limit Exceeded\n"
    judge_result["message"] += sandbox.read("compile.log")

    sandbox.terminate()
    report()
    return

  judge_result["status"] = "Running"
  judge_result["message"] = sandbox.read("compile.log")

  sandbox.pull(language.executable("code"),
               os.path.join(source_path, language.executable("code")))
  sandbox.clean()
  report()

  # Run test cases

  judge_result["subtasks"] = {}
  judge_result["max_time"] = 0
  judge_result["max_memory"] = 0
  judge_result["total_time"] = 0

  for subtask in data["subtasks"]:
    id = subtask["id"]
    type = subtask["type"]
    score = subtask["score"]
    depends = subtask["depends"]
    time_limit = subtask["time"]
    memory_limit = subtask["memory"]

    skip = False
    for depend in depends:
      if judge_result["subtasks"][depend]["status"] != "Accepted":
        skip = True
        break

    if skip:
      judge_result["subtasks"][id] = {
          "status": "Skipped",
          "score": 0,
          "max_time": 0,
          "max_memory": 0,
          "total_time": 0,
      }
      continue

    judge_result["subtasks"][id] = {
        "status": "Running",
        "score": score if type == "min" else 0,
        "max_time": 0,
        "max_memory": 0,
        "total_time": 0,
        "cases": [],
    }

    for case in subtask["cases"]:
      input = data["fileIO"]["input"]
      output = data["fileIO"]["output"]

      sandbox.push(os.path.join(source_path, language.executable("code")),
                   language.executable("code"))

      sandbox.push(os.path.join(data_path, case["input"]), input)

      status, debug, time, memory = sandbox.exec(
          language.run("code"),
          stdin="__stdin__", stdout="__stdout__", stderr="__stderr__",
          time_limit=time_limit, memory_limit=memory_limit)

      result = {
          "status": "",
          "score": 0,
          "time": time,
          "memory": memory,
          "stdout": "",
          "stderr": "",
          "message": "",
      }

      if not sandbox.exists(output):
        status = "File Error"
      else:
        result["stdout"] = sandbox.read(output)[:MAX_DISPLAY_BYTES]

      result["stderr"] = sandbox.read("__stderr__")[:MAX_DISPLAY_BYTES]

      sandbox.pull(output, os.path.join(source_path, "user_out"))
      sandbox.clean()

      judge_result["subtasks"][id]["max_time"] = max(
          judge_result["subtasks"][id]["max_time"], time)
      judge_result["subtasks"][id]["max_memory"] = max(
          judge_result["subtasks"][id]["max_memory"], memory)
      judge_result["subtasks"][id]["total_time"] += time

      judge_result["max_time"] = max(judge_result["max_time"], time)
      judge_result["max_memory"] = max(judge_result["max_memory"], memory)
      judge_result["total_time"] += time

      if status == "Accepted":
        sandbox.push(os.path.join(data_path, case["input"]), "input")
        sandbox.push(os.path.join(source_path, "user_out"), "user_out")
        sandbox.push(os.path.join(data_path, case["output"]), "answer")
        sandbox.push(os.path.join(source_path, "code"), "code")
        sandbox.push(os.path.join(source_path, checker.executable("checker")),
                     checker.executable("checker"))

        sandbox.write("__stdin__", "")

        status, debug, time, memory = sandbox.exec(
            checker.run("checker", ["input", "user_out", "answer"]),
            stdin="__stdin__", stdout="__stdout__", stderr="__stderr__",
            time_limit=10, memory_limit=2048)

        text = sandbox.read("__stdout__").strip()
        result["message"] = sandbox.read("__stderr__")[:MAX_DISPLAY_BYTES]

        try:
          partial = float(text)
          result["score"] = partial / 100 * score

          if partial == 0:
            result["status"] = "Wrong Answer"
          elif partial == 100:
            result["status"] = "Accepted"
          elif 0 < partial < 100:
            result["status"] = "Partially Correct"
          else:
            result["status"] = "System Error"
            result["score"] = 0
            result["message"] = "Checker returned score out of range [0, 100]"

        except ValueError:
          result["status"] = "System Error"
          result["score"] = 0
          result["message"] = "Checker returned non-number score"

      else:
        result["status"] = status
        result["score"] = 0
        result["message"] = debug

      judge_result["subtasks"][id]["cases"].append(result)

      if type == "sum":
        judge_result["subtasks"][id]["score"] += (
            result["score"] / subtask["cases"].__len__())
      elif type == "min":
        judge_result["subtasks"][id]["score"] = min(
            judge_result["subtasks"][id]["score"], result["score"])
      elif type == "max":
        judge_result["subtasks"][id]["score"] = max(
            judge_result["subtasks"][id]["score"], result["score"])
      else:
        raise Exception("Invalid subtask type")

      report()

    judge_result["score"] += judge_result["subtasks"][id]["score"]

    status = "Accepted"
    for subtask in judge_result["subtasks"][id]["cases"]:
      status = merge_status(status, subtask["status"])
    judge_result["subtasks"][id]["status"] = status

    report()

  status = "Accepted"
  for _, subtask in judge_result["subtasks"].items():
    status = merge_status(status, subtask["status"])
  judge_result["status"] = status

  report()
  sandbox.terminate()
