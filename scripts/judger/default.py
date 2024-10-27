import os

import config

from .utils.result import *
from .utils.report import *

from .utils.lang import select_language
from .utils.sandbox import Sandbox

join = os.path.join


def judge(data_path: str, source_path: str, data: dict):
  sandbox = Sandbox()

  judge_task = current_judge_task()
  judge_result = current_judge_result()

  judge_result.initialize_compiling()
  report_judge_result()

  # Step 1: checker compilation

  if data["checker"]["type"] == "default":
    from ..languages import cpp17 as checker
    sandbox.push(
        join(config.CHECKER_PATH, data["checker"]["name"] + ".cpp"), "checker.cpp")
  else:
    checker = select_language(data["checker"]["language"])
    sandbox.push(
        join(data_path, data["checker"]["name"]), checker.src("checker"))

  sandbox.push(config.TESTLIB_PATH, "testlib.h")
  status = sandbox.exec(checker.compile("checker"),
                        stdout="compile.log", stderr="compile.log",
                        time_limit=10, memory_limit=2048).status

  if status != Status.Accepted:
    if status == Status.TimeLimitExceeded:
      message = "Checker compilation time exceeded.\n"
    else:
      message = "Checker compilation failed.\n"

    message += sandbox.read("compile.log")
    judge_result.finalize_compiling(message, status=Status.SystemError)
    return

  sandbox.pull(checker.exe("checker"),
               join(source_path, checker.exe("checker")))
  sandbox.clean()

  # Step 2: code compilation

  lang = judge_task["submitFiles"][0]["language"]

  code = select_language(lang)

  sandbox.push(join(source_path, "code"), code.src("code"))
  for file in data["extraSourceFiles"]:
    if file["language"] == lang:
      sandbox.push(join(data_path, file["name"]), file["dest"])

  status = sandbox.exec(code.compile("code"),
                        stdout="compile.log", stderr="compile.log",
                        time_limit=10, memory_limit=2048).status

  if status != Status.Accepted:
    if status == Status.TimeLimitExceeded:
      message = "Compilation time exceeded.\n"
    else:
      message = "Compilation failed.\n"

    message += sandbox.read("compile.log")
    judge_result.finalize_compiling(message, status=Status.CompileError)
    return

  judge_result.finalize_compiling(sandbox.read("compile.log"))

  sandbox.pull(code.exe("code"), join(source_path, code.exe("code")))
  sandbox.clean()

  report_judge_result()

  # Step 3: test cases execution

  judge_result.initialize_running()
  report_judge_result()

  for subtask in data["subtasks"]:
    id = subtask["id"]
    type = subtask["type"]
    score = subtask["score"]
    depends = subtask["depends"]
    time_limit = subtask["time"]
    memory_limit = subtask["memory"]

    # Step 3.1: initialize subtask result

    subtask_result = SubtaskResult()
    judge_result.push(id, subtask_result)

    # Step 3.2: check if subtask should be skipped

    skip_subtask = False
    for depend in depends:
      if judge_result.subtasks[depend].status != Status.Accepted:
        skip_subtask = True
        break

    if skip_subtask:
      subtask_result.skip()
      report_judge_result()
      continue

    subtask_result.initialize()
    subtask_result.update(score if type == "min" else 0)
    report_judge_result()

    # Step 3.3: judge each test case

    def judge_case(case: dict) -> float:

      # Step 3.3.1: initialize case result

      input = case["input"]
      output = case["output"]

      case_result = CaseResult(input, output)
      case_result.initialize()
      subtask_result.push(case_result)
      report_judge_result()

      # Step 3.3.2: copy input and executable files

      file_in = data["fileIO"]["input"]
      file_out = data["fileIO"]["output"]

      sandbox.push(join(data_path, input), file_in)
      sandbox.push(join(source_path, code.exe("code")), code.exe("code"))

      # Step 3.3.3: execute user code

      r = sandbox.exec(code.execute("code"),
                       stdin=".stdin", stdout=".stdout", stderr=".stderr",
                       time_limit=time_limit, memory_limit=memory_limit)

      # Step 3.3.4: read stdout and stderr

      stderr = ""
      if sandbox.exists(".stderr"):
        stderr = sandbox.read(".stderr")

      if not sandbox.exists(file_out):
        case_result.finalize(Status.FileError, 0,
                             r.time, r.memory, "", stderr, "")
        return 0

      stdout = sandbox.read(file_out)

      sandbox.pull(file_out, os.path.join(source_path, "user_out"))
      sandbox.clean()

      # Step 3.3.5: check if user code executed successfully

      if r.status != Status.Accepted:
        case_result.finalize(r.status, 0, r.time, r.memory,
                             stdout, stderr, r.message)
        return 0

      # Step 3.3.6: copy input, output and answer files

      sandbox.push(join(data_path, input), "input")
      sandbox.push(join(data_path, output), "answer")
      sandbox.push(join(source_path, "code"), "code")
      sandbox.push(join(source_path, "user_out"), "user_out")
      sandbox.push(join(source_path, checker.exe("checker")),
                   checker.exe("checker"))

      # Step 3.3.7: execute checker

      sandbox.exec(checker.execute("checker", ["input", "user_out", "answer"]),
                   stdin=".stdin", stdout=".stdout", stderr=".stderr",
                   time_limit=10, memory_limit=2048)

      # Step 3.3.8: parse checker output

      text = sandbox.read(".stdout")
      message = sandbox.read(".stderr")

      try:
        partial = float(text.strip())
      except:
        case_result.finalize(Status.SystemError, 0, r.time, r.memory,
                             stdout, stderr, "Checker returned non-number score.\n" + text + "\n" + message + "\n")
        return 0

      # Step 3.3.9: finalize case result

      partial = max(0, min(100, partial))

      if partial == 0:
        case_result.finalize(Status.WrongAnswer, 0, r.time, r.memory,
                             stdout, stderr, message)
        return 0
      elif partial == 100:
        case_result.finalize(Status.Accepted, score, r.time, r.memory,
                             stdout, stderr, message)
        return score
      else:
        case_result.finalize(Status.PartiallyCorrect, partial / 100 * score, r.time, r.memory,
                             stdout, stderr, message)
        return partial / 100 * score

    cases = subtask["cases"]

    for case in cases:
      partial = judge_case(case)

      # Step 3.3.10: update subtask result

      if type == "sum":
        subtask_result.update(subtask_result.score + partial / cases.__len__())
      elif type == "min":
        subtask_result.update(min(subtask_result.score, partial))
        if partial == 0:
          break
      elif type == "max":
        subtask_result.update(max(subtask_result.score, partial))

      report_judge_result()

    # Step 3.4: finalize subtask result

    subtask_result.finalize()
    judge_result.update(id)
    report_judge_result()

  # Step 4: finalize judge result

  judge_result.finalize_running()
  report_judge_result()
