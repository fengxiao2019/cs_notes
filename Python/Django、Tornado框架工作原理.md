2. Django、Tornado框架工作原理
## Django vs Flask vs Tornado
- Django走的是大而全的方向，丰富的开发组件以及文档，开发效率高。
- Flask是轻量级的框架，自由，灵活，可扩展性很强，核心基于Werkzeug WSGI工具和jinja2模板引擎。
- Tornado走的是少而精的方向,性能优越。它最出名的是异步非阻塞的设计方式。Tornado的两大核心模块： 1.iostraem：对非阻塞式的socket进行简单的封装 2.ioloop：对I/O多路复用的封装，它实现了一个单例。
## WSGI
描述web server如何与web application通信的一种规范
WSGI协议主要包括server和application两部分：
WSGI server负责从客户端接收请求，将request转发给application，将application返回的response返回给客户端； WSGI application接收由server转发的request，处理请求，并将处理结果返回给server。
application中可以包括多个栈式的中间件(middlewares)，这些中间件需要同时实现server与application，因此可以在WSGI服务器与WSGI应用之间起调节作用：对服务器来说，中间件扮演应用程序，对应用程序来说，中间件扮演服务器。
## FBV vs CBV
FBV（function base views） 基于函数的视图
CBV（class base views） 基于类的视图
使用fbv的模式,在url匹配成功之后,会直接执行对应的视图函数
使用cbv模式,在url匹配成功之后,会找到视图函数中对应的类,然后这个类回到请求头中找到对应的Request Method
用户发送url请求,Django会依次遍历路由映射表中的所有记录,一旦路由映射表其中的一条匹配成功了,就执行视图函数中对应的函数名,这是fbv的执行流程

当服务端使用cbv模式的时候,用户发给服务端的请求包含url和method,这两个信息都是字符串类型 服务端通过路由映射表匹配成功后会自动去找dispatch方法,然后Django会通过dispatch反射的方式找到类中对应的方法并执行 类中的方法执行完毕之后,会把客户端想要的数据返回给dispatch方法,由dispatch方法把数据返回经客户端
![]()
1.wsgi,请求封装后交给web框架 （Flask、Django）
2.中间件，对请求进行校验或在请求对象中添加其他相关数据，例如：csrf、request.session
3.路由匹配 根据浏览器发送的不同url去匹配不同的视图函数
4.视图函数，在视图函数中进行业务逻辑的处理，可能涉及到：orm、templates =\> 渲染
5.中间件，对响应的数据进行处理。
6.wsgi,将响应的内容发送给浏览器。

