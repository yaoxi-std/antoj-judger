from . import cpp_clang


def compile(name: str, args: list[str] = []) -> list[str]:
  return cpp_clang.compile(name, ["-std=c++17", *args])


def execute(name: str, args: list[str] = []) -> list[str]:
  return cpp_clang.execute(name, args)


def src(name: str) -> str:
  return cpp_clang.src(name)


def exe(name: str) -> str:
  return cpp_clang.exe(name)
