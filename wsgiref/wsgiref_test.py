from wsgiref.simple_server import make_server
def app_demo(environ,start_response):
    status='200 OK!'
    message=b'Hello World!'
    start_response(status,[('Content-Type','text/plain')])
    return [message]
if __name__ == "__main__":
    httpd=make_server('localhost',12345,app_demo)
    httpd.serve_forever()