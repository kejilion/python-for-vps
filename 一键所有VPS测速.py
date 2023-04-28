

import paramiko
import speedtest

# 定义服务器列表，包括服务器名称、IP地址、端口号、用户名和密码
servers = [
    {"name": "美国", "hostname": "1.1.1.1", "port": 22, "username": "root", "password": "123456"},   
    {"name": "不丹", "hostname": "1.1.1.1", "port": 22, "username": "root", "password": "123456"},   
    {"name": "毛里求斯", "hostname": "1.1.1.1", "port": 22, "username": "root", "password": "123456"},   
    # 添加更多服务器
]

def get_speedtest_results(name, hostname, port, username, password):
    try:
        # 连接服务器
        print(f"在 {name} 服务器上测速")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname, port=port, username=username, password=password)

        # 在服务器上安装 speedtest-cli
        stdin, stdout, stderr = client.exec_command(f"echo {password} | sudo -S apt-get install speedtest-cli -y")
        # while not stdout.channel.exit_status_ready():
        #     if stdout.channel.recv_ready():
        #         print(stdout.channel.recv(1024).decode(), end="")
        # if stderr.channel.recv_exit_status() == 0:
        #     print("speedtest-cli 安装成功")
        # else:
        #     print("speedtest-cli 安装失败")
        #     return

        # 测延迟
        print("开始测速...")
        stdin, stdout, stderr = client.exec_command("ping -c 4 202.96.209.133")
        output = stdout.read().decode()
        if "packet loss" in output:
            packet_loss = output.split("packet loss")[0].split("\n")[-2].split("%")[0]
        else:
            packet_loss = 0
        if "min/avg/max/mdev" in output:
            rtt = output.split("min/avg/max/mdev")[1].split("\n")[0].split("/")
            min_rtt, avg_rtt, max_rtt, mdev_rtt = rtt
            print(f"延迟：{avg_rtt}ms")
        else:
            print("测延迟失败")

        # 进行速度测试
        st = speedtest.Speedtest()
        st.get_best_server()
        download_speed = st.download() / 1024 / 1024  # Mbps
        print(f"下载速度为：{download_speed:.2f} Mbps")
        upload_speed = st.upload() / 1024 / 1024  # Mbps
        print(f"上传速度为：{upload_speed:.2f} Mbps")

        # 删除 speedtest-cli
        stdin, stdout, stderr = client.exec_command(f"echo {password} | sudo -S apt-get remove speedtest-cli -y")
        # while not stdout.channel.exit_status_ready():
        #     if stdout.channel.recv_ready():
        #         print(stdout.channel.recv(1024).decode(), end="")
        # if stderr.channel.recv_exit_status() == 0:
        #     print("speedtest-cli 删除成功")
        # else:
        #     print("speedtest-cli 删除失败")

        # 关闭 SSH 连接
        client.close()
        print("测试完成")

        print()

    except Exception as e:
        print(f"连接服务器 {name} 失败: {e}")


# 遍历服务器列表，逐一更新
for server in servers:
    name = server["name"]
    hostname = server["hostname"]
    port = server["port"]
    username = server["username"]
    password = server["password"]
    get_speedtest_results(name, hostname, port, username, password)

# 等待用户按下任意键后关闭窗口
input("按任意键关闭窗口...")
