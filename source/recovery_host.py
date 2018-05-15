__author__ = 'Lijian'

import os
import shutil
import host





#还原host文件
def recovery_hosts():
    host.get_host_path()
    abs_host_path = host.ABS_HOST_PATH
    path, host_file = os.path.split(abs_host_path)
    #获得host文件备份绝对路径
    host_copy_path = os.getcwd()+'\\logs\\host\\'+host_file
    if not os.path.exists(host_copy_path):
        print('hosts备份文件不存在，先启动host.exe完成备份.........')
        host.enter_exit()
    print('-------------------------还原开始------------------------------')
    #还原最开始的host文件
    shutil.copyfile(host_copy_path, abs_host_path)
    print('\n'+'hosts文件还原中........'+'\n')
    print('-------------------------还原结束------------------------------'+'\n\n')
    host.enter_exit()

if __name__ == '__main__':
    recovery_hosts()
