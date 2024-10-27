# `data-lock.yaml` 配置

此文件为 web 后端根据 `data.yaml` 使用脚本自动生成，用于降低 web 后端与评测端代码的耦合性，以及降低自定义 `judger.py` 的编写难度。**请勿手动修改，配置信息被覆盖后果自负。**

生成脚本可以在 [`tools/lock.py`](../tools/lock.py) 找到。

自定义评测时只需读取该 `data-lock.yaml` 即可，其结构较为简单，所有默认的字段都已被写入，因此读取时无需处理默认值。测试点的正则匹配也已经完成。所有字段都检查过合法性，并检查过文件是否在数据包中存在。

也就是说按照该 `data-lock.yaml` 进行评测时 judger 无需考虑奇怪的 corner cases（~~大概吧~~）。

发现问题请[提 issue](https://github.com/yaoxi-std/antoj-judger/issues/new) ~~或找我本人~~。

一种可能的 `data-lock.yaml` 如下：

```yaml
checker:
  name: lcmp
  type: default
extraJudgerInfo: {}
extraSourceFiles: []
fileIO:
  input: .stdin
  output: .stdout
judger: judger.py
memory: 256.0
submitFiles:
- languages:
  - c
  - cpp
  - cpp11
  - cpp14
  - cpp17
  - cpp11-clang
  - cpp17-clang
  - haskell
  - pascal
  - java
  - python2
  - python3
  - rust
  - nodejs
  - swift
  - csharp
  - text
  - zip
  - binary
  name: code
subtasks:
- cases:
  - input: 1.in
    output: 1.ans
  depends: []
  id: 1
  memory: 256.0
  score: 100.0
  time: 1.0
  type: sum
time: 1.0
type: custom
```
