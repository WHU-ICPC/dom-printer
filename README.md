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
usage: client.py [-h] [--saveDir SAVEDIR] [--saveExt SAVEEXT] server user passwd

positional arguments:
  server             服务端地址
  user               用户名
  passwd             密码

optional arguments:
  -h, --help         show this help message and exit
  --saveDir SAVEDIR  保存文件的目录, 默认./PrintFiles
  --saveExt SAVEEXT  保存文件的扩展名, 默认txt

```
### 示例
使用 BaseAuth 账户 `admin` 密码 `1234` 请求服务端(`http://127.0.0.1:5000`)并保存文件至`print`目录下, 扩展名为 `pdf`
```shell
python client.py --saveDir ./print --saveExt pdf http://127.0.0.1:5000 admin 1234
```