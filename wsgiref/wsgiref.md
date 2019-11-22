### WSGI规范
* WSGI规范如下：

> * 服务器的请求处理程序中要调用符合WSGI规范的网关接口；
> * 网关接口调用应用程序，并且要定义start_response(status, headers)函数，用于返回响应；
> * 应用程序中实现一个函数或者一个可调用对象webapp(environ, start_response)。其中environ是环境设置的字典，由服务器和WSGI网关接口设置，start_response是由网关接口定义的函数。
### wsgiref包
* wsgiref包为实现WSGI标准提供了一个参考，它可以作为独立的服务器测试和调试应用程序。在实际的生产环境中尽量不要使用。wsgiref包含有以下模块：
1. simple_server模块 ——simple_server模块实现了可以运行单个WSGI应用的简单的HTTP服务器。
2. headers模块 ——管理响应首部的模块。
3. handlers模块 ——符合WSGI标准的Web服务网关接口实现。该模块包含了一些处理程序对象，用来设置WSGI执行环境，以便应用程序能够在其他的Web服务器中运行。
4. validate模块 ——“验证包装”模块，确保应用程序和服务器都能够按照WSGI标准进行操作。
5. util模块 ——一些有用的工具集
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190506205959203.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzgyOTYzMw==,size_16,color_FFFFFF,t_70)
* 逻辑流程
 1. 服务器创建socket，监听端口，等待客户端连接。
 2. 当有请求来时，服务器解析客户端信息放到环境变量environ中，并调用绑定的handler来处理请求。
 3. handler解析这个http请求，将请求信息例如method，path等放到environ中。
 4. wsgi handler再将一些服务器端信息也放到environ中，最后服务器信息，客户端信息，本次请求信息全部都保存到了环境变量environ中。
 5. wsgi handler 调用注册的wsgi app，并将environ和回调函数传给wsgi app
 6. wsgi app 将reponse header/status/body 回传给wsgi handler
 7. 最终handler还是通过socket将response信息塞回给客户端。
*![在这里插入图片描述](https://img-blog.csdnimg.cn/20190507161342283.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzgyOTYzMw==,size_16,color_FFFFFF,t_70)
```python
def demo_app(environ, start_response):
    from StringIO import StringIO
    stdout = StringIO()
    print(>>stdout, "Hello world!")
    print(>>stdout)
    h = environ.items()
    h.sort()
    for k, v in h:
        print(>>stdout, k, '=', repr(v))
    start_response("200 OK", [('Content-Type', 'text/plain')])
    return [stdout.getvalue()]


def make_server(
    host, port, app, server_class=WSGIServer, handler_class=WSGIRequestHandler
):
    """Create a new WSGI server listening on `host` and `port` for `app`"""
    server = server_class((host, port), handler_class)
    server.set_app(app)
    return server


httpd = make_server('localhost', 8002,  demo_app)
httpd.serve_forever()  # 使用select
```
