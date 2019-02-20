import netmiko 
import cgi, cgitb, traceback, sys, os, time, logging


device = {
	'device_type': 'cisco_wlc', 
	'ip': '10.200.254.250',
	'username': '',
	'password': '',
}

connect = netmiko.ConnectHandler(**device)
output = connect.send_command("show sysinfo")
print(output)

connect.disconnect()

