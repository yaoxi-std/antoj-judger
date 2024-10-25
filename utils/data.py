import yaml
from dataclasses import dataclass, field


@dataclass
class Case:
  input: str
  output: str

  def __init__(self, case: dict):
    self.input = case["input"]
    self.output = case["output"]


@dataclass
class Subtask:
  type: str
  score: float
  id: int
  time: float
  memory: float
  depends: list[int]
  cases: list[Case]

  def __init__(self, subtask: dict):
    self.type = subtask["type"]
    self.score = subtask["score"]
    self.id = subtask["id"]
    self.time = float(subtask["time"][:-1])
    self.memory = float(subtask["memory"][:-2])
    self.depends = subtask["depends"]
    self.cases = [Case(x) for x in subtask["cases"]]


@dataclass
class FileIO:
  input: str | None = field(default=None)
  output: str | None = field(default=None)

  def __init__(self, file_io: dict):
    self.input = file_io["input"] if file_io["input"] != "__stdin__" else None
    self.output = file_io["output"] if file_io["output"] != "__stdout__" else None


@dataclass
class Checker:
  type: str
  name: str
  language: str | None = field(default=None)

  def __init__(self, checker: dict):
    self.type = checker["type"]
    self.name = checker["name"]

    if self.type == "custom":
      self.language = checker["language"]


@dataclass
class Submit:
  name: str
  languages: list[str]

  def __init__(self, submit: dict):
    self.name = submit["name"]
    self.languages = submit["languages"]


@dataclass
class Interactor:
  name: str
  language: str

  def __init__(self, interactor: dict):
    self.name = interactor["name"]
    self.language = interactor["language"]


@dataclass
class ExtraSourceFile:
  name: str
  dest: str
  language: str
  compileWithSource: bool


@dataclass
class Data:
  type: str
  time: float
  memory: float
  subtasks: list[Subtask]
  fileIO: FileIO
  checker: Checker
  submits: list[Submit]
  interactor: Interactor | None = field(default=None)
  extraSourceFiles: list[ExtraSourceFile] | None = field(default=None)
  extraJudgerInfo: dict | None = field(default=None)

  def __init__(self, data: dict):
    self.type = data["type"]
    self.time = float(data["time"][:-1])
    self.memory = float(data["memory"][:-2])
    self.subtasks = [Subtask(x) for x in data["subtasks"]]
    self.fileIO = data["fileIO"]
    self.checker = data["checker"]
    self.submits = [Submit(x) for x in data["submits"]]

    if self.type == "interactive":
      self.interactor = Interactor(data["interactor"])

    if self.type in ["default", "interactive", "custom"]:
      self.extraSourceFiles = [
          ExtraSourceFile(x) for x in data["extraSourceFiles"]]

    if self.type == "custom":
      self.extraJudgerInfo = data["extraJudgerInfo"]


def load(path: str) -> Data:
  return Data(yaml.load(open(path, "r"), Loader=yaml.FullLoader))


if __name__ == "__main__":
  import sys
  from pprint import pprint

  if sys.argv.__len__() < 2:
    print("Usage: python3 data.py <data-lock.yaml>")
    sys.exit(1)

  data = load(sys.argv[1])
  pprint(data)
