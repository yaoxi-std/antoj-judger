from flask import Flask, jsonify, request
from queue import Queue

app = Flask(__name__)

judge_queue = Queue()


@app.route("/api/judge/get_task", methods=["GET", "POST"])
def get_task():
  if judge_queue.empty():
    return jsonify({"id": -1})
  return jsonify(judge_queue.get())


@app.route("/api/judge/update_results", methods=["POST"])
def update_results():
  print(request.json)
  return jsonify({"status": "success"})


if __name__ == '__main__':
  app.run(port=8011, debug=True)
