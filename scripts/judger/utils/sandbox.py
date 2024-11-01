import os
import uuid
import shutil
import logging

import config

from collections import namedtuple

from scripts.judger.utils.result import Status

_instances = set()


def quote(s):
  import json
  return json.dumps(s)


class Sandbox:
  def __init__(self, cpus=1, memory="2g", container_prefix="sandbox_"):
    self.id = uuid.uuid4().hex
    self.cpus = cpus
    self.memory = memory
    self.container_name = container_prefix + self.id

    self.base_dir = os.path.join(
        config.SANDBOX_DATA_PATH, self.container_name)
    self.host_dir = os.path.join(
        config.HOST_SANDBOX_DATA_PATH, self.container_name)

    os.makedirs(self.base_dir, exist_ok=True)

    self.exec_host([
        "> /dev/null",
        "docker", "run",
        "--cpus", self.cpus,
        "--memory", self.memory,
        "--network", "none",
        "--name", self.container_name,
        "--volume", f"\"{self.host_dir}\":/sandbox",
        "-d", "--rm",
        "antoj-sandbox",
        "/bin/sh", "-c",
        "\"while true; do sleep 1; done\""
    ])

    _instances.add(self)

    if config.DEBUG:
      logging.info(f"Container {self.container_name} started")

  def exec_host(self, cmd):
    if isinstance(cmd, list):
      cmd = ' '.join(map(str, cmd))
      
    logging.debug("exec_host", cmd)
    
    return os.system(cmd)

  def exec_container(self, cmd):
    if isinstance(cmd, list):
      cmd = ' '.join(map(str, cmd))
      
    logging.debug("exec_container", cmd)
    
    return self.exec_host([
        "docker", "exec",
        "-w", "/sandbox",
        self.container_name,
        "/bin/sh", "-c", quote(cmd)
    ])

  def exec(self, cmd, stdin="", stdout="", stderr="", time_limit=1, memory_limit=256):
    if isinstance(cmd, list):
      cmd = ' '.join(map(str, cmd))

    logging.info(f"exec {cmd}")

    self.exec_container([
        "ulimit", "-s", "unlimited",
        "&&",
        "/usr/local/bin/run",
        int(time_limit * 1000),
        int(memory_limit * 1024),
        quote(stdin),
        quote(stdout),
        quote(stderr),
        cmd
    ])

    with open(os.path.join(self.base_dir, "ReSultS.TxT"), "r") as f:
      status, message, time, memory = map(lambda x: x.strip(), f.readlines())
      time = float(time) / 1000
      memory = float(memory) / 1024
      status = Status["".join(status.split())]

    return namedtuple("SandboxResult",
                      ["status", "message", "time", "memory"])(status, message, time, memory)

  def read(self, path: str) -> str:
    with open(os.path.join(self.base_dir, path), "r") as f:
      return f.read()

  def write(self, path: str, text: str):
    with open(os.path.join(self.base_dir, path), "w") as f:
      f.write(text)

  def exists(self, path: str):
    return os.path.exists(os.path.join(self.base_dir, path))

  def push(self, srcpath: str, dstpath: str):
    dstpath = os.path.join(self.base_dir, dstpath)
    if os.path.isfile(srcpath):
      shutil.copy(srcpath, dstpath)
    else:
      shutil.copytree(srcpath, dstpath)

  def pull(self, srcpath: str, dstpath: str):
    srcpath = os.path.join(self.base_dir, srcpath)
    if os.path.isfile(srcpath):
      shutil.copy(srcpath, dstpath)
    else:
      shutil.copytree(srcpath, dstpath)

  def delete(self, path: str):
    path = os.path.join(self.base_dir, path)
    if os.path.isfile(path):
      os.remove(path)
    else:
      shutil.rmtree(path)

  def clean(self):
    for item in os.listdir(self.base_dir):
      item = os.path.join(self.base_dir, item)
      if os.path.isfile(item):
        os.remove(item)
      else:
        shutil.rmtree(item)

  def terminate(self):
    self.exec_host([
        "> /dev/null",
        "docker stop -t 0",
        self.container_name
    ])

    if config.DEBUG:
      logging.info(f"Container {self.container_name} stopped")
    else:
      shutil.rmtree(self.base_dir)

    _instances.remove(self)


def terminate_all():
  instances = tuple(_instances)
  for sbox in instances:
    sbox.terminate()
