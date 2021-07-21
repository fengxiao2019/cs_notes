client 和 server 都可以发起`close operation`。
标志位：FIN

**数据格式 **
「SeqNo ｜ AckNo ｜ FLAGS」｜ DATA」
   100               300          FIN           Empty
**正常关闭的流程**
step1: 客户端TCP发送一个TCP段，FIN位设置为1，并进入`FIN_WAIT_1`状态。
step2: server端发送一个TCP段，ACK位设置为1。
step3:client 收到server发送的响应消息后，client TCP进入`FIN_WAIT_2`状态。
step4:  server 发送一个tcp段，FIN位设置为1
step5: client 接收到server 发送的FIN报文，client 进入`TIME_WAIT`状态。

**`TIME_WAIT`状态让TCP客户端在ACK丢失的情况下重新发送最后的确认信息**。在`TIME_WAIT`状态下花费的时间与实现有关，但典型的值是30秒、1分钟和2分钟。等待之后，连接正式关闭，客户端的所有资源（包括端口号）被释放。
![][image-1] ![][image-2] ![][image-3]
**非正常关闭**
- 通过RST标志位结束

[课程课件链接][1]
[课件2][2]

[1]:	http://www.mathcs.emory.edu//~cheung/Courses/455/Syllabus/7-transport/tcp3a.html
[2]:	http://www.mathcs.emory.edu//~cheung/Courses/455/Syllabus/7-transport/tcp3c.html

[image-1]:	https://tva1.sinaimg.cn/large/008i3skNly1gsmc6m1kqsj30o40icq49.jpg
[image-2]:	https://tva1.sinaimg.cn/large/008i3skNly1gsmevrllp2j30lg0giwfk.jpg
[image-3]:	https://tva1.sinaimg.cn/large/008i3skNly1gsmccnaq3rj30kg0ms0tk.jpg