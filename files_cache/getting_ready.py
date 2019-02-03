import os
import subprocess as sp
import socket
import paramiko

def ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

def getting_ready():
    global mec_me  # {'hostname': <hostname>, 'ip': <ip>}

    my_ip = ip_address()
    print('my ip = {}'.format(my_ip))

    cmd = ['cat /etc/hostname | cut -c 1-4']
    hostname = str(sp.check_output(cmd, shell=True), 'utf-8')[0:-1]
    print('hostname = {}'.format(hostname))

    cmd = ['netstat -nr | head -n 3 | tail -n 1 | cut -d " " -f 10']
    router_ip = str(sp.check_output(cmd, shell=True), 'utf-8')[0:-1]
    print('router_ip = {}'.format(router_ip))

    mec_me = {'hostname': hostname, 'ip': my_ip}

    cmd = "bash /home/mec/files_cache/hosts.sh {}/24 > names.txt".format(router_ip)

    os.system(cmd)
    mec_set = {my_ip, router_ip}
    fr = open('names.txt', 'r')

    ips = []
    f1 = fr.readlines()
    for i in f1:
        ips.append(i[0:-1])

    fr.close()

    available_host = set(ips) - mec_set

    for i in available_host:
        c = paramiko.SSHClient()

        un = 'mec'
        pw = 'password'
        port = 22

        c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        c.connect(i, port, un, pw)
        cmd = ('echo "' + "'{}' : '{}'".format(hostname, my_ip) + '" >> /home/mec/files_cache/mec_list.txt')

        stdin, stdout, stderr = c.exec_command(cmd)

getting_ready()
