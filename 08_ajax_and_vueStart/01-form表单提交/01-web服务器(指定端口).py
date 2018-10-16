# 需求: 模拟服务器,接收客户端发送过来的请求报文,然后回复一个响应报文!(固定数据)
#   思路: 1.造tcp服务端socket   2.循环接收客户端发送来了的链接请求   3.接收和发送报文
import socket
import re
import time
# 需求4: 协程版,完成多任务...
import gevent
from gevent import monkey
monkey.patch_all()
import sys


# 造一个服务器对象类
class HTTPServer(object):
    # 初始化属性
    def __init__(self, port):
        # 1.1.造tcp服务端socket
        tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 1.2.端口复用
        tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # 1.3.绑定ip及端口
        ip_port1 = ('', port)
        tcp_server_socket.bind(ip_port1)
        # 1.4.变主动套接字为被动套接字
        tcp_server_socket.listen(128)
        print('服务器已开启...')
        # 绑定属性
        self.tcp_server_socket = tcp_server_socket

    # 开启服务
    def start(self):
        # 2.循环接收客户端发送来了的链接请求
        while True:
            service_client_socket, ip_port2 = self.tcp_server_socket.accept()
            # 打印一下,谁链接到了我们的服务器
            print(ip_port2, '已连接...')
            # 调用已经封装好的客户端处理器函数
            # client_handler(service_client_socket)
            # 协程实现多任务
            g1 = gevent.spawn(self.client_handler, service_client_socket)
            # 异步实现,不用join...(因为主线程不会执行完毕,有死循环...)

            # 协程版,要求不能出现单线程...
            # g1.join()
            # gevent.joinall()

    # 把这个方法,直接放到服务器类里面: (需要一些修饰...)
    # 封装一下, 服务端对客户端的请求处理
    def client_handler(self, service_client_socket):
        # 3.接收和发送报文
        request_data_bin = service_client_socket.recv(4096)
        # 浏览器地址中的端口号后面+/任何内容,在请求行中都可以获取到
        # print(request_data_bin.decode())
        print(request_data_bin)
        # 判断: 如果是空,说明客户端刚刚链接,可能由于网络原因就断开了,服务端也应该断开
        if not request_data_bin:
            print('客户端已断开!')
            service_client_socket.close()
            # 退出整个文件(封装后,就要退出函数了,而不是整个文件)
            return

        # 需求3: 如果客户端发送过来的请求报文存在内容,那么我们要发送给客户端指定页面里面的数据
        #   指定页面: 就存在请求行: GET /aaa/bbb/index.html HTTP/1.1\r\n...
        #   步骤: 把二进制转换成utf-8类型的字符串,然后取出里面的数据;
        request_str = request_data_bin.decode('utf-8')
        # 只有网络走的是HTTP协议,那么我们才能去获取
        #   把\r\n分割字符串, 获取一个列表,取出第一项,看看是否符合HTTP格式
        request_list = request_str.split('\r\n')
        # print(request_list[0])
        # 正则表达式进行校验: GET /hehehe.html HTTP/1.1
        obj = re.match(r'\w+\s+(\S+)\s+\S+', request_list[0])
        # 如果格式匹配没有通过,说明格式不对
        if obj is None:
            print('客户端发送的内容,不是HTTP协议...')
            service_client_socket.close()
            return

        # 获取资源路径   : request_list[0].split(' ')[1]
        request_url = obj.group(1)
        index = request_url.find("?")
        if index != -1:
            request_url = request_url[0:index]

        # 注意: 任何网站都有默认主页,如果客户端发送过来的报文,资源路径为: / 把么,我们默认添加一个主页
        if request_url == '/':
            # 添加一个默认主页
            request_url = '/index.html'
            # request_url = '/grand.html'

        # 发送响应报文
        response_head = 'Server: SZPWS/1.0\r\n'
        # response_body = 'I am lvchao, Hello world!!!\r\n'
        # 需求2: 返回固定页面(open() -- 然后存储到response_body)
        #   问题: 如果涉及到图片/音频/视频...  那么最好用二进制操作
        #   打开请求报文中指定的资源路径
        #       /hehehe.html

        # 需求3: 如果对方打开的页面不存在,那么不应该报错
        try:
            # 成功打开,头信息 200
            response_line = 'HTTP/1.1 200 OK\r\n'
            with open('./static'+request_url, 'rb') as file:
                # 获取的是二进制数据
                response_body = file.read()
        except Exception as e:
            # 没有打开,头信息 404 Not Found
            response_line = 'HTTP/1.1 404 Not Found\r\n'
            # 没有该页面,应该返回一个错误页面... (但是现在没有, 那就指定数据)
            #   因为发送的时候已经是二进制了
            response_body = ('error: ' + str(e)).encode()

        # 响应行           响应头           空行      响应体
        #                                                       转换为二进制         获取到的本身就是二进制
        response_data = (response_line + response_head + '\r\n').encode('utf-8') + response_body
        service_client_socket.send(response_data)
        # 不模拟长连接,模拟短连接
        service_client_socket.close()


# 封装一个主函数,所有的逻辑代码都写到这里面
def main():
    # 需求6: 获取外部传递过来的参数;
    # 1.尽量值传递一个参数过来
    #   ctrl+z: 退出页面,但是程序没有退出;(该端口还可以使用)
    #   ctrl+c: 退出页面,也退出程序;
    # print(sys.argv[1])
    if not len(sys.argv) == 2:
        print('输入的格式错误,正确的格式应该是: python3 文件名.py 端口号')
        return

    # 2.如果传递过来端口号,里面有非数字;(也不行)
    if not sys.argv[1].isdigit():
        print('端口号, 必须是整数!!!')
        return

    # 3.取值范围: [0-65535]
    if not 0<=int(sys.argv[1])<=65535:
        print('端口号必须在: [0-65535]之间!!!')
        return

    # 4.如果全部通过,那么要把端口号,传递到程序中

    # 需求5: 面向对象(a.把main方法里面的逻辑拆成 -- __init__()  start()  )
    h1 = HTTPServer(int(sys.argv[1]))
    # 开启服务
    h1.start()


# 程序入口
if __name__ == '__main__':
    main()
