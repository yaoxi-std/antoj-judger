from enum import IntEnum, auto
from dataclasses import dataclass


class Status(IntEnum):
  Waiting = auto()
  Compiling = auto()
  Running = auto()
  Accepted = auto()
  Skipped = auto()
  PartiallyCorrect = auto()
  OutputLimitExceeded = auto()
  TimeLimitExceeded = auto()
  MemoryLimitExceeded = auto()
  WrongAnswer = auto()
  RuntimeError = auto()
  FileError = auto()
  CompileError = auto()
  SystemError = auto()


def merge_status(x: Status, y: Status) -> Status:
  return x if x > y else y


MAX_DISPLAY_BYTES = 128


@dataclass
class CaseResult:
  status: Status
  score: float
  time: float
  memory: float
  input: str
  output: str
  stdout: str
  stderr: str
  message: str

  def __init__(self, input: str, output: str):
    self.status = Status.Waiting
    self.score = 0
    self.time = 0
    self.memory = 0
    self.input = input
    self.output = output
    self.stdout = ""
    self.stderr = ""
    self.message = ""

  def initialize(self):
    self.status = Status.Running

  def finalize(self, status: Status, score: float, time: float, memory: float, stdout: str, stderr: str, message: str):
    self.status = status
    self.score = score
    self.time = time
    self.memory = memory
    self.stdout = stdout[:MAX_DISPLAY_BYTES]
    self.stderr = stderr[:MAX_DISPLAY_BYTES]
    self.message = message[:MAX_DISPLAY_BYTES]


@dataclass
class SubtaskResult:
  status: Status
  score: float
  max_time: float
  max_memory: float
  total_time: float
  cases: list[CaseResult]

  def __init__(self):
    self.status = Status.Waiting
    self.score = 0
    self.max_time = 0
    self.max_memory = 0
    self.total_time = 0
    self.cases = []

  def initialize(self):
    self.status = Status.Running

  def skip(self):
    self.status = Status.Skipped

  def push(self, new: CaseResult):
    self.cases.append(new)

  def update(self, score: float):
    self.score = score
    self.max_time = max(self.max_time, self.cases[-1].time)
    self.max_memory = max(self.max_memory, self.cases[-1].memory)
    self.total_time += self.cases[-1].time

  def finalize(self):
    status = Status.Accepted
    for case in self.cases:
      status = merge_status(status, case.status)
    self.status = status


@dataclass
class JudgeResult:
  status: Status
  score: float
  message: str
  max_time: float
  max_memory: float
  total_time: float
  subtasks: dict[int, SubtaskResult]

  def __init__(self):
    self.status = Status.Waiting
    self.score = 0
    self.message = ""
    self.max_time = 0
    self.max_memory = 0
    self.total_time = 0
    self.subtasks = {}

  def initialize_compiling(self):
    self.status = Status.Compiling

  def finalize_compiling(self, message: str, status: Status = Status.Waiting):
    self.status = status
    self.message = message[:MAX_DISPLAY_BYTES]

  def initialize_running(self):
    self.status = Status.Running

  def push(self, id: int, subtask: SubtaskResult):
    self.subtasks[id] = subtask

  def update(self, id: int):
    self.score += self.subtasks[id].score
    self.max_time = max(self.max_time, self.subtasks[id].max_time)
    self.max_memory = max(self.max_memory, self.subtasks[id].max_memory)
    self.total_time += self.subtasks[id].total_time

  def finalize_running(self):
    status = Status.Accepted
    for subtask in self.subtasks.values():
      status = merge_status(status, subtask.status)
    self.status = status


judge_task = None
judge_result = None


def initialize_judge_task(task: dict):
  global judge_task
  global judge_result

  judge_task = task
  judge_result = JudgeResult()
  report_judge_result()


def report_judge_result():
  from pprint import pprint
  pprint(judge_result)
