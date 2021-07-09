TCP 流量控制
## 发送和接收buffer
- 当一个用户应用向另一个用户应用发送数据时，数据首先被存储在操作系统内核内的发送缓冲区。
![][image-1]
- 当发送缓冲区包含超过MSS字节或发送时间过期时，TCP模块将在一个TCP段中向接收方发送数据。
![][image-2]
接收数据存储在接收方计算机的操作系统内核内的接收缓冲区中。

- 接收应用程序可以使用read()系统调用来清空接收缓冲区中的接收数据。
![][image-3]
## 流量控制
- 流量控制是一种机制，确保发送方的传输速率不超过接收方的容量。
**事实是：**
> 如果传输速率超过了接收器的容量，那么迟早会没有缓冲空间来存储到达的数据包。
> 当这种情况发生时，新到达的数据包会被丢弃。

这里有一个比喻，当接收器的处理率低于传输率时，会发生什么:

![][image-4]
- 桶里有一个洞，可以让水以1升/分钟的速度排出。

- 一根管子以2升/分钟的速度将水灌进桶里。

- 迟早有一天，水桶会溢出来。
## 流量控制是如何实现的？
TCP的流量控制是通过TCP头中的 Advertised Windowsize大小实现的。
![][image-5]
Advertised Window Size是接收方愿意缓冲的最大字节数。
发送方应尊重接收方的要求，避免发送超过给定的Advertised Window Size的数据。
例如：
![][image-6]
- 客户端告诉服务器不要发送超过300字节的数据
- 服务器告诉客户不要发送超过900字节的数据
## Receive Buffer 和 Advertised Window Size
- Factors that determine the Advertised Window Size
	- TCP连接所保留的接收缓冲区的大小
	- 接收缓冲区的大小在连接建立时是固定的
	- 当前在接收缓冲区中缓冲的数据量
- 接收缓冲区：
- 接收缓冲区位于操作系统（内核）内部。
	- 当收到一个数据段时，接收缓冲区被填满。
	- 当用户进程读取数据时，接收缓冲区被清空（一点点）。
- 用户程序可以通过使用 setsockopt() 系统调用来设置最大接收缓冲区的大小。
来自 setsockopt man 页：


 SO_SNDBUF和SO_RCVBUF 选项分别调整分配给输出和输入缓冲区的正常缓冲区大小。缓冲区大小可以为大流量连接增加，也可以减少，以限制可能积压的入站数据。UDP的最大缓冲区大小由ndd变量udp_max_buf的值决定。TCP的最大缓冲区大小是由ndd变量tcp_max_buf的值决定的。在创建套接字之前使用 setsockopt.

在Solaris中默认的接收缓冲区大小是1Mbytes。

```python
> ndd /dev/tcp  tcp_max_buf
1048576
```
# 计算 Advertised Window Size
以下类型的数据可以存储在接收缓冲区。
- Deliverable data:
	- Data that has been acknowledges
> I.e., all preceeding data have been received
> The application can readily read the data (because the data can be delivered in the order that was transmitted)

- Undeliverable data:
	- Data that was received, but not been acknowledged because some preceeding data has not been received
> The application cannot read the data because the data would be read out of the order that was transmitted)
![][image-7]
Clearly, the Advertised WindowSize should be set to:
```python
Advertised Window = SizeRecvBuffer - (LastByteRecv - LastByteRead)
```

## 实际应用中的流量控制
只有当速度较快的发送方向速度较慢的接收方发送时，流量控制的效果才会显现出来!!!
下面的流量控制例子使用了100K字节的接收缓冲区大小
1. 最初，发送和接收缓冲区是空的。接收方公布了一个100K字节的窗口。
![][image-8]
2. 发送方快速发送许多数据包，速度超过接收方的处理能力...
接收缓冲区开始被填满，很快，Advertised Window Size下降到50K字节。
￼![][image-9]
3. 这种情况继续下去，接收缓冲区会进一步填满
来自接收方的ACK数据包现在会有一个较低的Advertised Window Size，例如，1 K字节。
![][image-10]
4. 迟早有一天，接收缓冲区会被填满
接收者返回一个ACK数据包，其广告窗口=0字节!!!
![][image-11]

