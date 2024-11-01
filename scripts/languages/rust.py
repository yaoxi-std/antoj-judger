
def compile(name: str, args: list[str] = []) -> list[str]:
  return ["/usr/bin/rustc", "-o", f"{name}.exe", f"{name}.rs", *args]


def execute(name: str, args: list[str] = []) -> list[str]:
  return [f"./{name}.exe", *args]


def src(name: str) -> str:
  return name + ".rs"


def exe(name: str) -> str:
  return name + ".exe"
