import os
import paramiko

# 服务器配置，根据您的需求修改
server_list = [
    {"name": "美国", "ip": "1.1.1.1", "port": 22, "username": "root", "password": "123456", "remote_path": "/home/"},
    #{"name": "美国", "ip": "1.1.1.1", "port": 22, "username": "root", "password": "123456", "remote_path": "/home/"},
          
    # 添加更多服务器配置
]

# 本地目录路径，根据您的需求修改
local_path = r"D:\kejilion\yyds"

def upload_to_remote(local_path, server):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    print("连接服务器：", server["name"])
    # 连接远程服务器
    ssh.connect(server["ip"], server["port"], server["username"], server["password"])

    print("创建所需目录")
    # 递归创建远程服务器上的内部目录
    for root, dirs, files in os.walk(local_path):
        for dir in dirs:
            remote_dir_path = os.path.join(server["remote_path"], os.path.relpath(os.path.join(root, dir), local_path)).replace("\\", "/")

            # 检查远程目录是否存在，如果不存在则创建
            try:
                sftp = ssh.open_sftp()
                sftp.stat(remote_dir_path)
                sftp.close()
            except IOError:
                ssh.exec_command("mkdir -p {}".format(remote_dir_path))

    sftp = ssh.open_sftp()

    total_files = sum([len(files) for _, _, files in os.walk(local_path)])
    uploaded_files = 0

    print("开始传输文件")
    for root, dirs, files in os.walk(local_path):
        for file in files:
            local_file_path = os.path.join(root, file)
            remote_file_path = os.path.join(server["remote_path"], os.path.relpath(local_file_path, local_path)).replace("\\", "/")

            # 检查远程文件是否存在，以及大小和修改时间是否变动
            try:
                remote_file_stat = sftp.stat(remote_file_path)
                local_file_stat = os.stat(local_file_path)

                if remote_file_stat.st_size == local_file_stat.st_size and \
                   remote_file_stat.st_mtime >= local_file_stat.st_mtime:
                    print("跳过文件：", local_file_path)  # 文件大小和修改时间未变动，跳过传输
                    continue
            except IOError:
                pass

            print("传输文件：", local_file_path, " -> ", remote_file_path)
            sftp.put(local_file_path, remote_file_path)
            uploaded_files += 1
            print("传输进度：{}/{}".format(uploaded_files, total_files))  # 显示上传进度
    print("传输完成")


    sftp.close()
    ssh.close()

# 上传文件到每个远程服务器
for server in server_list:
    upload_to_remote(local_path, server)


# 等待用户按下任意键后关闭窗口
input("按任意键关闭窗口...")