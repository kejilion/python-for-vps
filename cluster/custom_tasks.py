import time
import paramiko
from servers import servers

# 定义更新操作
def update_server(name, hostname, port, username, password):
    try:
        # 连接服务器
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname, port=port, username=username, password=password)
        print(f"{name} 已连接")

        # 设置 DEBIAN_FRONTEND 环境变量
        stdin, stdout, stderr = client.exec_command("Customtasks")

        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_ready():
                print(stdout.channel.recv(1024).decode(), end="")

        # 检查更新状态
        if stderr.channel.recv_exit_status() == 0:
            print(f"成功")
        else:
            print(f"失败")


        # 关闭 SSH 连接
        client.close()

    except Exception as e:
        print(f"连接 {name} 失败\n")

# 遍历服务器列表，逐一更新
for server in servers:
    name = server["name"]
    hostname = server["hostname"]
    port = server["port"]
    username = server["username"]
    password = server["password"]
    update_server(name, hostname, port, username, password)

print("")
input("任务执行已全部结束")
