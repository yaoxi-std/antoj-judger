
def compile(name: str, args: list[str] = []) -> list[str]:
  return ["/usr/bin/javac", f"{name}.java", *args]


def execute(name: str, args: list[str] = []) -> list[str]:
  return ["/usr/bin/java", f"{name}", *args]


def src(name: str) -> str:
  return name + ".java"


def exe(name: str) -> str:
  return name + ".class"
