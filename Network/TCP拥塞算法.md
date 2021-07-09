场景
tcp无法感知网络流量状态，因为在任意时刻网络上都可能有新的连接建立，其他连接也可能在任意时刻断开，所以网络是拥堵和畅通此连接并不清楚，那就需要根据实际的网络情况做一些调整。
涉及到的算法
- 慢启动
- 快速重传
- 快速恢复

这几个算法里面涉及到的几个概念
- TWS： 网络数据传输窗口 Transmit Window Size，发送方可以发送的#个数据包（每个数据包中的MSS字节），无需等待确认。
- AWS：Advertised Window Size  - 由接收端控制
- CWND：拥塞窗口(Congestion Window Size)   - 由发送端控制，发送方认为它可以在不引起网络拥堵的情况下传送到网络中的数据包（MSS字节的数据）的数量。
其中TWS = min(AWS，CWND)

**慢启动阶段**
> 这是TCP的启动运行模式
> 在这个模式/阶段，TCP对最大传输速率有一个想法（猜测），并且TCP正试图达到这个传输速率。
> 尽管TCP知道（猜测）这个最大传输速率，但TCP不会立即以这个速率传输。
> 在这个阶段，TCP将从传输一个数据包开始，一个RTT之后，TCP将把数据包的数量增加一倍（导致数据包的数量在时间上呈指数级增长）。

**避开拥堵阶段**
> 这是在启动阶段之后开始的阶段
> 当TCP达到它 "认为 "安全的最大传输速率时，启动阶段结束。

> 换句话说，TCP现在处于未知的领域....。
> 因为TCP已经达到了最大的安全水平，所以似乎还有一些可用的容量--不使用可用的容量就太可惜了，但是，TCP不知道新的最大容量是多少......所以它必须小心谨慎
> 在这个阶段，TCP增加数据包的数量将比启动阶段慢得多（增加率不是指数型的，而是**线性的**）。
这个阶段，理想情况下，希望每一个RTT结束CWND增加一个packet或者一个MSS。(如果收到的是一个 老的ACK数据，CWND不变化)
公式为：
```sql
 CWND = CWND + MSS \* MSS/CWND
```

![][image-1]

两个阶段最大的区别是对传输速率的控制

### 涉及到的策略
**慢启动**
在慢启动阶段，采用慢启动策略
\*\*涉及到的概念
> SSThresHold
> > TCP认为安全的窗口大小
> > SSThresHold=AWS，当TCP第一次开始时。
> > 当TCP检测到数据包丢失时，SSThresHold被设置为TWS/2
> CWND
> > (当前)拥塞窗口大小
> > CWND和AWS将决定TCP的发送窗口大小

**执行步骤**
1. 初始化。
> SSThresHold被设置为AWS（当TCP首次开始时）或传输窗口/2（当TCP检测到拥堵时）。
2. 慢速启动。

3. 设置CWND=MSS（即一个数据包）。
> 每当TCP收到一个新的ACK包（=TCP以前从未见过的ACK报文）时，TCP将CWND增加MSS。
> 注意：如果TCP收到一个重复的ACK，则不对CWND变量进行更新）。

_**慢启动阶段有意思的问题**_
1. 慢启动阶段什么时候结束？
![][image-2]
case 1: CWND \> SSThresh
case 2: 当tcp检测到丢包，这是一种非正常的方式，这种情况下，tcp 会重新进入慢启动阶段，
TCP 首先设置 SSThresHold = Transmit Window/2
然后TCP重新设置 CWND = 1 来重新启动慢启动阶段。

2. 指数级传输数据为什么还被称为慢启动？
与发送AWS字节的数据相比，先开始发送一个数据包的新方法确实比较慢......。


**快速重传 **
利用重复的ACKs来表示数据丢失。
数据在IP层传输是无序的，当TCP收到3个重复的ACK（所以TCP总共收到了4个相同的ACK包），那么TCP就断定该包丢失了，并且TCP立即重传该丢失的包（不需要等待超时）。在TCP重传丢失的数据包后，它进入慢速启动阶段（因为发生了数据包丢失）。
![][image-3]
**快速恢复**
快速恢复是对tcp传输性能进行的一个改进，显著提高了tcp的性能。研究发现，大多数快速重传动作发生在轻度拥堵情况下，即拥堵很快就会消失。研究发现，TCP不执行SLOW START（将CWND降低到1 x MSS），而是使用更大的拥塞窗口，也不会造成网络拥堵。

当TCP执行快速重传时（所以TCP没有超时）。
设置SSThresh = CWND/2
设置CWND = SSThresh + 3 \* MSS。
(理由是3个重复的ACK值3个MSS字节)

TCP继续使用拥塞避免（但使用SSThresh和CWND的新值）。
引用：
[http://www.mathcs.emory.edu/\~cheung/Courses/455/Syllabus/syl.html#CURRENT][1]
[http://www.mathcs.emory.edu//\~cheung/Courses/455/Syllabus/A1-congestion/tcp2.html][2]

[1]:	http://www.mathcs.emory.edu/~cheung/Courses/455/Syllabus/syl.html#CURRENT
[2]:	http://www.mathcs.emory.edu//~cheung/Courses/455/Syllabus/A1-congestion/tcp2.html

[image-1]:	https://tva1.sinaimg.cn/large/008i3skNly1gprj5sska1j30kz0aiabj.jpg
[image-2]:	https://tva1.sinaimg.cn/large/008i3skNly1gprjknqim5j30hk032t8u.jpg
[image-3]:	https://tva1.sinaimg.cn/large/008i3skNgy1gprr17fdxij30lj0cp763.jpg