
def compile(name: str, args: list[str] = []) -> list[str]:
  return ["g++", "-O2", "-lm", "-DONLINE_JUDGE", "-o", f"{name}.exe", f"{name}.cpp", *args]


def run(name: str, args: list[str] = []) -> list[str]:
  return [f"./{name}.exe", *args]


def source(name: str) -> str:
  return name + ".cpp"


def executable(name: str) -> str:
  return name + ".exe"
