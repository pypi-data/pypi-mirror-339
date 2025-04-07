import socket


def get_local_ip(isIpv6: bool = False):
    """
    获取本机 IP 地址
    return: str
        本机 IP  地址
    """
    try:
        # 创建一个UDP套接字
        sock = socket.socket(socket.AF_INET6 if isIpv6 else socket.AF_INET, socket.SOCK_DGRAM)
        # 连接到一个公共的IP地址和端口，
        # 这不会发送任何数据，但是会为套接字分配一个本地地址
        sock.connect(("2001:4860:4860::8888" if isIpv6 else "8.8.8.8", 80))
        # 获取分配给套接字的本地IP地址
        local_ip = sock.getsockname()[0]
    finally:
        # 关闭套接字
        sock.close()
    return local_ip
