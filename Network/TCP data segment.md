TCP data segment
- TCP data segment = another name for a tcp message
Facts about a TCP data segment
- A TCP data segment contains zero or more bytes
> A TCP ACK message may contains zero bytes of data !!!
> Important note:
> > A zero byte message (= an ACK message) does not need to be acknowledged !!!
> > because:
> > > you do not acknowledge an ACK message, otherwise, you have an infinite loop...

## The TCP send buffer
用户端通过TCP 发送数据，在c/c++中使用`write`系统调用，数据被存储在TCP 的send buffer中
注意：
> 通过write 系统调用写入的数据并不会立即被发送！！！
> 多次写入的数据可能会通过一次TCP segment 发送（this will help improve efficiency / performance）
> 另外，通过一次write 系统调用写入的数据也可能通过多个tcp segment 发送（一次写入的数据太大时）
![][image-1]
## TCP‘s MSS （Maximum Segment Size）
MSS = the largest tcp segment size that the TCP protocol will transmit
> 小的MSS值将减少/消除IP分片
> 小的MSS值也会导致传输更多的IP数据包，从而增加开销。
> MSS is set by the Operating System (system administrator)
## TCP transmission timer
- 传输定时器 = TCP用于传输数据段的倒计时器
- 当TCP传输一个数据段时，传输定时器被重置（大约3秒）。
- 当传输定时器过期时: TCP发送缓冲区中的所有数据将被立即传输
## tcp segment 传输算法
```python
if (  write( data ) operation )
   {
      Append data to the TCP send buffer;

      /* =================================================
         Transmit data if buffer exceeds MMS
	 ================================================= */
      while ( length(TCP send buffer) ≥ MSS )
      {
         Transmit  MSS bytes from send buffer in a TCP segment; 
         Reset TCP transmission timer;
      }
   }
   else if ( push( ) operation )   // C/C++'s flush( ) call
   {
      Transmit all data from send buffer in a TCP segment; 
      Reset TCP transmission timer;
   }
   else if ( TCP timer expired )
   {
      Transmit all data from send buffer in a TCP segment; 
      Reset TCP transmission timer; 
   }
```
## tcp receive buffer
receive buffer: 内核数据结构，用来存储接收到的数据
The read( ) system call is used to extract data from the TCP receive buffer
read(N bytes, …) 系统调用的行为：
```python
if ( length(TCP receive buffer) ≥ N bytes )
   {
      return N bytes to user program;
   }
   else
   {
      block until TCP receive buffer has ≥ N bytes;          
   }

   (I.e.: exactly like a pipe)
```
![][image-2]

[image-1]:	https://tva1.sinaimg.cn/large/008i3skNly1grdkj13v8hj30v00n675z.jpg
[image-2]:	https://tva1.sinaimg.cn/large/008i3skNly1grdkqam6w0j31240ic0u8.jpg