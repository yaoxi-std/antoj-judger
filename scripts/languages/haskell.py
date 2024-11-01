
def compile(name: str, args: list[str] = []) -> list[str]:
  return ["/usr/bin/ghc", "-o", f"{name}.exe", f"{name}.hs", *args]


def execute(name: str, args: list[str] = []) -> list[str]:
  return [f"./{name}.exe", *args]


def src(name: str) -> str:
  return name + ".hs"


def exe(name: str) -> str:
  return name + ".exe"
