__author__ = 'Lijian'


import shutil
from subprocess import *
import os
import re
import time
import datetime





#全局变量

# ping时间间隔
ABS_HOST_PATH = 'C:\\Windows\\System32\\drivers\\etc\\hosts'
SECOND = 5
#电信IP（默认)
IP = '115.239.210.27'
DX_IP = '115.239.210.27'
#联通IP
LT_IP = '115.239.210.27'
IS_COPY = False #是否已经备份，默认为没有



#按任意键退出def功能
def enter_exit():
    while True:
        str = input('按回车键退出.........')    #实则让线程等待阻塞
        if str == '':
            sys.exit()
        else:
            continue

# 1.获得hosts文件的绝对路径
def get_host_path():
    global ABS_HOST_PATH
    host_path = os.getcwd()+'\\hosts_path.txt'
    with open(host_path, 'r') as host_file:
            abs_host_path = host_file.readline()
    #如果hosts文件不存在，即默认路径是错的情况，需要手动键入
    if not os.path.isfile(ABS_HOST_PATH):
        print("默认hosts文件不存在，将读取hosts_path文件获取绝对路径...... ")
        if not os.path.isfile(abs_host_path):
            print("hosts_path文件中绝对路径有误，请检查后重新输入.......")
            enter_exit()
        else:
            ABS_HOST_PATH = abs_host_path


# 2.获取ip文件路径
def get_path(ping):

    #获得当前工作文件夹绝对路径
    work_path = os.getcwd()
    #判断使用电信还是联通
    if ping:
        filename = 'dx_ip.txt'
    else:
        filename = 'lt_ip.txt'
    #返回当前工作路径，ip的文件名
    return work_path, filename

#3.创建备份文件夹，备份host、ip文件
def log_file():
    work_path = os.getcwd()
    log_path = work_path+'\\logs' #全部日志文件目录
    host_log_path = log_path+'\\host'  #host日志目录
    lt_ip_log_path = log_path+'\\lt_ip' #联通ip日志目录
    dx_ip_log_path = log_path+'\\dx_ip' #电信ip日志目录
    ping_log_path = log_path+'\\ping' #ping日志目录
    isExists = os.path.exists(log_path)
    #all-log日志文件不存在则创建
    if not isExists:
        os.mkdir(log_path)
        os.mkdir(host_log_path)
        os.mkdir(lt_ip_log_path)
        os.mkdir(dx_ip_log_path)
        os.mkdir(ping_log_path)
    return log_path





# 4.一开始就备份host文件与ip文件
def copy_file():
    global IS_COPY
    print('-------------------------备份开始------------------------------')
    print('开始备份默认hosts文件、dx_ip.txt文件、lt_ip.txt文件.............')
    time.sleep(2) #“假装”2s备份时间

    log_path = log_file()
    path, file = os.path.split(ABS_HOST_PATH)
    lt_path = os.getcwd()+'\\lt_ip.txt'
    dx_path = os.getcwd()+'\\dx_ip.txt'
    #copy hosts
    host_copy_path = log_path+'\\host\\'+file
    #如果hosts文件已经备份则不需要备份，只备份一次就可以
    if not os.path.exists(host_copy_path):
        shutil.copyfile(ABS_HOST_PATH, host_copy_path)
        IS_COPY = True
    #copy lt_ip.txt
    lt_copy_path = log_path+'\\lt_ip\\lt_ip.txt'
    if not os.path.exists(lt_copy_path):
        shutil.copyfile(lt_path, lt_copy_path)
        IS_COPY = True
    #copy dx_ip.txt
    dx_copy_path = log_path+'\\dx_ip\\dx_ip.txt'
    if not os.path.exists(dx_copy_path):
        shutil.copyfile(dx_path, dx_copy_path)
        IS_COPY = True
    if IS_COPY:
        print('hosts文件、dx_ip.txt文件、lt_ip.txt文件已备份成功.............')
        print('-------------------------备份结束------------------------------'+'\n\n')
    else:
        print('hosts文件、dx_ip.txt文件、lt_ip.txt文件第一次启动已经备份.............')
        print('-------------------------备份失效------------------------------'+'\n\n')




# 5.读取ip文件
def read_ip(ping):
    ip_list = []
    ip_list.append('\n')
    ip_list.append('\n')
    (work_path, filename) = get_path(ping)

    with open(work_path+'\\'+filename, 'r') as file:
       for line in file:
           ip_list.append(line)

    return ip_list


