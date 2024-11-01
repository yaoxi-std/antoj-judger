
def compile(name: str, args: list[str] = []) -> list[str]:
  return ["/usr/bin/python3", "-m", "py_compile", f"{name}.py", *args,
          "&&", "cp", f"__pycache__/{name}.cpython-38.pyc", f"{name}.pyc"]


def execute(name: str, args: list[str] = []) -> list[str]:
  return ["/usr/bin/python3", f"{name}.pyc", *args]


def src(name: str) -> str:
  return name + ".py"


def exe(name: str) -> str:
  return name + ".pyc"
