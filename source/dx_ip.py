__author__ = 'Lijian'
import time
import host
import os
import re




# 1. 判断是增加IP还是更换IP
def add_change():
    host_cotent = []
    host_count = 0
    ip_count = 0
    with open(host.ABS_HOST_PATH, 'r') as host_file:
        for host_line in host_file.readlines():
            host_count = host_count+1
            sub_str = re.sub('\s', '', host_line)  #去除空格，便于下面的匹配识别
            host_cotent.append(host_line)
            if sub_str == '#::1localhost':   #识别host文件最后一行
                ip_count = host_count  #记录此时的行数
    str_list = "".join(host_cotent)
    #have_ip = True为空 have_ip = False不为空
    have_ip = len(host_cotent[ip_count:]) == host_cotent[ip_count:].count('\n')
    return str_list, have_ip


# 2.添加IP到hosts
def add_dx():
    dx_content = []
    dx_content.append('\n')
    dx_content.append('\n')
    dx_path = os.getcwd()+'//dx_ip.txt'
    with open(dx_path, 'r') as dx_file:
        for dx_line in dx_file.readlines():
            dx_content.append(dx_line)
    host_file = open(host.ABS_HOST_PATH, 'a+')
    host_file.write(''.join(dx_content))
    return dx_content



# 3.更换hosts文件IP
def replace_dx():
    str_list, have_ip = add_change()
    with open(host.ABS_HOST_PATH, 'w') as host_file:
          host_file.write(str_list)


#4. 手动更换/添加ip（或者在hosts中初始化ip）
def dx_ip():

    print('-------------------------手动更换/添加电信IP开始------------------------------')
    host_list, have_ip = add_change()

    #have_ip=False 不为空需要更换
    if not have_ip:
        print('\n'+'更换hosts为电信IP中........'+'\n')
        replace_dx()
        time.sleep(5)
        print('\n'+'-------------------------手动更换电信IP结束------------------------------'+'\n\n')
        host.enter_exit()
    #have_ip = True 为空需要添加
    else:
        print('\n'+'电信IP添加到hosts中........'+'\n')
        add_dx()
        print('-------------------------手动添加电信IP结束------------------------------'+'\n\n')
        host.enter_exit()

# 5.主函数入口
if __name__ == '__main__':
    #获得绝对路径之后才能更换
    host.get_host_path()
    dx_ip()