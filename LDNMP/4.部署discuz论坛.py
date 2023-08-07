import paramiko

servers = [

    {"name": "吉隆坡", "hostname": "1.1.1.1", "port": 22, "username": "root", "password": "123456", "dbrootpasswd": "webroot", "dbuse": "one", "dbusepasswd": "yyds", "domain": "a1.yuming.com", "dbname": "db1"},    

]


# 定义更新操作
def update_server(name, hostname, port, username, password, domain, dbrootpasswd, dbuse, dbname ):
    try:

        # 连接服务器
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname, port=port, username=username, password=password)


        stdin, stdout, stderr = client.exec_command("docker stop nginx")
        stdout.channel.recv_exit_status()  # 等待命令执行完成


        cert_command = (
            "curl https://get.acme.sh | sh && "
            "~/.acme.sh/acme.sh --register-account -m xxxx@gmail.com --issue -d {} "
            "--standalone --key-file /home/web/certs/{}_key.pem --cert-file /home/web/certs/{}_cert.pem --force"
        ).format(domain, domain, domain)

        # 使用 client.exec_command 执行命令，并将标准输出和标准错误重定向到 /dev/null
        stdin, stdout, stderr = client.exec_command(f"{cert_command} > /dev/null 2>&1")

        # 等待命令执行完成
        stdout.channel.recv_exit_status()


        stdin, stdout, stderr = client.exec_command("docker start nginx")
        stdout.channel.recv_exit_status()  # 等待命令执行完成



        stdin, stdout, stderr = client.exec_command('wget -O /home/web/conf.d/' + domain + '.conf https://raw.githubusercontent.com/kejilion/nginx/main/discuz.com.conf && \
                                                    sed -i "s/yuming.com/' + domain + '/g" /home/web/conf.d/' + domain + '.conf')
    
        stdout.channel.recv_exit_status()  # 等待命令执行完成


        # 使用字符串拼接来组织命令，增加可读性
        command = (
            'cd /home/web/html/ && '
            'mkdir {} && '
            'cd {} && '
            'wget https://github.com/kejilion/Website_source_code/raw/main/Discuz_X3.5_SC_UTF8_20230520.zip && '
            'unzip Discuz_X3.5_SC_UTF8_20230520.zip && '
            'rm Discuz_X3.5_SC_UTF8_20230520.zip'
        ).format(domain, domain)

        command = f"{command} > /dev/null 2>&1"

        stdin, stdout, stderr = client.exec_command(command)
        
        stdout.channel.recv_exit_status()

        stdin, stdout, stderr = client.exec_command('docker exec nginx chmod -R 777 /var/www/html && docker exec php chmod -R 777 /var/www/html && docker exec php74 chmod -R 777 /var/www/html')
        stdout.channel.recv_exit_status()  # 等待命令执行完成
   

        command = "docker exec mysql mysql -u root -p'{}' -e 'CREATE DATABASE {}; GRANT ALL PRIVILEGES ON {}.* TO \"{}\"@\"%\";'".format(dbrootpasswd,dbname,dbname,dbuse)
        stdin, stdout, stderr = client.exec_command(command)
        stdout.channel.recv_exit_status()  # 等待命令执行完成


        stdin, stdout, stderr = client.exec_command("docker restart php && docker restart php74 && docker restart nginx ")
        stdout.channel.recv_exit_status()  # 等待命令执行完成


        print(f"您的discuz论坛搭建好啦！\nhttps://{domain}")
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
    dbname = server["dbname"]
    dbrootpasswd = server["dbrootpasswd"]     
    dbuse = server["dbuse"]    
    update_server(name, hostname, port, username, password, domain, dbrootpasswd, dbuse, dbname )

# 等待用户按下任意键后关闭窗口
input("按任意键关闭窗口...")


