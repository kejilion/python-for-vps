import paramiko

servers = [

    {"name": "吉隆坡", "hostname": "1.1.1.1", "port": 22, "username": "root", "password": "123456", "dbrootpasswd": "webroot", "dbuse": "one", "dbusepasswd": "yyds", "domain": "a1.yuming.com", "dbname": "db1"},    

]


# 定义更新操作
def update_server(name, hostname, port, username, password, domain, dbrootpasswd, dbuse, dbusepasswd):
    try:

        # 连接服务器
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname, port=port, username=username, password=password)


        print(f"{name} 更新系统")
        stdin, stdout, stderr = client.exec_command("DEBIAN_FRONTEND=noninteractive apt update -y && DEBIAN_FRONTEND=noninteractive apt full-upgrade -y && apt install -y curl wget sudo socat unzip tar htop")

        stdout.channel.recv_exit_status()  # 等待命令执行完成

        # 检查执行状态
        if stderr.channel.recv_exit_status() == 0:
            print("完成")
        else:
            print("失败")

        
        print()


        print(f"{name} 安装 Docker")
        stdin, stdout, stderr = client.exec_command("curl -fsSL https://get.docker.com | sh")

        stdout.channel.recv_exit_status()  # 等待命令执行完成


        stdin, stdout, stderr = client.exec_command('curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose && chmod +x /usr/local/bin/docker-compose')

        stdout.channel.recv_exit_status()  # 等待命令执行完成

        # 检查执行状态
        if stderr.channel.recv_exit_status() == 0:
            print("完成")
        else:
            print("失败")

        print()

        stdin, stdout, stderr = client.exec_command("cd /home && mkdir -p web/html web/mysql web/certs web/conf.d web/redis && touch web/docker-compose.yml")

        stdout.channel.recv_exit_status()  # 等待命令执行完成


        command = '''wget -O /home/web/docker-compose.yml https://raw.githubusercontent.com/kejilion/docker/main/LNMP-docker-compose-4.yml && \
                     sed -i "s/webroot/{}/g" /home/web/docker-compose.yml && \
                     sed -i "s/kejilionYYDS/{}/g" /home/web/docker-compose.yml && \
                     sed -i "s/kejilion/{}/g" /home/web/docker-compose.yml'''.format(dbrootpasswd, dbusepasswd, dbuse)

        stdin, stdout, stderr = client.exec_command(command)

        stdout.channel.recv_exit_status()  # 等待命令执行完成

        stdin, stdout, stderr = client.exec_command('iptables -P INPUT ACCEPT && \
                                                    iptables -P FORWARD ACCEPT && \
                                                    iptables -P OUTPUT ACCEPT && \
                                                    iptables -F')

        stdout.channel.recv_exit_status()  # 等待命令执行完成




        print(f"{name} 启动环境")
        stdin, stdout, stderr = client.exec_command('cd /home/web && docker-compose up -d')

        stdout.channel.recv_exit_status()  # 等待命令执行完成

        # 检查执行状态
        if stderr.channel.recv_exit_status() == 0:
            print("完成")
        else:
            print("失败")

        print()

        print(f"{name} PHP最新版配置")

        command = (
            "docker exec php apt update && "
            "docker exec php apt install -y libmariadb-dev-compat libmariadb-dev libzip-dev libmagickwand-dev imagemagick && "
            "docker exec php docker-php-ext-install mysqli pdo_mysql zip exif gd intl bcmath opcache && "
            "docker exec php pecl install imagick && "
            "docker exec php sh -c 'echo \"extension=imagick.so\" > /usr/local/etc/php/conf.d/imagick.ini' && "
            "docker exec php pecl install redis && "
            "docker exec php sh -c 'echo \"extension=redis.so\" > /usr/local/etc/php/conf.d/docker-php-ext-redis.ini'"
        )

        stdin, stdout, stderr = client.exec_command(command)

        stdout.channel.recv_exit_status()  # 等待命令执行完成

        # 检查执行状态
        if stderr.channel.recv_exit_status() == 0:
            print("完成")
        else:
            print("失败")

        print()

        print(f"{name} PHP7.4配置")

        command = (
            "docker exec php74 apt update && "
            "docker exec php74 apt install -y libmariadb-dev-compat libmariadb-dev libzip-dev libmagickwand-dev imagemagick && "
            "docker exec php74 docker-php-ext-install mysqli pdo_mysql zip gd intl bcmath opcache && "
            "docker exec php74 pecl install imagick && "
            "docker exec php74 sh -c 'echo \"extension=imagick.so\" > /usr/local/etc/php/conf.d/imagick.ini' && "
            "docker exec php74 pecl install redis && "
            "docker exec php74 sh -c 'echo \"extension=redis.so\" > /usr/local/etc/php/conf.d/docker-php-ext-redis.ini'"
        )

        stdin, stdout, stderr = client.exec_command(command)

        stdout.channel.recv_exit_status()  # 等待命令执行完成

        # 检查执行状态
        if stderr.channel.recv_exit_status() == 0:
            print("完成")
        else:
            print("失败")

        print()
        print()        

        stdin, stdout, stderr = client.exec_command('docker restart php && docker restart php74')

        stdout.channel.recv_exit_status()  # 等待命令执行完成


        stdin, stdout, stderr = client.exec_command('rm /home/web/docker-compose.yml')

        stdout.channel.recv_exit_status()  # 等待命令执行完成

        # 检查执行状态
        if stderr.channel.recv_exit_status() == 0:
            print(f"搭建完成")
        else:
            print(f"搭建失败")

        print()
        print()

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
    dbrootpasswd = server["dbrootpasswd"]
    dbuse = server["dbuse"]
    dbusepasswd = server["dbusepasswd"]
    update_server(name, hostname, port, username, password, domain, dbrootpasswd, dbuse, dbusepasswd)

# 等待用户按下任意键后关闭窗口
input("按任意键关闭窗口...")


