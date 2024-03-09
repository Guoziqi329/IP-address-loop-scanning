# IP-address-loop-scanning

这是一个循环扫描ip地址的程序，每隔一定时间扫描一次（默认30分钟），如果输入"**yes**"程序会立即扫描，并且重新计时。
## 开始使用
你需要准备两个txt文件用来装要扫描的IP和备注地址，并且设置代码中的参数。
### 安装依赖
代码一共依赖`ping3`和`openpyxl`这两个库，安装代码：
```
pip install ping3
pip install openpyxl
```
对版本应该没什么限制
***
### 文件1（ip地址文件）
该文件需要以以下格式来写`name=xxx.xxx.xxx.xxx`例如：
```
address1=192.168.10.1
address2=192.168.10.2
address3=192.168.10.3
address4=192.168.10.4
...
```
***
### 文件2（真实地址）
该文件和文件一类似以`name=xx地址`的格式来写，例如：
```
address1=地址1
address2=地址2
address3=地址3
address4=地址4
```
***
### 修改代码
1.找到这几行代码（在import下面）
```
ip_address_file = 'ip地址.txt'  
ip_actual_address = 'ip地址实际名称.txt'
```
把`ip_address_file`的值改为文件1的名字，把`ip_actual_address`的值改为文件2的名字

2.找到第120行的`elif time.time() - t > 1800:`代码，1800秒为30分钟，你也可以改成其他数字。
***
### 查看日志
在运行过程中会产生一个叫`ip地址日志.xlsx`的excel文件，里面存放IP地址扫描的日志。
