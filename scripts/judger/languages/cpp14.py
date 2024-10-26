from . import cpp


def compile(name: str, args: list[str] = []) -> list[str]:
  return cpp.compile(name, ["-std=c++14", *args])


def run(name: str, args: list[str] = []) -> list[str]:
  return cpp.run(name, args)


def source(name: str) -> str:
  return cpp.source(name)


def executable(name: str) -> str:
  return cpp.executable(name)
