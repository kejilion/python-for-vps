
import time
import paramiko

# 定义服务器列表，包括服务器名称、IP地址、端口号、用户名、密码和解析好的域名
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



        # 执行步骤1: 更新操作
        print(f" {name} 建立连接")
        stdin, stdout, stderr = client.exec_command("apt update -y && apt install -y curl wget sudo socat htop")
        
        print(f"正在更新:")
        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_ready():
                print(stdout.channel.recv(1024).decode(), end="")

        # 检查执行状态
        if stderr.channel.recv_exit_status() == 0:
            print(f"更新成功")
        else:
            print(f"更新失败")
        
        print()


        # 设置 DEBIAN_FRONTEND 环境变量
        stdin, stdout, stderr = client.exec_command("wget -N https://raw.githubusercontent.com/fscarmen/warp/main/menu.sh && bash menu.sh [option] [lisence]")
        print(f"{name} 开始解锁ChatGPT:")


        # 暂停一段时间以等待安装程序接受输入
        time.sleep(10)

        # 中文
        stdin.write('2\n')
        stdin.flush()

        # 暂停一段时间以等待安装程序接受输入
        time.sleep(20)

        # 开启v6
        stdin.write('2\n')
        stdin.flush()

        # 暂停一段时间以等待安装程序接受输入
        time.sleep(2)

        # 使用免费账户
        stdin.write('1\n')
        stdin.flush()

        # 暂停一段时间以等待安装程序接受输入
        time.sleep(2)

        # 优先v6
        stdin.write('2\n')
        stdin.flush()


        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_ready():
                print(stdout.channel.recv(8192).decode(), end="")


        print(f"解锁成功")


        # 关闭 SSH 连接
        client.close()

 
      
    
    except Exception as e:
        print(f"连接 {name} 失败\n\n")

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
