from ping3 import ping
from datetime import datetime
import time
import openpyxl
import threading

ip_address_file = 'ip地址.txt'
ip_actual_address = 'ip地址实际名称.txt'

def read_line_by_number_and_data_processing(file_path, line_number):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            if 1 <= line_number <= len(lines):
                selected_line = lines[line_number - 1].strip()
                ip_address_or_actual_address = selected_line.split('=')[1].strip()
                return ip_address_or_actual_address
            else:
                return f"行号 {line_number} 超出文件范围"
            file.close()
    except FileNotFoundError:
        return "文件未找到"
    except Exception as e:
        return f"发生错误：{str(e)}"

def count_file_line(file_path):
    try:
        with open(file_path,'r',encoding='utf-8') as file:
            lines = file.readlines()
            file.close()
            return len(lines)
    except Exception as e:
        return f'发生错误：{str(e)}'

def file_update():
    length_ip_address_file = count_file_line(ip_address_file)
    length_ip_actual_address = count_file_line(ip_actual_address)
    if length_ip_actual_address != length_ip_address_file:
        return False
    else:
        line_number = count_file_line(ip_address_file)
        h = 1
        ip_address_and_actual_address=[]
        while h<=line_number:
            ip_address_and_actual_address.append([read_line_by_number_and_data_processing(ip_address_file,h),read_line_by_number_and_data_processing(ip_actual_address,h)])
            h = h+1
        return ip_address_and_actual_address

def ip_address_scan(ip_address):
    try:
        result = ping(ip_address, timeout=5)
        if result is False:
            return False
        elif result is None:
            return False
        else:
            return True
    except Exception:
        return False

def determine_whether_files_are_equal():
    if file_update() is not False:
        f = file_update()
        return f
    else:
        file_update()
        return 1

def excel_work(ip_address,ping_result,actual_address,time):
    workbook = openpyxl.load_workbook("ip地址日志.xlsx")
    sheet = workbook.active
    new_data = [ip_address,ping_result,actual_address,time]
    sheet.append(new_data)
    workbook.save("ip地址日志.xlsx")

def main_loop():
    while determine_whether_files_are_equal() == 1:
        print("两文件文件长度不相等！")
        time.sleep(5)
        determine_whether_files_are_equal()

    ip_address_and_actual_address = determine_whether_files_are_equal()
    print(ip_address_and_actual_address)

    for ip_address in ip_address_and_actual_address:
        current_time = datetime.now()
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

        if ip_address_scan(ip_address[0]):
            excel_work(ip_address=ip_address[0], ping_result="可以ping通，链接正常", actual_address=ip_address[1], time=formatted_time)
            print(f"{ip_address[0]} 可以 ping 通,地址:{ip_address[1]},链接正常。  时间:{formatted_time}")
        else:
            excel_work(ip_address=ip_address[0], ping_result="无法ping通，疑似断链", actual_address=ip_address[1], time=formatted_time)
            print(f"{ip_address[0]} 无法 ping 通,地址:{ip_address[1]}，疑似断链。  时间：{formatted_time}")

class user_in:
    def __init__(self,conture):
        self.conture =conture


def user_input(user):
    while True:
        input_str = input("请输入yes开始执行扫描，如果不输入30分钟后将自动执行：")
        if input_str == "yes":
            user.conture = True
            while True:
                if user.conture == False:
                    break
                time.sleep(1)


def control(user):
    while True:
        t = time.time()
        while True:
            if user.conture ==True:
                main_loop()
                user.conture = False
                break
            elif time.time() - t > 1800:
                main_loop()
                print("请输入yes开始执行扫描，如果不输入30分钟后将自动执行：",end="")
                break
            time.sleep(1)


if __name__ == '__main__':
    user = user_in(False)
    user_wait_thread = threading.Thread(target=user_input,args=(user,))
    contral_thread = threading.Thread(target=control,args=(user,))
    user_wait_thread.start()
    contral_thread.start()