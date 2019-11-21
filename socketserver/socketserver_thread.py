import threading
import socketserver

class ThreadEchoRH(socketserver.BaseRequestHandler):
    def handle(self):
        data=self.request.recv(1024)
        cur_thread=threading.currentThread()
        response=b'%s:%s'%(cur_thread.getName().encode(),data)
        self.request.send(response)
        return

class ThreadEchoServer(socketserver.ThreadingMixIn,socketserver.TCPServer):
    pass

if __name__ == "__main__":
    import socket
    