import sqlite3
import hashlib
import os
import socket
import paramiko
from time import gmtime, strftime
import random
import time
import subprocess as sp
import psutil
import ping_code as pc
from matplotlib import pyplot as plt
import ast
from pyfiglet import Figlet


cache_size = 3
H = 0
M = 0
MH = 0
re_use = 0
ref = [2, 6, 4, 1, 2, 6, 3, 2, 0, 3, 4, 2, 6, 1, 5, 6, 2, 5, 2, 6, 4, 5, 6, 3, 6, 4, 0, 4, 4, 6]
# ref = [1, 5, 0, 3, 14, 7, 4, 17, 11, 19, 10, 7, 19, 9, 14, 2, 18, 0, 6, 2, 12, 11, 12, 10, 17, 9, 10, 7, 12, 6, 0, 6, 0, 5, 10, 17, 18, 8, 5, 0, 8, 8, 14, 4, 4, 0, 0, 14, 10, 14, 10, 15, 9, 7, 17, 6, 18, 2, 2, 18, 8, 1, 11, 14, 13, 3, 0, 5, 19, 6, 10, 0, 7, 8, 3, 3, 18, 10, 19, 6, 7, 9, 6, 10, 7, 9, 8, 15, 19, 17, 15, 15, 7, 2, 7, 17, 6, 9, 16, 9, 18, 16, 15, 18, 15, 5, 3, 4, 10, 14, 10, 9, 12, 16, 8, 3, 15, 3, 17, 6, 13, 13, 8, 8, 8, 10, 11, 13, 19, 0, 5, 19, 15, 5, 11, 14, 12, 10, 5, 2, 17, 8, 1, 11, 16, 5, 9, 6, 14, 11, 15, 14, 8, 8, 8, 18, 10, 12, 3, 17, 0, 13, 4, 18, 5, 19, 13, 19, 4, 12, 0, 16, 2, 16, 19, 0, 6, 13, 15, 12, 5, 16, 1, 16, 0, 9, 9, 1, 5, 14, 1, 6, 11, 2, 12, 5, 8, 19, 1, 9, 7, 2, 11, 15, 7, 2, 17, 14, 13, 16, 14, 2, 17, 10, 12, 14, 18, 1, 7, 8, 6, 7, 3, 18, 18, 9, 12, 6, 18, 16, 1, 16, 13, 9, 2, 8, 6, 14, 14, 14, 9, 5, 0, 18, 17, 15, 9, 2, 15, 7, 4, 18, 14, 11, 3, 1, 12, 17, 0, 15, 8, 12, 1, 8, 8, 18, 13, 11, 3, 5, 11, 18, 10, 15, 10, 3, 3, 7, 1, 13, 18, 5, 9, 7, 10, 6, 17, 14, 10, 10, 15, 7, 11, 16, 4, 4, 9, 2, 5, 14, 0, 2, 13, 19, 1, 10, 16, 16, 7, 10, 0, 4, 18, 5, 0, 19, 1, 0, 16, 0, 6, 9, 10, 6, 0, 17, 14, 6, 10, 1, 0, 9, 9, 10, 10, 11, 3, 15, 15, 5, 17, 19, 8, 2, 4, 3, 7, 7, 17, 8, 18, 5, 12, 12, 2, 14, 5, 17, 2, 10, 13, 13, 17, 7, 15, 19, 3, 8, 14, 16, 11, 12, 13, 3, 7, 11, 10, 17, 19, 11, 8, 14, 7, 15, 17, 14, 8, 15, 10, 19, 9, 9, 13, 14, 18, 7, 4, 13, 18, 16, 10, 7, 8, 13, 8, 16, 8, 11, 9, 9, 9, 2, 1, 0, 0, 17, 16, 4, 16, 4, 17, 2, 16, 5, 12, 4, 17, 6, 7, 9, 6, 17, 14, 18, 1, 8, 18, 0, 19, 16, 5, 2, 17, 18, 18, 2, 17, 4, 0, 16, 0, 9, 14, 13, 3, 9, 1, 13, 19, 18, 9, 7, 4, 15, 2, 5, 4, 7, 3, 9, 4, 3, 4, 7, 3, 18, 6, 2, 17, 3, 10, 0, 19, 19, 5, 6, 18, 9, 6, 3, 10, 7, 1, 0, 5, 12, 6, 15, 1, 8]

