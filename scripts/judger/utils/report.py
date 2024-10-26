
judge_task = None
judge_result = None


def initialize_judge_task(task: dict):
  global judge_task
  global judge_result

  judge_task = task
  judge_result = {
      "id": task["id"],
      "status": "Pending",
      "score": 0,
      "message": "",
  }
  report()


def report():
  from pprint import pprint
  pprint(judge_result)
