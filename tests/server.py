import os
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


@app.route("/api/judge/update", methods=["POST"])
def update():
  print(request.json)
  return jsonify({"status": "success"})


@app.route("/files/<path:filename>")
def server_file(filename):
  try:
    print(BASE_DIR)
    return send_from_directory(BASE_DIR, filename)
  except FileNotFoundError:
    return "File not found", 404


if __name__ == '__main__':
  judge_queue.put({
      "id": 1,
      "data": {
          "url": "http://localhost:8010/files/tasks/default/data.tar",
          "md5": "443304a6f6b9efb84b124b516aedcd9a",
      },
      "submitFiles": [
          {
              "name": "code",
              "language": "cpp14",
              "url": "http://localhost:8010/files/tasks/default/code/1.cpp",
              "md5": "7d0b3f3639203209696756d2d2b8f8a8",
          }
      ],
  })

  app.run(port=8010, debug=True)