freq = {}
changing_freq = {}
window_size = 0


x_axis = []
y_axis = []


def make_hash_dic(host_ip, n):
    h_dic = {}   # {url: hash}
    kolour = ['r', 'g', 'c', 'k', 'b', 'm', 'y']
    col = {}
    for i in range(1, n+1):
        url = '{}/{}.html'.format(host_ip, i)
        hash_me = 'get {} HTTP/1.0'.format(url)
        y = str.encode(hash_me)
        ha = hashlib.md5(y)
        hash_no = ha.hexdigest()
        h_dic[url] = hash_no
        col[url] = kolour[i-1]
    return [h_dic, col]


def plot_performance():
    global H
    global M
    global MH
    global re_use

    fig5 = plt.figure('Cache Performance')

    fig5 = plt.clf()

    fig5 = plt.ion()
    name = ['Hits', 'Misses', 'Co-operative-Hits', 'Algo use']
    ypos = ([0, 1, 2, 3])
    values = [H, M, (H + MH), re_use]

    fig5 = plt.xticks(ypos, name)
    fig5 = plt.bar(ypos, values, align='center', color='m')
    fig5 = plt.title('Cache Performance')

    fig5 = plt.ylabel('values')

    fig5 = plt.pause(2)


def update_changing_freq():
    for key in freq.keys():
        x = key
        y = freq[key]
        if x in changing_freq.keys():
            changing_freq[x].append(y)
        else:
            changing_freq[x] = [y]


def plot_changing_freq():
    global changing_freq

    plot_dic = {}

    for key in hash_dic:
        if hash_dic[key] not in changing_freq:
            continue
        elif hash_dic[key] in changing_freq:
            rf = changing_freq[hash_dic[key]]
            plot_dic[key] = rf  # converts the dictionary from hash: frequency to web: frequency

    fig3 = plt.figure('Moving Relative Frequency')

    fig3 = plt.clf()
    fig3 = plt.ion()
    fig3 = plt.grid(True, color='k')
    for key in plot_dic.keys():
        fig3 = plt.plot(plot_dic[key], linewidth=5, label=key, color=colour[key])

    fig3 = plt.title('Changing frequency Graph')
    fig3 = plt.ylabel('URL')
    fig3 = plt.xlabel('Time (seconds)')
    fig3 = plt.legend()
    fig3 = plt.pause(2)


def local_cache_frequency():
    ip = ip_address()

    con = sqlite3.connect('/home/mec/cache.db')
    cur = con.cursor()
    cur.execute("select Hash from CacheTable where Host_ip ='" + ip + "'")
    data = cur.fetchall()
    '''
    data format

    [('7e7ea8d98195d1fcf6abe4f77e56730e',), ('26ff04f8463191809dcd9e8605bb952a',), ('d37269610dffb86e4925864b110e4d4e',)]
    '''
    d = []
    if len(data) == 0:
        con.close()
        return 'no items'
        pass
    else:
        for i in data:
            d.append(i[
                         0])  # cleaning data to d = ['7e7ea8d98195d1fcf6abe4f77e56730e', '26ff04f8463191809dcd9e8605bb952a', 'd37269610dffb86e4925864b110e4d4e']
        con.close()
        cache_dic = {}
        for i in d:
            cache_dic[i] = freq[i]  # creates a dictionary and tags the hash with its relative frequency

        plot_dic = {}

        for key in hash_dic:
            if hash_dic[key] not in cache_dic:
                continue
            elif hash_dic[key] in cache_dic:
                rf = cache_dic[hash_dic[key]]
                plot_dic[key] = rf  # converts the dictionary from hash: frequency to web: frequency

        return plot_dic


