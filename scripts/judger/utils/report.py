from scripts.judger.utils.result import JudgeResult


_judge_task = None
_judge_result = None


def initialize_judge_task(task: dict):
  global _judge_task
  global _judge_result

  _judge_task = task
  _judge_result = JudgeResult()
  report_judge_result()


def current_judge_task() -> dict:
  return _judge_task


def current_judge_result() -> JudgeResult | None:
  return _judge_result


def report_judge_result():
  from pprint import pprint
  pprint(_judge_result)
