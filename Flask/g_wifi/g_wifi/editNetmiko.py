import netmiko 
import cgi, cgitb, traceback, sys, os, time, logging


device1 = {'device_type': 'cisco_wlc', 'ip': '10.200.254.250', 'username': 'irg', 'password': 'N0vember24'}
device2 = {'device_type': 'cisco_wlc', 'ip': '10.208.254.250', 'username': 'irg', 'password': 'N0vember24'}


connect = netmiko.ConnectHandler(**device)
output = connect.send_command("show sysinfo")
print(output)

connect.disconnect()

