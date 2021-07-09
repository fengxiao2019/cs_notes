golang-环境变量 GOPATH
环境变量GOPATH 是用来解析import 语句的，GOPATH的实现源码在go/build中。
如果环境变量没有设置，GOPATH默认为用户主目录中名为“ go”的子目录（unix下为$HOME/go，windows下为%USERPROFILE%\go on Windows），可以通过命令 go env GOPATH 来查看当前的GOPATH环境变量的值。


