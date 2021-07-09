# TCP 消息格式

![][image-1]

## Source port # and destination port#:
Used to implement the multiplexing function (just like UDP)
## FLAGS: used to indicate a TCP control message
### SYN flag: (synchronize)
> SYN is set when the TCP source wants to establish a connection
### FIN flag: (finish)
> FIN is set when the either TCP party wants to close an existing TCP connection
### RESET flag: (reset)
> RESET is used to abort a TCP connection
> (Abnormal exit)

### PUSH flag: (flush the connection)
> The PUSH bit is set when the user application invoked the push operation that flushes/clears the transmission buffer.
### URG flag::
> indicates that urgent data is sent inside the TCP payload.
> The Urgent pointer marks the end of the urgent data
### ACK flag: (acknowledgement)
> If the ACK bit is set:
> The Acknowledgement (receive) sequence number in the TCP header is valid
Otherwise:
> The Acknowledgement (receive) sequence number in the TCP header is invalid and must be ignored !!!
> Note:
> The send sequence number in the TCP header is always valid
- SequenceNumber
	- Eevery item that require reliable transmission must be:
		- identified by a unique (send) sequence number
> Example:
> - A SYN request (used to establish a TCP connection)
> - A FIN request (used to tear down a TCP connection)
> - Each byte that the user application transmits

## Acknowlegdement Number
In TCP, ACK(n) will acknowledge:
All send sequence numbers that are \< n
> Note:
> the Acknowlegdement Number is only valid if the ACK flag bit is set !!!!!!!

## Advertised WindowSize:
- Use in flow control
- Advertised window size = the many bytes (free space) that is available in the receiver buffer
The sender cannot transmit more data than it is given in the Adv. window size

## CheckSum: checksums the TCP header & message.

原文：[http://www.mathcs.emory.edu/\~cheung/Courses/455/Syllabus/7-transport/tcp1b.html][1]

[1]:	http://www.mathcs.emory.edu/~cheung/Courses/455/Syllabus/7-transport/tcp1b.html

[image-1]:	https://tva1.sinaimg.cn/large/008i3skNly1grdl3t5yo9j310i0iadhn.jpg

#is_material