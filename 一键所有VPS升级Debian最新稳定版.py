

import paramiko

# 定义服务器列表，包括服务器名称、IP地址、端口号、用户名和密码
servers = [
    {"name": "美国", "hostname": "1.1.1.1", "port": 22, "username": "root", "password": "123456"},   
    {"name": "不丹", "hostname": "1.1.1.1", "port": 22, "username": "root", "password": "123456"},   
    {"name": "毛里求斯", "hostname": "1.1.1.1", "port": 22, "username": "root", "password": "123456"},   
    # 添加更多服务器
]



# 定义更新操作
def update_server(name, hostname, port, username, password):
    try:
        # 连接服务器
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname, port=port, username=username, password=password)

        stdin, stdout, stderr = client.exec_command("DEBIAN_FRONTEND=noninteractive apt update -y && DEBIAN_FRONTEND=noninteractive apt full-upgrade -y")
        stdin.write('Y\n')  # 将默认响应设置为 Y（安装软件包维护者的版本）
        stdin.flush()  # 刷新输入流
        
        print(f"{name} 开始更新")
        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_ready():
                print(stdout.channel.recv(1024).decode(), end="")
        
        # 检查更新状态
        if stderr.channel.recv_exit_status() == 0:
            print(f"更新成功")
        else:
            print(f"更新失败")

        print()  

        stdin, stdout, stderr = client.exec_command("cat > /etc/apt/sources.list << EOF\ndeb http://deb.debian.org/debian stable main\ndeb-src http://deb.debian.org/debian stable main\n\ndeb http://deb.debian.org/debian-security/ stable-security main\ndeb-src http://deb.debian.org/debian-security/ stable-security main\n\ndeb http://deb.debian.org/debian stable-updates main\ndeb-src http://deb.debian.org/debian stable-updates main\nEOF")      
        print(f"{name} 导出官方更新源")
        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_ready():
                print(stdout.channel.recv(1024).decode(), end="")
        
        # 检查更新状态
        if stderr.channel.recv_exit_status() == 0:
            print(f"导入成功")
        else:
            print(f"导入失败")

        print()  

        stdin, stdout, stderr = client.exec_command("DEBIAN_FRONTEND=noninteractive apt update -y && DEBIAN_FRONTEND=noninteractive apt full-upgrade -y && apt install -y curl wget sudo socat htop")
        stdin.write('Y\n')  # 将默认响应设置为 Y（安装软件包维护者的版本）
        stdin.flush()  # 刷新输入流
        
        print(f"{name} 开始升级")
        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_ready():
                print(stdout.channel.recv(1024).decode(), end="")
        
        # 检查更新状态
        if stderr.channel.recv_exit_status() == 0:
            print(f"升级成功")
        else:
            print(f"升级失败")

        print()  

        stdin, stdout, stderr = client.exec_command("apt autoremove --purge -y && apt clean -y && apt autoclean -y && apt remove --purge $(dpkg -l | awk '/^rc/ {print $2}') -y && journalctl --rotate && journalctl --vacuum-time=1s && journalctl --vacuum-size=50M && apt remove --purge $(dpkg -l | awk '/^ii linux-(image|headers)-[^ ]+/{print $2}' | grep -v $(uname -r | sed 's/-.*//') | xargs) -y")

        print(f"{name} 开始清理")
        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_ready():
                print(stdout.channel.recv(1024).decode(), end="")
        
        # 检查更新状态
        if stderr.channel.recv_exit_status() == 0:
            print(f"清理成功")
        else:
            print(f"清理失败")

        print()  
   
        # 检查更新状态
        stdin, stdout, stderr = client.exec_command("reboot")
        print(f"{name} 重启服务器")
        print()  
        print()  

        # 关闭 SSH 连接
        client.close()


    except Exception as e:
        print(f"连接 {name} 失败")

        print()        
        print()                        

# 遍历服务器列表，逐一更新
for server in servers:
    name = server["name"]
    hostname = server["hostname"]
    port = server["port"]
    username = server["username"]
    password = server["password"]
    update_server(name, hostname, port, username, password)

# 等待用户按下任意键后关闭窗口
input("按任意键关闭窗口...")
