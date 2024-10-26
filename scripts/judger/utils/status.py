
STATUS = ["Skipped", "Accepted", "Partially Correct", "Output Limit Exceeded", "Time Limit Exceeded",
          "Memory Limit Exceeded", "Wrong Answer", "Runtime Error", "File Error", "Compile Error", "System Error"]


def merge_status(x: str, y: str) -> str:
  return x if STATUS.index(x) > STATUS.index(y) else y
