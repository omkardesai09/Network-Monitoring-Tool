import time
import sys
from colorama import init, deinit, Fore, Style
import subprocess
import os.path
import paramiko
import re

print "Enter 3 additional parameters(filenames) while execution \n 1. Filename containing IP addresses of devices in topology \n 2. Filename containing username and password to setup SSH connection \n 3. Filename containing credentials to setup connection with MySQL database\n"

if len(sys.argv) == 4:
    ip_file = sys.argv[1]
    ssh_credentials = sys.argv[2]
    mysql_credentials = sys.argv[3]
    print sys.argv

else:
    print Fore.RED + "Please enter correct number of arguments as mentioned above\n"
    sys.exit()

# Check IP addresses in file are valid or not
def valid_ip():
    global list_of_ip
    ip_addr_file = open(ip_file, 'r')
    ip_addr_file.seek(0)
    list_of_ip = ip_addr_file.readlines()
    ip_addr_file.close()
    print list_of_ip
    for ip in list_of_ip:
        ip_octets = ip.split('.')
        ip_octets[3].strip('\n')

        if (len(ip_octets)==4) and (1<=int(ip_octets[0])<=223) and (int(ip_octets[0])!=127) and (int(ip_octets[0])!=169 or int(ip_octets[1])!=254) and (0<=int(ip_octets[1])<=255 and 0<=int(ip_octets[2])<=255 and 0<=int(ip_octets[3])<=255):
            pass

        else:
            print Fore.RED + "Invalid IP address: %s\n" %str(".".join(ip_octets))
            sys.exit()

    # Checking IP reachability
    while True:
        check = False
        for ip in list_of_ip:
            ping_reply = subprocess.call(['ping', '-c', '3', '-w', '3', '-q', '-n', ip], stdout=subprocess.PIPE)

            if ping_reply == 0:
                check = True
                continue
            elif ping_reply == 2:
                print Fore.RED + "\nNo response from device %s" %ip
                check = False
                break
            else:
                print Fore.RED + "\nPing to %s is failed" %ip
                check = False
                break

        if check == True:
            print Fore.GREEN + "All devices are reachable\n"
            break

        elif check == False:
            print Fore.RED + "Check IP address list or device\n"
            sys.exit()

def files_valid():
    global ssh_credentials, mysql_credentials
    if os.path.isfile(ssh_credentials) == True:
        pass
    else:
        print Fore.RED + "File %s not found\n" %ssh_credentials
        sys.exit()

    if os.path.isfile(mysql_credentials) == True:
        pass
    else:
        print Fore.RED + "File %s not found\n" %mysql_credentials
        sys.exit()

valid_ip()
files_valid()

# Establish SSH connection with devices

def ssh_conn(ip):

    credentials = open('ssh_pass.txt', 'r')
    credentials.seek(0)
    username = credentials.readlines()[0].split(',')[0]
    credentials.seek(0)
    password = credentials.readlines()[0].split(',')[1].rstrip('\n')
    credentials.close()

    conn = paramiko.SSHClient()
    conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    conn.connect(ip, username=username, password=password)

    shell = conn.invoke_shell()
    shell.send('terminal length 0\n')
    time.sleep(1)

    commands = '''show version | include (, Version|uptime is|bytes of memory|Processor board ID)&\
               show interfaces | include bia'''

    commands_list = commands.split('&')

    for each_command in commands_list:
        shell.send(each_command + '\n')
        time.sleep(2)

    output = shell.recv(65535)
    print output
    print '\n\n'

    hostname = re.search(r"(.+) uptime is", output)
    final_hostname = hostname.group(1)
    print final_hostname

    mac = re.findall(r"\(bia (.+?)\)", output)
    final_mac = mac[0]
    print final_mac

    model = re.search(r"(.+?) (.+?) (.+) bytes of memory", output)
    final_model = model.group(2)
    print final_model

    serial = re.search(r"Processor board ID (.+)", output)
    final_serial = serial.group(1)
    print final_serial

    uptime = re.search(r"uptime is (.+)\n", output)
    up_time = uptime.group(1)
    time_list = up_time.split(', ')

    year_list = 0
    week_list = 0
    day_list = 0
    hour_list = 0
    min_list = 0

    for i in time_list:
        if 'year' in i:
            year_list = int(i.split(' ')[0]) * 525600

        elif 'week' in i:
            week_list = int(i.split(' ')[0]) * 10080

        elif 'day' in i:
            day_list = int(i.split(' ')[0]) * 1440

        elif 'hour' in i:
            hour_list = int(i.split(' ')[0]) * 60

        elif 'minute' in i:
            min_list = int(i.split(' ')[0])

    total_time_min = year_list + week_list + day_list + hour_list + min_list

    print total_time_min


ssh_conn('192.168.2.10')


deinit()



