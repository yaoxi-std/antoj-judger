import os
import json

from flask import Flask, jsonify, request, send_from_directory
from queue import Queue

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)

judge_queue = Queue()


@app.route("/api/judge/info", methods=["GET"])
def info():
  import scripts
  return jsonify({
      "languages": scripts.LANGUAGES,
      "internal-checkers": scripts.INTERNAL_CHECKERS,
  })


@app.route("/api/judge/task", methods=["GET", "POST"])
def task():
  if judge_queue.empty():
    return jsonify({"id": -1})
  return jsonify(judge_queue.get())


@app.route("/api/judge/report", methods=["POST"])
def report():
  print(json.dumps(request.json, indent=2))
  return jsonify({"status": "success"})


@app.route("/files/<path:filename>")
def server_file(filename):
  try:
    return send_from_directory(BASE_DIR, filename)
  except FileNotFoundError:
    return "File not found", 404


def url_with_md5(path: str) -> dict:
  import config
  from urllib.parse import urljoin
  from scripts.judger.utils.down import calculate_md5
  return {
      "url": urljoin("http://localhost:8010/files/tasks/", path),
      "md5": calculate_md5(os.path.join(config.BASE_DIR, "tests/tasks", path)),
  }


if __name__ == '__main__':
  tasks = [
      {
          "id": 1,
          "data": url_with_md5("default/data.tar"),
          "submitFiles": [{
              "name": "code", "language": "cpp14", **url_with_md5("default/code/1.cpp")
          }],
      },
      {
          "id": 2,
          "data": url_with_md5("default.subtasks/data.tar"),
          "submitFiles": [{
              "name": "code", "language": "cpp17", **url_with_md5("default.subtasks/code/1.cpp")
          }],
      },
      {
          "id": 3,
          "data": url_with_md5("default.subtasks/data.tar"),
          "submitFiles": [{
              "name": "code", "language": "cpp17", **url_with_md5("default.subtasks/code/2.cpp")
          }],
      },
      {
          "id": 4,
          "data": url_with_md5("default.subtasks/data.tar"),
          "submitFiles": [{
              "name": "code", "language": "cpp17", **url_with_md5("default.subtasks/code/3.cpp")
          }],
      },
      {
          "id": 5,
          "data": url_with_md5("default.subtasks/data.tar"),
          "submitFiles": [{
              "name": "code", "language": "cpp17", **url_with_md5("default.subtasks/code/4.cpp")
          }],
      },
      {
          "id": 6,
          "data": url_with_md5("custom/data.tar"),
          "submitFiles": [{
              "name": "code", "language": "cpp17", **url_with_md5("custom/code/1.cpp")
          }],
      },
  ]

  judge_queue.put(tasks[5])

  app.run(port=8010, debug=True)
