
def compile(name: str, args: list[str] = []) -> list[str]:
  return ["echo", ">", "/dev/null"]


def execute(name: str, args: list[str] = []) -> list[str]:
  return ["/usr/bin/node", f"{name}.js", *args]


def src(name: str) -> str:
  return name + ".js"


def exe(name: str) -> str:
  return name + ".js"