def plot_local_cache_freq():
    global changing_freq

    plot_dic = {}

    for key in hash_dic:
        if hash_dic[key] not in changing_freq:
            continue
        elif hash_dic[key] in changing_freq:
            rf = changing_freq[hash_dic[key]]
            plot_dic[key] = rf  # converts the dictionary from hash: frequency to web: frequency

    fig4 = plt.figure('Local Cache Frequency')

    fig4 = plt.clf()
    fig4 = plt.ion()
    fig4 = plt.grid(True, color='k')
    if local_cache_frequency() == 'no items':
        pass
    else:
        for key in plot_dic.keys():
            if key in local_cache_frequency():
                fig4 = plt.plot(plot_dic[key], linewidth=5, label=key, color=colour[key])

            fig4 = plt.title('Local Cache frequency Graph')
            fig4 = plt.ylabel('URL')
            fig4 = plt.xlabel('Time (seconds)')
            fig4 = plt.legend()
            fig4 = plt.pause(2)


def hash_to_web():
    global freq

    plot_dic = {}

    for key in hash_dic:
        if hash_dic[key] not in freq:
            continue
        elif hash_dic[key] in freq:
            rf = freq[hash_dic[key]]
            plot_dic[key] = rf

    return plot_dic


def plot_graphs():
    host = server_ip
    prev_t = 0
    rtt = pc.verbose_ping(host)
    next_t = psutil.cpu_percent(percpu=False)
    delta = abs(prev_t - next_t)
    prev_t = next_t
    plot_resource_util(rtt, delta)
    plot_relative_frequency()
    plot_changing_freq()
    plot_local_cache_freq()
    plot_performance()
    plt.show()


def plot_resource_util(x, y):
    fig1 = plt.figure('Resource Utilization')

    fig1 = plt.clf()
    x_axis.append(x)
    y_axis.append(y)
    fig1 = plt.ion()
    fig1 = plt.grid(True, color='k')
    fig1 = plt.plot(x_axis, linewidth=5, label='RTT')
    fig1 = plt.plot(y_axis, linewidth=5, label='CPU')
    fig1 = plt.title('CPU and RTT Utilization over Time')
    fig1 = plt.ylabel('CPU and RTT')
    fig1 = plt.xlabel('Time (seconds)')
    fig1 = plt.legend()
    fig1 = plt.pause(2)

    # plt.show()


def plot_relative_frequency():
    fig2 = plt.figure('Relative Frequency')
    fig2 = plt.clf()
    ret = hash_to_web()

    val = []
    keys = []
    cols = ['r', 'g', 'c', 'k', 'b', 'm', 'y']

    for i in ret.items():
        val.append(i[1])
        keys.append(i[0])

    explode = []
    for i in val:
        if i == max(val):
            explode.append(0.1)
        else:
            explode.append(0)

    fig2 = plt.ion()
    fig2 = plt.pie(val, labels=keys, autopct='%.3f%%', shadow=True, explode=explode, colors=cols)
    fig2 = plt.title('Relative Frequency')
    fig2 = plt.pause(2)


def get_hash(url):
    hash_me = 'get {} HTTP/1.0'.format(url)
    y = str.encode(hash_me)
    ha = hashlib.md5(y)
    hash_no = ha.hexdigest()
    calc_relative_freq(hash_no)
    check_cache(hash_no, url)


def ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


def calc_relative_freq(x):
    global freq
    global window_size

    window_size += 1
    alpha = 1 / window_size
    delta = alpha / (len(freq) + 1)
    if x not in freq.keys():
        for k in freq.keys():
            freq[k] -= delta
        freq[x] = alpha
    else:
        for k in freq.keys():
            if k != x:
                freq[k] -= delta
        freq[x] += (len(freq) - 1) * delta
    update_changing_freq()
    plot_graphs()


def get_time():
    y = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    return y


def check_cache(hash_no, url):
    try:
        global con
        con = sqlite3.connect('/home/mec/cache.db')
        cur = con.cursor()
        cur.execute("SELECT COUNT(*) FROM CacheTable WHERE Hash='" + hash_no + "'")
        d = cur.fetchone()
        r = d[0]
        if r == 0:
            fetch_from_source(hash_no, url)
        else:
            fetch_from_cache(hash_no)

    except sqlite3.Error as e:
        if con:
            con.rollback()
            print('Error in check_cache: {}'.format(e))

    finally:
        if con:
            con.close()