# 6.读取host文件，识别ip-host区
def read_host():
    global IP
    host_list = []
    host_count = 0
    ip_count = 0
    with open(ABS_HOST_PATH, 'r') as host_file:
       for line in host_file:
            host_count = host_count+1
            sub_str = re.sub('\s', '', line)  #去除空格，便于下面的匹配识别
            host_list.append(line)
            if sub_str == '#::1localhost':   #识别host文件最后一行
                ip_count = host_count  #记录此时的行数

    #判断hosts文件中没有ip的条件是，读取到的list列表全都是回车
    #因为默认的host只有一个回车，更换的hosts文件有两个回车
    have_ip = len(host_list[ip_count:]) == host_list[ip_count:].count('\n')

    #进一步判断是联通还是移动

    print('\n\n'+'------------------检测hosts文件是否有匹配的IP------------------')
    if not have_ip:
        #hosts文件中有符合要求的电信联通ip
        if '#dx_ip\n' in host_list[ip_count:]:
            IP = DX_IP
            print('存在电信IP..........')
            print('检测5s后退出........')
            time.sleep(5)
            print('----------------------------检测结束----------------------------'+'\n\n')
            return host_list, ip_count, not have_ip
        elif '#lt_ip\n' in host_list[ip_count:]:
            IP = LT_IP
            print('存在联通IP..........')
            print('检测5s后退出........')
            time.sleep(5)
            print('----------------------------检测结束----------------------------'+'\n\n')
            return host_list, ip_count, not have_ip
        else: #hosts文件中有ip，但是不符合要求
            print('\n'+'hosts文件不存在电信联通ip，请点击lt_ip.exe(dx_ip.exe)更换/添加并再次启动host.exe程序.................'+'\n')
            print('------------------------------检测结束------------------------------')
            enter_exit()
    #hosts文件ip中为空，不符合要求，have_ip重新置为False
    print('\n'+'hosts文件没有ip，请点击lt_ip.exe(dx_ip.exe)更换/添加并再次启动host.exe程序.................'+'\n')
    print('----------------------------检测结束----------------------------'+'\n\n')
    enter_exit()


# 7.写入hosts文件
def write_host(host_list):
    #这里只需要获得hosts文件绝对路径即可
    str_list = "".join(host_list)
    #print(str_list)
    with open(ABS_HOST_PATH, 'w') as host_file:
          host_file.write(str_list)


# 8.替换ip(集成5/6/7各个模块)
def replace_ip(ping):

    (host_list, ip_count, have_ip) = read_host()
    ip_list = read_ip(ping)
    host_list[ip_count:] = ip_list  #替换ip-host区域
    write_host(host_list)



# 9.ping IP判断是否替换
def pingIP(second):


    #这里只获得have_ip判断hosts文件中是否存在ip，如果不存在ip则直接退出
    read_host()
    ip_time = datetime.datetime.now().strftime('%Y%m%d')
    print('---------------------------开始ping-----------------------------')
    while True:
        time.sleep(second)
        p = Popen(["ping.exe", IP],
                  stdin=PIPE, stdout=PIPE, stderr=PIPE,
                  shell=True)
        out = p.stdout.read().decode('gbk')
        print(out)
        reg_receive = '已接收 = \d'
        match_receive = re.search(reg_receive, out)
        receive_count = -1
        str_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if match_receive:
            receive_count = int(match_receive.group()[6:])

        if receive_count > 0: #接受到的反馈大于0，表示网络通
            print('ip地址：'+IP+' ping..........成功...............')
            #ping成功则继续
            get_path(True)
            #ping日志记录在ip_log中
            ip_path = log_file()+'\\ping\\'+ip_time+'ping.log'
            ping_file = open(ip_path, 'a+')
            ping_file.write(str_time+': '+out+'\n\n')
            #再次检测hosts文件是否有ip
            read_host()
            continue
        else:
            print('ip地址：'+IP+' ping..........失败...............')
            print('开始记录网络不通日志在all_log\ping.log文件夹下.............')
            print('开始替换ip再次进行ping...............')
            #ping失败则换ip并记录
            get_path(False) #这里必须先获得路径
            replace_ip(False)

            ping_path = log_file()+'\\ping\\'+ip_time+'notping.log'
            #追加错误日志记录在ping.log中并备份
            not_ping_file = open(ping_path, 'a+')
            not_ping_file.write(str_time+': '+out+'\n\n')
            #如果host文件不存在ip则退出，如果有则完成替换ip区域


# 10.主函数入口
if __name__ == '__main__':
    print('Windows系统内的hosts文件默认的路径为：C:\Windows\System32\drivers\etc\hosts')
    print('检测默认hosts文件路径是否存在...........')
    print('------------------------开始检测------------------------------')
    #获得全局变量hosts文件绝对路径
    get_host_path()
    print('hosts文件存在...................')
    print('------------------------检测结束------------------------------'+'\n\n')
    #一开始备份，只备份一次
    copy_file()
    pingIP(SECOND)
    time.sleep(5)


