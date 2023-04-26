# dom-printer
## 目录结构
```
dom-printer
 ├── client.py            客户端
 ├── fake.py              在simulation/server内生成模拟数据
 ├── requirements.txt
 ├── server.py            服务端
 └── simulation           模拟目录
     ├── client
     └── server
         ├── new
         └── old
```
## CLI用法
```
usage: client.py [-h] [--saveExt SAVEEXT] [--rmPrintFile RMPRINTFILE] server user passwd

positional arguments:
  server                服务端地址
  user                  用户名
  passwd                密码

optional arguments:
  -h, --help            show this help message and exit
  --saveExt SAVEEXT     保存文件的扩展名, 默认.txt
  --rmPrintFile RMPRINTFILE
                        是否在打印完后删除对应文件, 默认 false
```
