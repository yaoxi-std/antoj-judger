import logging
import os
import hashlib
import requests
import tarfile

import config


def calculate_md5(path: str) -> str:
  md5 = hashlib.md5()
  with open(path, "rb") as f:
    for chunk in iter(lambda: f.read(4096), b""):
      md5.update(chunk)
  return md5.hexdigest()


def download_file(url: str, path: str):
  r = requests.get(url)
  if r.status_code != 200:
    raise Exception(f"Failed to download file: {r.text}")
  with open(path, "wb") as f:
    f.write(r.content)


def check_and_download_file(url: str, path: str, md5: str, retry=3):
  if os.path.isfile(path) and calculate_md5(path) == md5:
    return

  for _ in range(retry):
    try:
      download_file(url, path)
    except Exception as e:
      logging.error(e)

    if os.path.isfile(path) and calculate_md5(path) == md5:
      return

  raise Exception("Failed to download file")


def extract_tar(tar_path: str, extract_path: str):
  if os.path.exists(extract_path):
    os.removedirs(extract_path)
  os.makedirs(extract_path)

  def filter_func(tarinfo, path):
    return tarinfo

  with tarfile.open(tar_path, "r") as tar:
    for member in tar.getmembers():
      tar.extract(member, path=extract_path, filter=filter_func)


def download_data(data: dict) -> str:
  md5 = data["md5"]
  path = os.path.join(config.DATA_PATH, md5)
  tar_path = os.path.join(config.DATA_PATH, md5 + ".tar")

  if os.path.isfile(tar_path) and calculate_md5(tar_path) == md5 and os.path.isdir(path):
    return path

  check_and_download_file(data["url"], tar_path, md5)

  extract_tar(tar_path, path)

  return path


def download_task(task: dict) -> tuple[str, str]:
  data_path = download_data(task["data"])
  source_path = os.path.join(config.SUBMIT_PATH, str(task["id"]))

  os.makedirs(source_path, exist_ok=True)

  for file in task["submitFiles"]:
    check_and_download_file(file["url"], os.path.join(
        source_path, file["name"]), file["md5"])

  return data_path, source_path
