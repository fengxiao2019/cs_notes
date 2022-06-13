Supervisor 配置
机器配置：centos 7.5
#### 步骤1: 安装supervisor
```json
yum install -y epel-release
yum install -y supervisor
```
#### 步骤2: 生成配置文件
配置文件路径：`/etc/supervisord.conf` 
#### 步骤3: supervisord 添加到自启动
添加自动启动脚本，脚本目录：[https://raw.githubusercontent.com/Supervisor/initscripts/master/redhat-init-mingalevme][1]
将内容复制到文件`/etc/supervisord`
修改
```json
PIDFILE=/var/run/supervisord.pid
```
变更为：
```json
PIDFILE=/tmp/supervisord.pid
```

```json

chmod +x /etc/init.d/supervisord
chkconfig --add supervisord
chkconfig supervisord on
service supervisord start
```
#### 步骤4: 添加配置项（ **添加服务只需要这一个步骤**）
需要修改：`/etc/supervisord.conf ` 文件
可以参考`fuxi_service`的配置添加，只需要修改environment/ command / directory 三个配置项就可以。
之后，可以利用 `service supervisord [stop|start|restart]`  操纵`supervisord` 服务。
也可以使用 `supervisorctl` 命令操作。
```json
supervisorctl reload # 控制supervisord从新加载配置文件
supervisorctl restart service name # service name 具体指/etc/supervisord.conf 中的[program:x]中的x
supervisorctl stop service name
supervisorctl start service name
supervisorctl tail -f service name
```

`supervisord` 的日志目录：`/tmp/supervisord.log`
启动异常信息可以在该日志文件中添加。

[1]:	https://raw.githubusercontent.com/Supervisor/initscripts/master/redhat-init-mingalevme