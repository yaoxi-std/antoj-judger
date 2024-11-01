from . import c


def compile(name: str, args: list[str] = []) -> list[str]:
  return c.compile(name, ["-std=c11", *args])


def execute(name: str, args: list[str] = []) -> list[str]:
  return c.execute(name, args)


def src(name: str) -> str:
  return c.src(name)


def exe(name: str) -> str:
  return c.exe(name)
