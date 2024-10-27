# `data.yaml` 配置

`data.yaml` 基于 SYZOJ 的 `data.yml` 进行了一些修改，例如将题目的时空限制写入配置文件中以便于题目的传输，以及添加一些额外配置使其更加灵活。`data.yaml` 不完全兼容 SYZOJ 的 `data.yml`，但在 `data.yml` 上稍作修改后即可，故建议使用 `.yaml` 作为后缀以进行区分。

以下是 `data.yaml` 的示例：

---

```yaml
# 评测方式。支持的值有：
# - `default`         常规评测，ioi-style 的交互题应设为此方式
# - `interactive`     交互题，特指 cf/icpc-style 使用 io 的交互题
# - `submit-answer`   提交答案题
# - `objective`       客观题
# - `custom`          完全自定义评测方式，需要使用自定义评测脚本，如通信题等
type: default

# 全局时间限制，未对 subtask 指定特殊时间限制则默认使用此限制
# 支持浮点数，以 `s/ms` 作为后缀
time: 1.0s

# 全局空间限制。未对 subtask 指定特殊空间限制则默认使用此限制
# 支持浮点数，以 `k/kb/m/mb/g/gb` 为后缀，且后缀不区分大小写
memory: 256.0MB

# 输入文件和答案文件在数据包中的文件名格式，非必须
# 会自动将 `#` 替换为子任务配置中指定的内容，详见子任务配置
inputFile: "#.in"
outputFile: "#.ans"

# 选手提交的输出文件名称
# 仅 type 为 `submit-answer` 时允许
userOutput: "dat#.out"

# 子任务配置。type 为 `objective` 或 `submit-answer` 时不允许使用
subtasks:
- score: 100        # 该子任务的分数。除了 custom 类型之外，所有子任务的总分必须为 100
  type: sum         # 子任务类型，可选值有 sum/min/max
  id: 1             # 子任务编号，若不指定则默认为上一子任务的编号 +1，从 1 开始
  time: 2s          # 特殊时间限制，若不指定则使用全局限制
  memory: 512m      # 特殊空间限制，同上
  depends: []       # 子任务依赖，数组内填写依赖的子任务编号。必须严格小于当前子任务的编号
  cases:            # 该子任务的测试点

    # 使用 inputFile 和 outputFile 进行替换
    # 匹配 1a.in / 1a.ans
    - 1a

    # 直接指定 2a.in / 2a.ans
    # 只使用此项无需填写 inputFile 和 outputFile
    - input: 2a.in
      output: 2a.ans

    # 以斜杠 `/` 开头结尾的字符串会被当作正则表达式进行处理
    # 并使用 inputFile / outputFile 进行匹配。此项等价于：
    # - input: /^(3[a-zA-Z]+).in$/
    # - output: /^(3[a-zA-Z]+).ans$/
    - /3[a-zA-Z]+/

    # 直接使用正则表达式指定输入输出文件
    # 注意正则表达式中的括号有提取匹配项的语义，匹配方式为将括号位置匹配到的字符串提取为 tuple[str]
    # 并将 tuple 值相同的 input 和 output 划分至同一组内
    # 例如 `4a.in` 和 `4a.ans` 提取出的 tuple 均为 `('4', 'a')`，因此会被放置在同一组内
    # 注：正则表达式中 `^` 表示匹配开头，`$` 表示匹配结尾
    - input: /^(4)([a-zA-Z]+).in$/
      output: /^(4)([a-zA-Z]+).ans$/

# 文件输入输出，默认使用标准输入输出
fileIO:
  input: .stdin     # 输入文件，`.stdin` 表示标准输入
  output: .stdout   # 输出文件，`.stdout` 表示标准输出

# checker 非必须。默认不会从 data 文件夹中寻找！
# 自定义 special judge 编译时会提供 testlib
# 但也可以像 SYZOJ 那样将得分和额外信息分别输出到 stdout 和 stderr
# special judge 运行目录下还会有 input、user_out、answer、code 四个文件
# 同时调用 spj 时会传入 input user_out answer 作为命令行参数
# 得分的范围为 [0, 100]，会自动折合到子任务分数
checker:
  type: default       # 或 custom 表示使用 special judge
  name: lcmp          # 逐行比较，忽略空白符。其他内置 checker 见
                      # https://github.com/MikeMirzayanov/testlib
  # language: cpp17   # special judge 使用的语言，type 为 custom 时必须

# 编译时使用的额外文件
extraSourceFiles:
- name: itlib_cpp.h       # 在 data 文件夹中的位置
  dest: interaction.h     # 目标文件名，在编译时被放置在与选手程序的同一目录下
  language: cpp           # 对应的语言，注意 cpp 不包括 cpp11、cpp14 等
- name: grader.cpp
  dest: grader.cpp        # 编译时不会自动将 grader.cpp 加入到 gcc 编译命令中
  language: cpp           # 因此需要在 itlib_cpp.h 中 `#include "grader.cpp"`
- name: itlib_c.h         # ~~SYZOJ 也这么干不是吗~~
  dest: interaction.h
  language: c             # C 语言版本的头文件

# cf/icpc-style 的交互器，仅在 type 为 interactive 时允许使用
interactor:
- name: interactor.cpp    # 很容易理解吧
  language: cpp17

# 提交时允许使用的语言。不指定则默认所有语言都可以
languages: [c, cpp]

# 选手需要提交的文件列表。仅在 type 为 custom 时允许使用。若不指定则默认提交文件名为 `code`
submitFiles:
- languages: [c, cpp]   # 若不指定则使用全局 languages
  name: code
- languages: [c, cpp]   # 支持提交多个文件
  name: code2

# 仅在 type 为 custom 时允许使用
# 自定义 judger 名称，默认为 judger.py。只支持 python 编写，编写方式见 `judger.md`
judger: judger.py

# 传递给自定义 judger 的信息
# 不要在 yaml 的全局 key 中储存自定义信息，解析时会被自动忽略！
# 仅在 type 为 custom 时允许使用
extraJudgerInfo: {}
```

当 `data` 目录下不存在 `data.yml` 和 `data.yaml` 或者一些参数未指定时，会默认使用以下配置文件中的内容：

```yaml
type: default
time: 1.0s
memory: 256.0MB
subtasks:
- score: 100
  type: sum
  cases:
    # 匹配 abc123.in / abc123.out
  - input: /^([a-zA-Z]*)([0-9]+).in$/
    output: /^([a-zA-Z]*)([0-9]+).out$/
    # 匹配 abc123.in / abc123.ans
  - input: /^([a-zA-Z]*)([0-9]+).in$/
    output: /^([a-zA-Z]*)([0-9]+).ans$/
    # 匹配 input123.txt / output123.txt
  - input: /^(input)([0-9]+).txt$/
    output: /^(output)([0-9]+).txt$/
    # 匹配 input123.txt / answer123.txt
  - input: /^(input)([0-9]+).txt$/
    output: /^(answer)([0-9]+).txt$/
fileIO:
  input: .stdin
  output: .stdout
checker:
  type: default
  name: lcmp # 逐行比较，忽略空白符
```
