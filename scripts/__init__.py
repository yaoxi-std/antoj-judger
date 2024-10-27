import os

from config import BASE_DIR, CHECKER_PATH

LANGUAGES = []

for item in os.listdir(os.path.join(BASE_DIR, "scripts/languages")):
  if item.endswith(".py"):
    LANGUAGES.append(item[:-3])

INTERNAL_CHECKERS = []

for item in os.listdir(CHECKER_PATH):
  if item.endswith(".cpp"):
    INTERNAL_CHECKERS.append(item[:-4])
