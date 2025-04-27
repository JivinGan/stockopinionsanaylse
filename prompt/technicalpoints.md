win 部署
安装 pymysql  
pip install pymysql

pymysql 是Python里连接MySQL常用的库之一
不然Python会找不到 pymysql，抛出 ModuleNotFoundError。

pip install cryptography

MySQL8以后默认密码插件	caching_sha2_password
加密通讯时需要处理认证协议，比如ssl、加密密码交换