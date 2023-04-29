import paramiko

# 定义服务器列表，包括服务器名称、IP地址、端口号、用户名和密码
servers = [
    {"name": "美国", "hostname": "1.1.1.1", "port": 22, "username": "root", "password": "123456"},   
    {"name": "不丹", "hostname": "1.1.1.1", "port": 22, "username": "root", "password": "123456"},   
    {"name": "毛里求斯", "hostname": "1.1.1.1", "port": 22, "username": "root", "password": "123456"},   
    # 添加更多服务器
]

# 定义获取服务器信息的操作
def get_server_info(name, hostname, port, username, password):
    try:
        # 连接服务器
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname, port=port, username=username, password=password)

        # 获取Debian系统版本
        stdin, stdout, stderr = client.exec_command("cat /etc/os-release | grep PRETTY_NAME | awk -F= '{print $2}' | tr -d '\"'")
        debian_version = stdout.read().decode().strip()

        # 获取Linux内核版本
        stdin, stdout, stderr = client.exec_command("uname -r")
        kernel_version = stdout.read().decode().strip()

        # 获取CPU信息
        stdin, stdout, stderr = client.exec_command("cat /proc/cpuinfo | grep 'model name' | uniq")
        cpu_info = stdout.read().decode().strip()

        # 获取CPU占用量
        stdin, stdout, stderr = client.exec_command("top -bn1 | grep 'Cpu(s)' | awk '{print $2 + $4}'")
        cpu_usage = stdout.read().decode().strip() + "%"    

        # 获取CPU核心数
        stdin, stdout, stderr = client.exec_command("nproc")
        cpu_cores = stdout.read().decode().strip()

        # 获取内存信息
        stdin, stdout, stderr = client.exec_command("free -b | awk 'NR==2{printf \"%.2f/%.2f MB (%.2f%%)\", $3/1024/1024, $2/1024/1024, $3*100/$2 }'")
        mem_info = stdout.read().decode().strip()

        # 获取硬盘信息
        stdin, stdout, stderr = client.exec_command("df -h | awk '$NF==\"/\"{printf \"%d/%dGB (%s)\", $3,$2,$5}'")
        disk_info = stdout.read().decode().strip()
        
        # 打印服务器信息
        print(f"{name} 当前信息:")
        print(f"系统版本: {debian_version}")
        print(f"Linux版本: {kernel_version}")   
        print(f"CPU架构: {cpu_info}")
        print(f"CPU占用: {cpu_usage}")   
        print(f"CPU核心数: {cpu_cores}")             
        print(f"内存占用: {mem_info}")
        print(f"硬盘占用: {disk_info}")
 
        print()

        # 关闭 SSH 连接
        client.close()
    except Exception as e:
        print(f"连接服务器 {name} 失败")

# 遍历服务器列表，逐一获取信息
for server in servers:
    name = server["name"]
    hostname = server["hostname"]
    port = server["port"]
    username = server["username"]
    password = server["password"]
    get_server_info(name, hostname, port, username, password)

# 等待用户按下任意键后关闭窗口
input("按任意键关闭窗口...")
