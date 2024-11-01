
def compile(name: str, args: list[str] = []) -> list[str]:
  return ["/usr/bin/python2", "-m", "py_compile", f"{name}.py", *args]


def execute(name: str, args: list[str] = []) -> list[str]:
  return ["/usr/bin/python2", f"{name}.pyc", *args]


def src(name: str) -> str:
  return name + ".py"


def exe(name: str) -> str:
  return name + ".pyc"
