import time
import sys
from colorama import init, deinit, Fore, Style

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

    print "All IP addresses are valid.\n"

valid_ip()




