
def compile(name: str, args: list[str] = []) -> list[str]:
  return ["/usr/bin/clang++", "-O2", "-lm", "-DONLINE_JUDGE", "-o", f"{name}.exe", f"{name}.cpp", *args]


def execute(name: str, args: list[str] = []) -> list[str]:
  return [f"./{name}.exe", *args]


def src(name: str) -> str:
  return name + ".cpp"


def exe(name: str) -> str:
  return name + ".exe"
