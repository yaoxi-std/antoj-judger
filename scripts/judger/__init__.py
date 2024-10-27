import os
import yaml
import logging

from .utils import sandbox
from .utils.down import download_task
from .utils.result import Status, initialize_judge_task, judge_result, report_judge_result


def judge(task: dict):
  initialize_judge_task(task)

  data_path, source_path = download_task(task)

  with open(os.path.join(data_path, "data-lock.yaml"), "r") as f:
    data = yaml.load(f, Loader=yaml.FullLoader)

  try:
    # TODO: Implement more judge types
    if data["type"] == "default":
      from .default import judge
      judge(data_path, source_path, data)

  except Exception as e:
    logging.error(e)

    judge_result.score = 0
    judge_result.status = Status.SystemError
    judge_result.message = "System error occurred during judging.\n" + str(e)

  report_judge_result()
  sandbox.terminate_all()


if __name__ == "__main__":
  def url_with_md5(path: str) -> dict:
    import config
    from urllib.parse import urljoin
    from .utils.down import calculate_md5
    return {
        "url": urljoin("http://localhost:8010/files/tasks/", path),
        "md5": calculate_md5(os.path.join(config.BASE_DIR, "tests/tasks", path)),
    }

  tasks = [
      {
          "id": 1,
          "data": url_with_md5("default/data.tar"),
          "submitFiles": [{
              "name": "code",
              "language": "cpp14",
              **url_with_md5("default/code/1.cpp")
          }],
      },
      {
          "id": 2,
          "data": url_with_md5("default.subtasks/data.tar"),
          "submitFiles": [{
              "name": "code",
              "language": "cpp17",
              **url_with_md5("default.subtasks/code/1.cpp")
          }],
      },
      {
          "id": 3,
          "data": url_with_md5("default.subtasks/data.tar"),
          "submitFiles": [{
              "name": "code",
              "language": "cpp17",
              **url_with_md5("default.subtasks/code/2.cpp")
          }],
      },
      {
          "id": 4,
          "data": url_with_md5("default.subtasks/data.tar"),
          "submitFiles": [{
              "name": "code",
              "language": "cpp17",
              **url_with_md5("default.subtasks/code/3.cpp")
          }],
      },
      {
          "id": 5,
          "data": url_with_md5("default.subtasks/data.tar"),
          "submitFiles": [{
              "name": "code",
              "language": "cpp17",
              **url_with_md5("default.subtasks/code/4.cpp")
          }],
      },
  ]

  import sys
  judge(tasks[int(sys.argv[1])])