这导致发送TCP停止传输更多的数据.....，并防止发送TCP溢出接收TCP的接收缓冲区。

> NOTE:

> > This will not stop the sending application from sending more data....
> > The sending application process can still send more data...
> > but the data sent will remains in the send buffer !!! (as given in the above figure)
5. 如果发送应用进程继续发送，发送缓冲区将被填满
随后的write()调用将导致发送应用进程阻塞。
￼![][image-12]
现在，发送应用程序已经被限流了。

## 编程需要注意的地方
- The default bahavior of write() is blocking
	-When the send buffer fills up, the write() operation will cause the application to block (wait)
- Non-blocking write() operations:
The following UNIX system call will change the behavior of write() to non-blocking:
```python
  fcntl(socket, F_SETFL, fcntl(recvfd, F_GETFL)|O_NDELAY);   
```
The write() operation will return −1 when the send buffer is full (otherwise, it will return the number of bytes written)
# TCP 流控block的问题
事实
A receiving TCP protocol module will only send an (ACK) packet if it has received a TCP segment....
> Rephrased:
> - A receiving TCP protocol module will not send an (ACK) packet if it has not receive any TCP segment....
带来的问题：
> Since the advertised window size = 0 at the sender, the sender cannnot send any packet...
> Consequently, the the receiver may not send any packet to the sender
> Consequently, the Adverised Window Size of the sender will remain ZERO
类似“死锁”的场景：
![][image-13]
如果在发送方advertised window 大小=0，并且发送方在发送缓冲区有一些数据，发送方将定期向接收方发送一个字节的TCP段，以触发接收方的响应。
![][image-14]

字节大小探测TCP段的确认将包含adv.wind.size的新（非零）值，发送方可以用它来控制其传输的速度。
原文：[http://www.mathcs.emory.edu/\~cheung/Courses/455/Syllabus/7-transport/flow-control.html][1]

[1]:	http://www.mathcs.emory.edu/~cheung/Courses/455/Syllabus/7-transport/flow-control.html

[image-1]:	https://tva1.sinaimg.cn/large/008i3skNly1grdkthxeikj310y0aodgm.jpg
[image-2]:	https://tva1.sinaimg.cn/large/008i3skNly1grdkua1ln8j311i0f0q3r.jpg
[image-3]:	https://tva1.sinaimg.cn/large/008i3skNly1grdkvlrkxyj311y0akdgl.jpg
[image-4]:	https://tva1.sinaimg.cn/large/008i3skNly1grdky4szjij30e40d6mxd.jpg
[image-5]:	https://tva1.sinaimg.cn/large/008i3skNly1grdl3t5yo9j310i0iadhn.jpg
[image-6]:	https://tva1.sinaimg.cn/large/008i3skNly1grdl66wfzoj311w0bg3zk.jpg
[image-7]:	https://tva1.sinaimg.cn/large/008i3skNly1grdllrym5sj31260pcjtq.jpg
[image-8]:	https://tva1.sinaimg.cn/large/008i3skNly1grdlobq9hxj310a0f4ab8.jpg
[image-9]:	https://tva1.sinaimg.cn/large/008i3skNly1grdlpep5xnj310m0f2ab9.jpg
[image-10]:	https://tva1.sinaimg.cn/large/008i3skNly1grdlreh8oqj30zk0eqgmr.jpg
[image-11]:	https://tva1.sinaimg.cn/large/008i3skNly1grdlryqf3oj310k0d275c.jpg
[image-12]:	https://tva1.sinaimg.cn/large/008i3skNly1grdluay391j30zw08igmj.jpg
[image-13]:	https://tva1.sinaimg.cn/large/008i3skNly1grdm3ucgiwj314e0i00ul.jpg
[image-14]:	https://tva1.sinaimg.cn/large/008i3skNly1grdm5b8wj6j311e0jg762.jpg