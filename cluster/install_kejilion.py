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
        stdin, stdout, stderr = client.exec_command("curl -sS -O https://raw.githubusercontent.com/kejilion/sh/main/kejilion.sh && chmod +x kejilion.sh && ./kejilion.sh")
        stdin.flush()

         # 暂停一段时间以等待安装程序接受输入
        time.sleep(1)
        
        # 中文
        stdin.write('y\n')
        stdin.flush()

         # 暂停一段时间以等待安装程序接受输入
        time.sleep(1)

        # 中文
        stdin.write('0\n')
        stdin.flush()
        
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
