Python 协程greenlet 实现原理

**greenlet 、eventlet、gevent 三者之间的关系？**
> greenlet 源于stack Python项目，可以作为官方Cpython的一个扩展使用。
> gevent 正是基于greenlet实现的。
> eventlet 基于greenlet实现。

**greenlet 上下文切换 和 yield的类型的上下文切换有什么不同？**
> greenlet 上下文切换可以直接switch上另一个greenlet，不用关心目标greenlet是否已经在运行，不同greenlet 之间处于完全对等状态，可以相互switch。（缺点：会导致代码的逻辑混乱）
> yield实现的协程只能切换到自己直接或间接的调用者，本质上yield只能保留栈顶的帧，python 3中可以使用`yield from` 嵌套的挂起内存过程调用，但是仍然不能任意的切换到其他上下文。

**greenlet基本原理？**
> 将一个子过程封装进一个greenlet里，而一个greenlet代表了一段C的栈内存。
> 在greenlet里执行Python的子过程（通常是个函数），当要切换出去的时候，保存当前greenlet的栈内存，方式是memcpy到堆上，也就是说每一个greenlet可能都需要在堆上保存上下文，挂起的时候就把栈内存memcpy到堆上，恢复的时候再把堆上的上下文（运行时栈内存的内容）拷贝到栈上，然后释放堆上的内存。
> 恢复栈顶只需要将当前线程的top_frame修改为恢复的greenlet的top_frame就行。

> > greenlet的基本原则
> > 1. 除了main greenbelt 之外，任意一个greenlet都有唯一一个父greenlet。
> > 2. 当前greenlet执行完毕，回到自己的父greenlet。
> > 3. 可以通过switch放的不同参数实现不同greenlet之间的传递数据。
> > greenlet实现的关键是先切c函数的栈，切换和恢复c的栈需要将**%ebp**(函数栈底)、**%esp**(函数栈顶)等寄存器的值保存到本地变量，恢复的时候就可以通过从堆上拷贝的内存，来恢复寄存器的值，达到恢复上下文的目的。
---- 
**python gevent 实现原理**

gevent 1.0版本之后底层实现是libev，基于greenlet实现。
使用hub调度其它的greenlet实例，hub也是一个greenlet。这么设计的原因：
> hub是事件驱动的核心，每次切换到hub后将继续循环事件，如果在一个greenlet中不出来，其他的greenlet得不到调用。
>  处理起来会更简单，每次只需要维持hub和当前greenlet，不用考虑各个greenlet之间的关系。
**gevent.sleep发生了什么？**
> 向事件循环注册当前greenlet的switch函数
> 切换到hub，运行主事件循环

**gevent.spawn 和gevent.join原理？**
> gevent.spawn 其实就是Greenlet.spawn，所以gevent就是创建一个greenlet，并将greenlet的switch()加入到hub主循环回调。

> join 语句会保存当前greenlet.switch 到一个队列中，并注册_notify_links回调，然后切换会hub，在notify_links 回调中将依次调用先前注册在队列中的回调。
**Python 解释器的实现原理？**

**引用**
[https://cyrusin.github.io/2016/07/28/greenlet-20150728/][1]

[1]:	https://cyrusin.github.io/2016/07/28/greenlet-20150728/