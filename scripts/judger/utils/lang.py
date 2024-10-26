def select_language(language: str):
  try:
    import importlib
    from .. import languages
    return importlib.import_module(f".{language}", languages.__package__)
  except ModuleNotFoundError:
    raise Exception(f"Unsupported language: {language}")
