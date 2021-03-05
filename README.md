# 计组作业帮

> 为了帮助完成我校计组课设作业而做的小工具

*注：本项目仅支持导出指令系统表及uM微程序表，若要导出程序执行跟踪结果请移步至[COP3000](https://github.com/i-Pear/COP3000)*

## 使用方法

```shell script
# 会询问文件的路径
python run.py
# 直接进行解析
python run.py 文件名
```

## 一些说明

- 通过解析 COP2000 模拟器生成的 `*.INS` 文件来生成两个表：

    - `*.INS.inst.csv` 是文件对应的 指令系统表

    - `*.INS.upro.csv` 是文件对应的 uM微程序表
    
- 由于生成的是 csv 文件，在不同办公软件中的样式并不一致（有的带边框有的不带），可能需要手动调整下
    
- 本工具基于如下约定进行文件的解析：

    - 提供的文件是有效的
    
    - 文件中微程序以前的部分不可能出现 0xff 字节
    
    - 文件中的 0x00 字节是无效字节，可以放心跳过
    
    - 文件中 `_FATCH_` 指令的微程序是 `0xCBFFFF, 0xFFFFFF, 0xFFFFFF`
    
    - 对于 uM微程序表 而言：
        
        - "数据打入" 这一项里值的顺序可能与模拟器中的显示不一致

        - "状态" 这一项里只保证在指令中最后一条微指令为 T0 的条件下从第一条微指令递减

- 技术不佳，欢迎提交 issue 和 PR 进行交流