def fetch_from_source(hash_no, url):
    global M
    cmd = "curl {}".format(url)
    os.system(cmd)

    prepare_db()  # CHECKS IF CACHE IS FULL AND ELIMINATES VICTIM

    cmd = "echo `curl {}` > /home/mec/cache/{}.html".format(url, hash_no)  # CACHES DATA FROM SOURCE
    os.system(cmd)
    cmd_line = 'echo "password" | sudo -S -H -u mec bash -c "ipfs add /home/mec/cache/{}.html | cut -c 7-52"'.format(hash_no)
    cmd = [cmd_line]
    ipfs_hash = str(sp.check_output(cmd, shell=True), 'utf-8')[0:-1]
    print('-----------------------------------')
    print('Cache Miss')
    print('-----------------------------------')
    M += 1
    update_local_database(hash_no, ipfs_hash)


def update_local_database(hash_no, ipfs_hash):
    try:
        global con

        con = sqlite3.connect('/home/mec/cache.db')
        cur = con.cursor()
        cache_time = get_time()
        ip = mec_me['ip']
        path = '/home/mec/cache/{}.html'.format(hash_no)
        data = (ipfs_hash, hash_no, path, cache_time, ip)
        cur.execute("INSERT INTO CacheTable VALUES(?, ?, ?, ?, ?)", data)
        con.commit()
        cur.execute("SELECT * FROM CacheTable")
        d = cur.fetchall()

        for row in d:
            print(row)

        update_mec_database(ipfs_hash, hash_no, path, cache_time, ip)
        con.close()

    except sqlite3.Error as e:
        print('Error in cache_update: {}'.format(e))


def update_mec_database(ipfs_hash, hash_no, path, cache_time, host_ip):
    for i in mec_list:
        c = paramiko.SSHClient()

        un = 'mec'
        pw = 'password'
        port = 22

        c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        c.connect(mec_list[i], port, un, pw)
        cmd = 'python3 /home/mec/files_cache/db_manage.py insert "{}" "{}" "{}" "{}" "{}"'.format(ipfs_hash, hash_no, path, cache_time, host_ip)

        stdin, stdout, stderr = c.exec_command(cmd)


def fetch_from_cache(hash_no):
    try:
        global con
        global H
        con = sqlite3.connect('/home/mec/cache.db')
        cur = con.cursor()
        cur.execute("SELECT Ipfs_Hash, Host_ip FROM CacheTable WHERE Hash='" + hash_no + "'")
        ipfs_ip = cur.fetchall()     # [('927EHD8IEHD29EIDH', '192.168.1.2'), ('927EHD8IEHD29EIDH', '192.168.1.3'), ('927EHD8IEHD29EIDH', '192.168.1.4')]
        host_ips = []
        for i in ipfs_ip:
            host_ips.append(i[1])

        if mec_me['ip'] in host_ips:
            time_ = get_time()
            cmd = "cat /home/mec/cache/{}.html".format(hash_no)
            os.system(cmd)
            print('-----------------------------------')
            print('Cache Hit from localhost')
            print('-----------------------------------')
            H += 1
            cur.execute("update CacheTable set DateTime = '" + time_ + "' where Hash = '" + hash_no + "' and Host_ip = '" + mec_me['ip'] + "';")
            con.close()
        else:
            fetch_from_mec(hash_no, ipfs_ip[0][0])

    except sqlite3.Error as e:
        print('Error in cache_update: {}'.format(e))


def frequently_used(hash_no):
    host_ip = mec_me['ip']
    global freq
    try:
        global con
        con = sqlite3.connect('/home/mec/cache.db')
        cur = con.cursor()
        cur.execute("SELECT Hash FROM CacheTable WHERE Host_ip ='" + host_ip + "'")
        host_ip_list = cur.fetchall()
        li = []
        for i in range(len(host_ip_list)):
            li.append(host_ip_list[i - 1][0])
        fre_li = []
        for i in li:
            fre_li.append(freq[i])
        min_freq = min(fre_li)

        if min_freq > freq[hash_no]:
            return 'no'
        elif min_freq < freq[hash_no]:
            y = fre_li.index(min_freq)
            delete_least_frequent_mec(li[y], host_ip)
            delete_least_frequent_locally(li[y], host_ip)
            return 'yes'

    except sqlite3.Error as e:
        print('Error in cache_update: {}'.format(e))


