import time
import sys
from colorama import init, deinit, Fore, Style

print "Enter 3 additional parameters(filenames) while execution \n 1. Filename containing IP addresses of devices in topology \n 2. Filename containing username and password to setup SSH connection \n 3. Filename containing credentials to setup connection with MySQL database\n"

if len(sys.argv) == 4:
    ip_addr = sys.argv[1]
    ssh_credentials = sys.argv[2]
    mysql_credentials = sys.argv[3]
    print sys.argv

else:
    print Fore.RED + "Please enter correct number of arguments as mentioned above\n"
    sys.exit()


