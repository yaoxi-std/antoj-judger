from . import cpp


def compile(name: str, args: list[str] = []) -> list[str]:
  return cpp.compile(name, ["-std=c++11", *args])


def execute(name: str, args: list[str] = []) -> list[str]:
  return cpp.execute(name, args)


def src(name: str) -> str:
  return cpp.src(name)


def exe(name: str) -> str:
  return cpp.exe(name)