def delete_least_frequent_locally(hash_no, host_ip):
    try:
        con = sqlite3.connect('/home/mec/cache.db')
        cur = con.cursor()
        cur.execute("SELECT Ipfs_Hash FROM CacheTable WHERE Hash = '" + hash_no + "' AND Host_ip = '" + host_ip + "'")
        ipfs_hash = cur.fetchone()[0]

        cur.execute("DELETE FROM CacheTable WHERE Hash = '" + hash_no + "' AND Host_ip = '" + host_ip + "'")
        cmd = 'echo "password" | sudo -S -H -u mec bash -c "ipfs pin rm -r {} ; ipfs repo gc"'.format(ipfs_hash)
        os.system(cmd)
        con.commit()
        con.close()
        cmd = 'rm /home/mec/cache/{}.html'.format(hash_no)
        os.system(cmd)

    except sqlite3.Error as e:
        print('Error in cache_update: {}'.format(e))


def delete_least_frequent_mec(hash_no, host_ip):
    for i in mec_list:
        c = paramiko.SSHClient()

        un = 'mec'
        pw = 'password'
        port = 22

        c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        c.connect(mec_list[i], port, un, pw)
        cmd = 'python3 /home/mec/files_cache/db_manage.py del "{}" "{}" '.format(hash_no, host_ip)

        stdin, stdout, stderr = c.exec_command(cmd)


def fetch_from_mec(hash_no, ipfs_hash):
    global MH
    global re_use
    com = 'echo "password" | sudo -S -H -u mec bash -c "ipfs cat {}"'.format(ipfs_hash)
    cmd = [com]
    stdout = str(sp.check_output(cmd, shell=True), 'utf-8')[0:-1]

    con = sqlite3.connect('/home/mec/cache.db')
    cur = con.cursor()

    ip = mec_me['ip']

    cur.execute("SELECT COUNT(*) FROM CacheTable WHERE Host_ip='" + ip + "'")
    d = cur.fetchone()
    r = d[0]  # This value represents how many data entries for host_ip

    if r >= cache_size and frequently_used(hash_no) == 'no':
        print(stdout)
        print('\n-----------------------------------')
        print('Hit from MEC Not Cached')
        print('-----------------------------------')
        MH += 1
    else:
        cmd = "echo '{}' > /home/mec/cache/{}.html".format(stdout, hash_no)     # cache file
        os.system(cmd)

        com = 'echo "password" | sudo -S -H -u mec bash -c "ipfs add /home/mec/cache/{}.html | cut -c 7-52"'.format(hash_no)              # add to ipfs database
        cmd = [com]
        new_ipfs_hash = str(sp.check_output(cmd, shell=True), 'utf-8')[0:-1]
        update_local_database(hash_no, new_ipfs_hash)

        cmd = 'echo "password" | sudo -S -H -u mec bash -c "ipfs cat {}"'.format(new_ipfs_hash)                               # show user
        os.system(cmd)

        print('-----------------------------------')
        print('Cache Hit from MEC')
        print('-----------------------------------')
        MH += 1
        if r >= cache_size:
            re_use += 1
    con.close()


