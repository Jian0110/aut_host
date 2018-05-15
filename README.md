# aut_host自动更换IP介绍

## 一、文件介绍
* 三个文本的作用
    *   dx_ip.txt：存放电信IP，以#dx_ip开头标识
    *   lt_ip.txt：存放联通IP，以#lt_ip开头标识
    *   hosts_path.txt：当Windows下默认的hosts文件路径不存在时候，这里存放输入hosts文件绝对路径
* 三个应用程序作用	
    *   dx_ip.exe：当hosts文件中不存在ip或者不是电信ip时，可以点击进行手动添加/更换操作。
    *   lt_ip.exe：当hosts文件中不存在ip或者不是联通ip时，可以点击进行手动添加/更换操作。
    *   recovery_host.exe：恢复最初的host.exe一开始备份的hosts文件。
    *   host.exe：一开始生成logs日志目录，之后会备份hosts、dx_ip.txt、lt_ip.txt文件到logs目录下，之后检测（ping）默认的电信IP，若电信ping不通则自动更换联通IP，再次进行5m间隔的ping检测。

## 二、技术介绍
* 语言说明：采用`python`语言，导入`os、sys、subprocess、shutil`等基本模块完成功能
* 主要流程：`get_host_path`(获得hosts文件正确路径)->`get_path`(获得dx_ip/lt_ip文件的路径)->`log_file`(创建logs目录文件)->`copy_file`(备份文件)->`read_ip read_host`（读取ip文件与hosts文件）->`write_host`（写入hosts文件）->`replace_ip`(更换hosts文件ip)->`pingIP`(ping检测IP)->`main`(主程序入口)
* Ping时间间隔说明：每隔5m ping一次IP
* 日志说明：日志只是简单的记录ping/notping（ping成功与ping不成功的记录）
* 生成exe文件说明：最后利用`pyinstaller.exe -F -w -c file_path`生成.exe应用程序文件
* 界面说明：控制台都会有良好的界面提示效果，即使出错也不会秒退窗口，会提示按回车退出

## 三、补充说明
        虽然主要的更换IP工已经实现，但是仍然还有很多不完美的地方。日后有时间会逐渐完善！
