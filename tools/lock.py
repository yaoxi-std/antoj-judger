#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import yaml

DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(DIR, "../defaults/data.yaml"), "r") as f:
  DATA_YAML_DEFAULT: dict = yaml.load(f, Loader=yaml.FullLoader) or {}

INTERNAL_CHECKERS = ["fcmp", "hcmp", "lcmp", "ncmp",
                     "nyesno", "rcmp4", "rcmp6", "rcmp9", "wcmp", "yesno"]

LANGUAGES = ["c", "c11", "cpp", "cpp11", "cpp14", "cpp17",
             "cpp-clang", "cpp11-clang", "cpp14-clang", "cpp17-clang",
             "csharp", "haskell", "java", "nodejs", "python2", "python3", "rust"]


def lock(data: dict, base_dir: str) -> dict:

  def parse_type(type: str) -> str:
    type = str(type)
    if type not in ["default", "interactive", "submit-answer", "objective", "custom"]:
      raise ValueError(f"Invalid type: {type}")
    return type

  def parse_time(time: str) -> float:
    time = str(time)
    if time.endswith("ms"):
      return float(time[:-2]) / 1000
    elif time.endswith("s"):
      return float(time[:-1])
    else:
      raise ValueError(f"Invalid time format: `{time}`")

  def parse_memory(memory: str) -> float:
    def with_suffix(s: str, suffix: str) -> bool:
      return s.lower().endswith(suffix.lower())

    memory = str(memory)

    if with_suffix(memory, "KB"):
      return float(memory[:-2]) / 1024
    elif with_suffix(memory, "MB"):
      return float(memory[:-2])
    elif with_suffix(memory, "GB"):
      return float(memory[:-2]) * 1024
    elif with_suffix(memory, "k"):
      return float(memory[:-1]) / 1024
    elif with_suffix(memory, "m"):
      return float(memory[:-1])
    elif with_suffix(memory, "g"):
      return float(memory[:-1]) * 1024
    else:
      raise ValueError(f"Invalid memory format: `{memory}`")

  def parse_case(case: int | str | dict) -> list:
    def isregexp(s: str) -> bool:
      return s.__len__() >= 2 and s.startswith("/") and s.endswith("/")

    def parse_regexp(input: str, output: str) -> list:
      mapping = {}

      input_regexp = re.compile(input)
      output_regexp = re.compile(output)

      for file in os.listdir(base_dir):
        if not os.path.isfile(os.path.join(base_dir, file)):
          continue

        if match := input_regexp.match(file):
          key = match.groups()
          if key not in mapping:
            mapping[key] = {}
          if "input" not in mapping[key]:
            mapping[key]["input"] = file
          else:
            raise ValueError(
                f"Multiple input files for the same tuple: {key}")

        if match := output_regexp.match(file):
          key = match.groups()
          if key not in mapping:
            mapping[key] = {}
          if "output" not in mapping[key]:
            mapping[key]["output"] = file
          else:
            raise ValueError(
                f"Multiple output files for the same tuple: {key}")

      result = []
      for _, value in mapping.items():
        if "input" in value and "output" in value:
          result.append(value)

      def natural_key(s: str):
        return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]

      return sorted(result, key=lambda x: (natural_key(x["input"]), natural_key(x["output"])))

    def unwrap_regexp(s: str) -> str:
      return s[1:-1]

    if isinstance(case, int):
      case = str(case)

    if isinstance(case, str):
      input_file = str(data["inputFile"])
      output_file = str(data["outputFile"])

      if isregexp(case):
        input = input_file.replace("#", f"({unwrap_regexp(case)})")
        output = output_file.replace("#", f"({unwrap_regexp(case)})")
        return parse_regexp(input, output)

      input = input_file.replace("#", case)
      output = output_file.replace("#", case)

    elif isinstance(case, dict):
      input = str(case["input"])
      output = str(case["output"])

      if isregexp(input) and isregexp(output):
        return parse_regexp(unwrap_regexp(input), unwrap_regexp(output))

    else:
      raise ValueError("Invalid case format")

    if not os.path.isfile(os.path.join(base_dir, input)):
      raise ValueError(f"Input file not found: {input}")
    if not os.path.isfile(os.path.join(base_dir, output)):
      raise ValueError(f"Output file not found: {output}")

    return [{
        "input": input,
        "output": output,
    }]

  def parse_subtasks(subtasks: list) -> list:
    subid = 0
    subid_used = []
    subtasks_locked = []
    total_score = 0

    time_default = parse_time(data["time"])
    memory_default = parse_memory(data["memory"])

    for subtask in subtasks:
      subid += 1
      time = time_default
      memory = memory_default

      type = str(subtask["type"])
      if type not in ["sum", "min", "max"]:
        raise ValueError(f"Invalid subtask type: {type}")

      score = float(subtask["score"])
      if score < 0 or score > 100:
        raise ValueError(f"Invalid subtask score: {score}")

      total_score += score

      if "id" in subtask:
        newid = int(subtask["id"])
        if newid < subid:
          raise ValueError(
              f"Invalid subtask id: {newid} (expected > {subid} (ascending))")
        subid = newid

      if "time" in subtask:
        time = parse_time(subtask["time"])

      if "memory" in subtask:
        memory = parse_memory(subtask["memory"])

      depends = []
      if "depends" in subtask:
        for depend in subtask["depends"]:
          depend = int(depend)
          if depend not in subid_used:
            raise ValueError(f"Invalid dependency: {depend}")
          depends.append(depend)

      subid_used.append(subid)

      cases = []
      for case in subtask["cases"]:
        cases.extend(parse_case(case))

      if cases.__len__() == 0:
        raise ValueError(f"No cases found for subtask {subid}")

      subtasks_locked.append({
          "type": type,
          "score": score,
          "id": subid,
          "time": time,
          "memory": memory,
          "depends": depends,
          "cases": cases,
      })

    type = parse_type(data["type"])

    if total_score != 100 and type not in ["objective", "custom"]:
      raise ValueError(f"Total score of subtasks is not 100: {total_score}")

    return subtasks_locked

  def parse_file_io(file_io: dict) -> dict:
    file_io_locked = {}

    if "input" in file_io:
      file_io_locked["input"] = file_io["input"]
    else:
      file_io_locked["input"] = ".stdin"

    if "output" in file_io:
      file_io_locked["output"] = file_io["output"]
    else:
      file_io_locked["output"] = ".stdout"

    return file_io_locked

  def parse_checker(checker: str) -> str:
    type = str(checker["type"])

    if type == "default":
      name = str(checker["name"])

      if name not in INTERNAL_CHECKERS:
        raise ValueError(f"Invalid checker name: {name}")

      return {
          "type": "default",
          "name": name,
      }

    elif type == "custom":
      name = str(checker["name"])
      language = str(checker["language"])

      if not os.path.isfile(os.path.join(base_dir, name)):
        raise ValueError(f"Checker file not found: {name}")

      if language not in LANGUAGES:
        raise ValueError(f"Invalid checker language: {language}")

      return {
          "type": "custom",
          "name": name,
          "language": language,
      }

    else:
      raise ValueError(f"Invalid checker type: {type}")

  def parse_interactor(interactor: dict) -> dict:
    name = str(interactor["name"])
    language = str(interactor["language"])

    if not os.path.isfile(os.path.join(base_dir, name)):
      raise ValueError(f"Interactor file not found: {name}")

    if language not in LANGUAGES:
      raise ValueError(f"Invalid checker language: {language}")

    return {
        "name": name,
        "language": language,
    }

  def parse_extra(extra: list) -> list:
    extra_locked = []

    for file in extra:
      if not isinstance(file, dict):
        raise ValueError("Invalid extra source file format")

      name = str(file["name"])
      dest = str(file["dest"])
      language = str(file["language"])

      if not os.path.isfile(os.path.join(base_dir, name)):
        raise ValueError(f"Extra file not found: {name}")

      if language not in LANGUAGES:
        raise ValueError(f"Invalid extra source file language: {language}")

      extra_locked.append({
          "name": name,
          "dest": dest,
          "language": language,
      })

    return extra_locked

  def parse_languages(type: str, languages: list | None) -> list:
    if type in ["default", "interactive"]:
      available_langs = LANGUAGES
    elif type == "objective":
      available_langs = ["text"]
    elif type == "submit-answer":
      available_langs = ["zip"]
    elif type == "custom":
      available_langs = [*LANGUAGES, "text", "zip", "binary"]
    else:
      raise ValueError(f"Invalid type: {type}")

    if not languages:
      return available_langs

    locked_langs = []
    for lang in languages:
      if lang not in available_langs:
        raise ValueError(f"Invalid language: {lang}")
      locked_langs.append(lang)

    return locked_langs

  def parse_submit(submit_files: list) -> list:
    if submit_files.__len__() < 1:
      raise ValueError("Submit list is empty")

    type = parse_type(data["type"])
    if submit_files.__len__() > 1 and type != "custom":
      raise ValueError(
          "Multiple submit files are only allowed for custom type")

    names = set()
    submit_files_locked = []
    languages = parse_languages(type, data.get("languages"))

    for sub in submit_files:
      name = str(sub["name"])
      if type != "custom" and name != "code":
        raise ValueError("Invalid submit file name: {name} (should be `code`)")

      submit_langs = languages

      if name in names:
        raise ValueError(f"Duplicate submit file name: {name}")
      names.add(name)

      if "languages" in sub:
        submit_langs = parse_languages(type, sub["languages"])

      submit_files_locked.append({
          "name": name,
          "languages": submit_langs,
      })

    return submit_files_locked

  data = DATA_YAML_DEFAULT | data

  locked = {
      "type": parse_type(data["type"]),
      "time": parse_time(data["time"]),
      "memory": parse_memory(data["memory"]),
      "subtasks": parse_subtasks(data["subtasks"]),
      "fileIO": parse_file_io(data["fileIO"]),
      "checker": parse_checker(data["checker"]),
  }

  if locked["type"] in ["default", "interactive"]:
    if "submitFiles" in data:
      raise ValueError(
          f"Submit files are not allowed for {locked['type']} type")
    locked["submitFiles"] = [{
        "name": "code",
        "languages": parse_languages(locked["type"], data.get("languages")),
    }]
    locked["extraSourceFiles"] = parse_extra(data.get("extraSourceFiles", []))

    if locked["type"] == "interactive":
      locked["interactor"] = parse_interactor(data["interactor"])

  elif locked["type"] in ["submit-answer", "objective"]:
    if "submitFiles" in data:
      raise ValueError(
          f"Submit files are not allowed for {locked['type']} type")
    locked["submitFiles"] = [{
        "name": "answer",
        "languages": ["zip" if locked["type"] == "submit-answer" else "text"],
    }]
    if "extraSourceFiles" in data:
      raise ValueError(
          f"Extra source files are not allowed for {locked['type']} type")
    locked["extraSourceFiles"] = []

  else:
    if "submitFiles" in data:
      locked["submitFiles"] = parse_submit(data["submitFiles"])
    else:
      locked["submitFiles"] = [{
          "name": "code",
          "languages": parse_languages(locked["type"], data.get("languages")),
      }]
    locked["extraSourceFiles"] = parse_extra(data.get("extraSourceFiles", []))
    locked["extraJudgerInfo"] = data.get("extraJudgerInfo", {})

    judger = data.get("judger", "judger.py")
    if not os.path.isfile(os.path.join(base_dir, judger)):
      raise ValueError(f"Judger file not found: {judger}")
    locked["judger"] = judger

  return locked


