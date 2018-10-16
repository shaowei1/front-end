import socket
import re
import sys
import multiprocessing


class WSGIServer(object):
    ''' 定义WSGI类 '''

    def __init__(self, port, documents_root, app):
        # create tcp socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # bind local information
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(("0.0.0.0", port))

        # set bind socket
        self.server_socket.listen(128)

        # set route of source
        self.documents_root = documents_root

        # set function(object) who need call web_frame
        self.app = app

    def run_forever(self):
        ''' run forever, waiting connect from browser then give server for browser'''

        while True:
            # waiting new user
            new_socket, new_addr = self.server_socket.accept()
            new_process = multiprocessing.Process(target=self.deal_with_request, args=(new_socket,))
            new_process.start()
            new_socket.close()

    def deal_with_request(self, new_socket):
        ''' use a process to finish the server for new client of browser'''

        while True:
            # accept request from browser
            request = new_socket.recv(1024).decode('utf-8')
            if not request:
                new_socket.close()
                return

            request_lines = request.splitlines()
            for i, line in enumerate(request_lines):
                print(i, line)

            # GET /login.html HTTP/1.1
            ret = re.match(r"([^/]*)([^ ]*)", request_lines[0])
            if ret:
                print("re deal data1: ", ret.group(1))
                print("re deal data2: ", ret.group(2))
                # get file name (contain route)
                file_name = ret.group(2)
                if file_name == "/":
                    file_name = '/index.html'

                # check whether contain address_paras "?code=000056$ingo=text"
                if "?" in file_name:
                    url_arr = file_name.split("?")
                    file_name = url_arr[0]
                    url_dat = url_arr[1]

                else:
                    url_dat = ''

            # if end not with "_data", so think it as a plain text, read and return
            # if end with "_data", then deliver to web frame for deal it
            if not file_name.endswith("_data"):
                try:
                    print(self.documents_root + file_name)
                    f = open(self.documents_root + file_name, "rb")
                except:
                    response_body = "sorry, 么有你要找的文件...."

                    response_header = "HTTP/1.1 404 Not Found\r\n"
                    response_header += "content-type:text/html; charset=utf-8\r\n"
                    response_header += "Content-Length: %d\r\n" % len(response_body)
                    response_header += "\r\n"

                    response = response_header + response_body

                    new_socket.send(response.encode("utf-8"))
                else:
                    content = f.read()
                    f.close()
                    response_body = content

                    response_line = "HTTP/1.1 200 OK\r\n"
                    response_header = "Content-Length:%d\r\n" % len(response_body)
                    response_header += "\r\n"

                    new_socket.send((response_line + response_header).encode('utf-8') + response_body)
            else:
                # save data that will give web frame
                env = dict()
                env["PATH_INFO"] = file_name
                env["URL_DAT"] = url_dat

                # call web frame's function
                response_body = self.app(env, self.set_response_headers)

                response_header = "HTTP/1.1 %s\r\n" % self.headers[0]
                for header_temp in self.headers[1]:
                    # response_header = "Content-Type:text/html; charset=utf-8\r\n"
                    response_header += "%s:%s\r\n" % (header_temp[0], header_temp[1])

                response_header += "Content-Length:%d\r\n" % len(response_body.encode("utf-8"))
                response_header += "\r\n"

                response = response_header + response_body

                new_socket.send(response.encode('utf-8'))

    def set_response_headers(self, status, headers):
        ''' set request line information'''
        # status 200 OK
        # heders [("Content-Type", "text/html")]
        # ["200 OK", [("Content-Type", "text/html")]
        self.headers = [status, headers]


g_static_root = "./static"
g_dynamic_root = "/"


def main():
    ''' main function'''

    # python3 server.py 8888 web:app
    if len(sys.argv) == 3:
        port = sys.argv[1]
        if port.isdigit():
            port = int(port)
        else:
            print("port is error")
            return

        # get web_frame's module_name and the function(object) name that ready for future
        # web:app
        web_frame_app_name = sys.argv[2]
    else:
        print("please run with : python3 xxxx.py 8888 web:app")
        return
    print("web port is: %d" % port)

    # web:app
    ret = re.match(r"([^:]+):(.*)", web_frame_app_name)
    if ret:
        frame_name = ret.group(1)
        app_name = ret.group(2)

    # add the file of saved web_frame to path route , so assure module no problems
    sys.path.append(g_dynamic_root)

    frame = __import__(frame_name)
    app = getattr(frame, app_name)

    http_server = WSGIServer(port, g_static_root, app)
    http_server.run_forever()


if __name__ == '__main__':
    main()
