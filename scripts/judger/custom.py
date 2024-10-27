import sys
import importlib


def judge(data_path: str, source_path: str, data: dict):
  judger = data["judger"]
  name = __package__ + ".custom_judger"
  spec = importlib.util.spec_from_file_location(name, judger)
  module = importlib.util.module_from_spec(spec)
  sys.modules[name] = module
  spec.loader.exec_module(module)

  try:
    judge = getattr(module, "judge")
    judge(data_path, source_path, data)
  finally:
    del sys.modules[name]
