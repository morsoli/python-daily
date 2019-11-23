from http.server import BaseHTTPRequestHandler,HTTPServer
from urllib import parse
        
import cgi
import io

from socketserver import ThreadingMixIn
import threading

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type','text/plain;charset=utf-8')
        self.end_headers()
        message=threading.currentThread().getName()
        self.wfile.write(message.encode('utf-8'))
        self.wfile.write(b'\n')

class ThreadHTTPServer(ThreadingMixIn,HTTPServer):
    pass

class GetHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed_path = parse.urlparse(self.path)
        message_parts = [
            'CLIENT VALUES:',
            'client_address={} ({})'.format(
                self.client_address,
                self.address_string()),
            'command={}'.format(self.command),
            'path={}'.format(self.path),
            'real path={}'.format(parsed_path.path),
            'query={}'.format(parsed_path.query),
            'request_version={}'.format(self.request_version),
            '',
            'SERVER VALUES:',
            'server_version={}'.format(self.server_version),
            'sys_version={}'.format(self.sys_version),
            'protocol_version={}'.format(self.protocol_version),
            '',
            'HEADERS RECEIVED:',
        ]
        for name, value in sorted(self.headers.items()):
            message_parts.append(
                '{}={}'.format(name, value.rstrip())
            )
        message_parts.append('')
        message = '\r\n'.join(message_parts)
        self.send_response(200)
        self.send_header('Content-Type',
                         'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(message.encode('utf-8'))

class POSTHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        form=cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={
                'REQUEST_METHOD':'POST',
                'CONTENT_TYPE':self.headers['Content-Type']
            }
        )
        self.send_response(200)
        self.send_header('Content-Type','text/plain;charset=utf-8')
        self.end_headers()
        out = io.TextIOWrapper(
            self.wfile,
            encoding='utf-8',
            line_buffering=False,
            write_through=True,
        )

        out.write('Client: {}\n'.format(self.client_address))
        out.write('User-agent: {}\n'.format(
            self.headers['user-agent']))
        out.write('Path: {}\n'.format(self.path))
        out.write('Form data:\n')

        # 表单信息内容回放
        for field in form.keys():
            field_item = form[field]
            if field_item.filename:
                # 字段中包含的是一个上传文件
                file_data = field_item.file.read()
                file_len = len(file_data)
                del file_data
                out.write(
                    '\tUploaded {} as {!r} ({} bytes)\n'.format(
                        field, field_item.filename, file_len)
                )
            else:
                # 通常形式的值
                out.write('\t{}={}\n'.format(
                    field, form[field].value))

        # 将编码 wrapper 到底层缓冲的连接断开， 
        # 使得将 wrapper 删除时， 
        # 并不关闭仍被服务器使用 socket 。
        out.detach()

if __name__ == '__main__':
    #server = HTTPServer(('localhost', 8080), GetHandler)
    #server = HTTPServer(('localhost', 8080), POSTHandler)
    server=ThreadHTTPServer(('localhost',8080),Handler)
    print('Starting server, use <Ctrl-C> to stop')
    server.serve_forever()