
def compile(name: str, args: list[str] = []) -> list[str]:
  return ["gcc", "-O2", "-lm", "-DONLINE_JUDGE", "-o", f"{name}.exe", f"{name}.c", *args]


def execute(name: str, args: list[str] = []) -> list[str]:
  return [f"./{name}.exe", *args]


def src(name: str) -> str:
  return name + ".c"


def exe(name: str) -> str:
  return name + ".exe"