def prepare_db():
    global re_use
    host_ip = mec_me['ip']
    try:
        con = sqlite3.connect('/home/mec/cache.db')
        cur = con.cursor()

        cur.execute("SELECT COUNT(*) FROM CacheTable WHERE Host_ip='" + host_ip + "'")
        d = cur.fetchone()
        r = d[0]  # This value represents how many data entries for host_ip
        if r >= cache_size:
            cur.execute("SELECT DateTime FROM CacheTable where Host_ip = '" + host_ip + "'")

            data = cur.fetchall()  # returns array that looks like [('2018-08-20 13:23:49',), ('2018-08-20 11:56:04',), ('2018-08-20 13:40:01',)]

            min_time = min(data)[0]  # Return minimum time

            delete_from_mec(min_time, host_ip)

            cur.execute(
                "SELECT Hash, Ipfs_Hash FROM CacheTable WHERE DateTime = '" + min_time + "' AND Host_ip = '" + host_ip + "'")
            data = cur.fetchone()

            cmd = 'rm /home/mec/cache/{}.html'.format(data[0])
            os.system(cmd)
            print('removing ipfs hash ({})'.format(data[1]))

            cmd = 'echo "password" | sudo -S -H -u mec bash -c "ipfs pin rm -r {} ; ipfs repo gc"'.format(data[1])
            print('testing ipfs: ' + cmd)
            os.system(cmd)

            cur.execute("DELETE FROM CacheTable WHERE DateTime = '" + min_time + "' AND Host_ip = '" + host_ip + "'")
            con.commit()
            con.close()
            re_use += 1

            # cur.execute("SELECT * FROM CacheTable")

    except sqlite3.Error as e:
        print('Error Encountered: {}'.format(e))


def delete_from_mec(min_time, host_ip):

    for i in mec_list:
        c = paramiko.SSHClient()

        un = 'mec'
        pw = 'password'
        port = 22

        c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        c.connect(mec_list[i], port, un, pw)
        cmd = 'python3 /home/mec/files_cache/db_manage.py delete "{}" "{}" '.format(min_time, host_ip)

        stdin, stdout, stderr = c.exec_command(cmd)


def cache_performance():
    global H
    global M
    global MH
    global window_size
    global re_use
    p = int((H / request_no) * 100)
    q = int(((H+MH) / request_no) * 100)
    print('----------------------------------------------------------')
    print('                   Cache Performance')
    print('----------------------------------------------------------')
    print('local MEC Performance: {}% | Cooperative Performance: {}% '.format(p, q))
    print('\nLocal Cache hits: {}       | Cache Misses: {}'.format(H, M))
    print('\nMEC Cache hits: {}         | Total Cache hits: {}'.format(MH, H + MH))
    print('----------------------------------------------------------')
    print('         Total use of Replacement Algorithm = {}'.format(re_use))
    print('----------------------------------------------------------')


def getting_ready():
    global mec_me  # {'hostname': <hostname>, 'ip': <ip>}

    my_ip = ip_address()

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


def run_me():
    global hash_dic
    global mec_list  # {'mec1': ip_address, 'mec3': 'ip_address'}
    global server_ip
    global request_no
    global colour

    os.system('clear')
    server_ip = input('web server ip: ')
    n = int(input('number of web(html) contents: '))
    request_no = int(input('number of requests: '))
    for i in range(1, n+1):
        cmd = 'echo "{}/{}.html" >> web_test.txt'.format(server_ip, i)
        os.system(cmd)
    result = make_hash_dic(server_ip, n)
    hash_dic = result[0]
    colour = result[1]
    os.system('clear')

    print("getting ready to start. . .")

    time.sleep(5)
    getting_ready()
    os.system('clear')
    g = Figlet(font='bubble')

    print(g.renderText('MEC CACHING PROJECT'))
    print(g.renderText('                      BY     EMEKA'))

    while True:
        print('\n')
        s = input('Enter any key to start and "stop" to exit: ')
        if s == 'stop':
            print('\nProgramme Terminated')
            print(freq)
            cache_performance()
            os.system('rm /home/mec/files_cache/mec_list.txt')
            os.system('rm /home/mec/files_cache/web_test.txt')
            break
        else:
            mec_str = ''
            tr = open('/home/mec/files_cache/mec_list.txt', 'r')
            tp = tr.readlines()
            for i in tp:
                mec_str += i[0:-1] + ','
            mec = '{' + mec_str[0:-1] + '}'
            mec_list = ast.literal_eval(mec)

            for i in range(30):
                fr = open('web_test.txt', 'r')

                t = fr.readlines()

                v = random.randint(0, (len(t) - 1))
                get_hash(t[v][0:-1])
                fr.close()
                time.sleep(3)
            '''

            for v in ref:
                fr = open('web_test.txt', 'r')

                t = fr.readlines()
                get_hash(t[v][0:-1])
                fr.close()
                time.sleep(3)
            '''


def main():
    run_me()


if __name__ == "__main__":
    main()

