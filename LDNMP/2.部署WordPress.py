import paramiko

servers = [

    {"name": "DOUS", "hostname": "0.0.0.0", "port": 22, "username": "root", "password": "123456","domain": "web1.yuming.com", "dbname": "web1_db", "remote_path": "/home/"},   
    {"name": "DOUS", "hostname": "0.0.0.0", "port": 22, "username": "root", "password": "123456","domain": "web2.yuming.com", "dbname": "web2_db", "remote_path": "/home/"},   
    {"name": "DOUS", "hostname": "0.0.0.0", "port": 22, "username": "root", "password": "123456","domain": "web3.yuming.com", "dbname": "web3_db", "remote_path": "/home/"},   

]


# 定义更新操作
def update_server(name, hostname, port, username, password, domain, dbname):
    try:

        # 连接服务器
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname, port=port, username=username, password=password)


        stdin, stdout, stderr = client.exec_command("docker stop nginx")
        print(f"{name} 停止nginx")
        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_ready():
                print(stdout.channel.recv(1024).decode(), end="")

        # 检查执行状态
        if stderr.channel.recv_exit_status() == 0:
            print(f"停止成功")
        else:
            print(f"停止失败")

        print()        


        print(f"{name} 申请证书")
        cert_command = (
            "curl https://get.acme.sh | sh && "
            "~/.acme.sh/acme.sh --register-account -m xxxx@gmail.com --issue -d {} "
            "--standalone --key-file /home/web/certs/{}_key.pem --cert-file /home/web/certs/{}_cert.pem --force"
        ).format(domain, domain, domain)

        # 使用 client.exec_command 执行命令，并将标准输出和标准错误重定向到 /dev/null
        stdin, stdout, stderr = client.exec_command(f"{cert_command} > /dev/null 2>&1")

        # 等待命令执行完成
        stdout.channel.recv_exit_status()

        # 检查命令的退出状态以确定是否成功执行
        if stdout.channel.recv_exit_status() == 0:
            print(f"申请成功")
        else:
            print(f"申请失败")

        print()


        stdin, stdout, stderr = client.exec_command("docker start nginx")
        print(f"{name} 启动nginx")
        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_ready():
                print(stdout.channel.recv(1024).decode(), end="")

        # 检查执行状态
        if stderr.channel.recv_exit_status() == 0:
            print(f"启动成功")
        else:
            print(f"启动失败")

        print()     




        print(f"{name} 配置nginx")
        stdin, stdout, stderr = client.exec_command('wget -O /home/web/conf.d/' + domain + '.conf https://raw.githubusercontent.com/kejilion/nginx/main/wordpress.com.conf && \
                                                    sed -i "s/yuming.com/' + domain + '/g" /home/web/conf.d/' + domain + '.conf')
        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_ready():
                print(stdout.channel.recv(1024).decode(), end="")

        # 检查执行状态
        if stderr.channel.recv_exit_status() == 0:
            print(f"配置成功")
        else:
            print(f"配置失败")

        print()

        print(f"{name} 下载网站源码-wp")
        # 使用字符串拼接来组织命令，增加可读性
        command = (
            'cd /home/web/html/ && '
            'mkdir {} && '
            'cd {} && '
            'wget https://cn.wordpress.org/wordpress-6.2.2-zh_CN.zip && '
            'unzip wordpress-6.2.2-zh_CN.zip && '
            'rm wordpress-6.2.2-zh_CN.zip && '
            'echo "define(\'FS_METHOD\', \'direct\'); define(\'WP_REDIS_HOST\', \'redis\'); define(\'WP_REDIS_PORT\', \'6379\');" >> /home/web/html/{}/wordpress/wp-config-sample.php'
        ).format(domain, domain, domain)

        command = f"{command} > /dev/null 2>&1"

        stdin, stdout, stderr = client.exec_command(command)
        
        stdout.channel.recv_exit_status()
        
        # 检查执行状态
        if stderr.channel.recv_exit_status() == 0:
            print(f"下载成功")
        else:
            print(f"下载失败")


        print()


        print(f"{name} 赋予文件权限")
        stdin, stdout, stderr = client.exec_command('docker exec nginx chmod -R 777 /var/www/html && docker exec php chmod -R 777 /var/www/html && docker exec php74 chmod -R 777 /var/www/html')
        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_ready():
                print(stdout.channel.recv(1024).decode(), end="")

        # 检查执行状态
        if stderr.channel.recv_exit_status() == 0:
            print(f"赋予成功")
        else:
            print(f"赋予失败")

        print()        


        print(f"{name} 创建数据库")
        # 使用双引号将密码部分括起来，并在双引号前加上反斜杠转义
        command = "docker exec mysql mysql -u root -p'webroot' -e 'CREATE DATABASE {}; GRANT ALL PRIVILEGES ON {}.* TO \"kejilion\"@\"%\";'".format(dbname,dbname)
        stdin, stdout, stderr = client.exec_command(command)

        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_ready():
                print(stdout.channel.recv(1024).decode(), end="")

        # 检查执行状态
        if stderr.channel.recv_exit_status() == 0:
            print(f"创建数据库成功")
        else:
            print(f"创建数据库失败")


        print(f"{name} 重启容器")
        stdin, stdout, stderr = client.exec_command("docker restart php && docker restart php74 && docker restart nginx ")

        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_ready():
                print(stdout.channel.recv(1024).decode(), end="")

        # 检查执行状态
        if stderr.channel.recv_exit_status() == 0:
            print(f"重启成功")
        else:
            print(f"重启失败")

        print()


        print()
        print()
        print(f"搭建完成\nhttps://{domain}")
        print()
        print()


        # print()
        # print()

        # 关闭 SSH 连接
        client.close()


    except Exception as e:
        print(f"连接 {name} 失败")


# 遍历服务器列表，逐一更新
for server in servers:
    name = server["name"]
    hostname = server["hostname"]
    port = server["port"]
    username = server["username"]
    password = server["password"]
    domain = server["domain"]
    dbname = server["dbname"]
    update_server(name, hostname, port, username, password, domain, dbname)

# 等待用户按下任意键后关闭窗口
input("按任意键关闭窗口...")