def update_lock(base_dir: str, data_yaml_path: str | None = None, data_lock_path: str | None = None):
  if not data_yaml_path:
    data_yaml_path = os.path.join(base_dir, "data.yaml")

    if not os.path.isfile(data_yaml_path):
      data_yaml_path = os.path.join(base_dir, "data.yml")

  if not data_lock_path:
    data_lock_path = os.path.join(base_dir, "data-lock.yaml")

  data_yaml = {}

  if os.path.isfile(data_yaml_path):
    with open(data_yaml_path, "r") as f:
      data_yaml = yaml.load(f, Loader=yaml.FullLoader) or {}

  data_locked = lock(data_yaml, base_dir)

  with open(data_lock_path, "w") as f:
    f.write(yaml.dump(data_locked))


if __name__ == "__main__":
  import sys

  if sys.argv.__len__() < 2 or sys.argv[1] in ["-h", "--help"]:
    print(
        "Usage: python3 lock.py <base_dir> [<data_yaml_path>] [<data_lock_path>]")
    sys.exit(1)

  base_dir = sys.argv[1]
  data_yaml_path = sys.argv.__len__() > 2 and sys.argv[2]
  data_lock_path = sys.argv.__len__() > 3 and sys.argv[3]

  try:
    update_lock(base_dir,
                data_yaml_path=data_yaml_path,
                data_lock_path=data_lock_path)
  except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
