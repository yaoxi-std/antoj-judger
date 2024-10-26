import os
import yaml
import logging

from .utils.down import download_task
from .utils.report import initialize_judge_task, judge_result, report
from .utils.sandbox import terminate_all


def judge(task: dict):
  initialize_judge_task(task)

  data_path, source_path = download_task(task)

  with open(os.path.join(data_path, "data-lock.yaml"), "r") as f:
    data = yaml.load(f, Loader=yaml.FullLoader)

  try:
    # TODO: Implement the judging logic here
    if data["type"] == "default":
      from .default import judge
      judge(data_path, source_path, data)
  except Exception as e:
    logging.error(e)

    judge_result["status"] = "System Error"
    judge_result["score"] = 0
    judge_result["message"] = str(e)

    terminate_all()
    report()


if __name__ == "__main__":
  tasks = [
      {
          "id": 1,
          "data": {
              "url": "http://localhost:8010/files/tasks/default/data.tar",
              "md5": "ab1414741121f23a4e77cde3120c2b0d",
          },
          "submitFiles": [
              {
                  "name": "code",
                  "language": "cpp14",
                  "url": "http://localhost:8010/files/tasks/default/code/1.cpp",
                  "md5": "331ef6828481c062c085da847505745b",
              }
          ],
      },
      {
          "id": 2,
          "data": {
              "url": "http://localhost:8010/files/tasks/default.subtasks/data.tar",
              "md5": "f7d50dd73c83b7f156dac5cf3a02fa70",
          },
          "submitFiles": [
              {
                  "name": "code",
                  "language": "cpp17",
                  "url": "http://localhost:8010/files/tasks/default.subtasks/code/1.cpp",
                  "md5": "46cacc653961751cbf78b89996503628",
              }
          ],
      },
      {
          "id": 3,
          "data": {
              "url": "http://localhost:8010/files/tasks/default.subtasks/data.tar",
              "md5": "f7d50dd73c83b7f156dac5cf3a02fa70",
          },
          "submitFiles": [
              {
                  "name": "code",
                  "language": "cpp17",
                  "url": "http://localhost:8010/files/tasks/default.subtasks/code/2.cpp",
                  "md5": "22c24319ba1d3bcf83d467c54c5eae57",
              }
          ],
      },
      {
          "id": 4,
          "data": {
              "url": "http://localhost:8010/files/tasks/default.subtasks/data.tar",
              "md5": "f7d50dd73c83b7f156dac5cf3a02fa70",
          },
          "submitFiles": [
              {
                  "name": "code",
                  "language": "cpp17",
                  "url": "http://localhost:8010/files/tasks/default.subtasks/code/3.cpp",
                  "md5": "26ffc5d04de7a89858de05dcd980a805",
              }
          ],
      },
  ]

  judge(tasks[0])
