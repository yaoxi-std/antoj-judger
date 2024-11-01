
def compile(name: str, args: list[str] = []) -> list[str]:
  return ["/usr/bin/mcs", f"{name}.cs", *args]


def execute(name: str, args: list[str] = []) -> list[str]:
  return ["/usr/bin/mono", f"{name}.exe", *args]


def src(name: str) -> str:
  return name + ".cs"


def exe(name: str) -> str:
  return name + ".exe"
