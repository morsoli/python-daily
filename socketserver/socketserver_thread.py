import threading
import socketserver
import os

class ThreadEchoRH(socketserver.BaseRequestHandler):
    def handle(self):
        data=self.request.recv(1024)
        cur_thread=threading.currentThread()
        response=b'%s:%s'%(cur_thread.getName().encode(),data) 
        self.request.send(response)
        return
class ProcessEchoRH(socketserver.BaseRequestHandler):
    def handle(self):
        data=self.request.recv(1024)
        response=b'%d:%s'%(os.getpid(),data)
        self.request.send(response)
        return
class ThreadEchoServer(socketserver.ThreadingMixIn,socketserver.TCPServer):
    pass

class ProcessEchoServer(socketserver.ForkingMixIn,socketserver.TCPServer):
    pass
if __name__ == "__main__":
    import socket
    import threading
    address=('localhost',12346)
    #server=ThreadEchoServer(address,ProcessEchoRH)
    server=ProcessEchoServer(address,ProcessEchoRH)
    print('the server address:',server.server_address)
    host,ip=server.server_address

    t=threading.Thread(target=server.serve_forever)
    t.setDaemon(True)
    t.start()
    print('current process num: ',os.getpid())

    c=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    c.connect((host,ip))

    message=b'Hello World!'
    ret=c.send(message)

    response=c.recv(1024)
    print('client recieve res: ',response)

    server.shutdown()
    c.close()
    server.socket.close()