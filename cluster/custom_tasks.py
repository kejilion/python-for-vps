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

        stdin, stdout, stderr = client.exec_command("Customtasks")
        
        # 读取输出
        output = stdout.read().decode()
        error = stderr.read().decode()

        # 检查命令执行状态
        exit_status = stdout.channel.recv_exit_status()
        if exit_status == 0:
            print(output)
            print(f"{name} 成功")
        else:
            print(error)
            print(f"{name} 失败")

        print("")
        print("")

        
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
