
def compile(name: str, args: list[str] = []) -> list[str]:
  return ["gcc", "-O2", "-lm", "-DONLINE_JUDGE", "-o", f"{name}.exe", f"{name}.c", *args]


def run(name: str, args: list[str] = []) -> list[str]:
  return [f"./{name}.exe", *args]


def source(name: str) -> str:
  return name + ".c"


def executable(name: str) -> str:
  return name + ".exe"
