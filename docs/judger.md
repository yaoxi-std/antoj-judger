# 自定义 judger

咕咕咕

会补上的，在这之前可以看看 [default judger](../scripts/judger/default.py) 咋写的。工具类都封装在 `scripts.judger.utils` 里了，运行选手代码时请使用 Sandbox。~~其实有个参考实现也不难看懂~~

由于自定义 judger 必须与评测后端运行在同一进程中，所以考虑到安全性问题该 feature 默认是关闭的。若要开启请联系管理员在 [`config.py`](../config.py) 中修改并将你的 judger 加入白名单（~~白名单功能还在咕咕咕~~）。
