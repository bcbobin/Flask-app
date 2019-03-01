import netmiko 

device1 = {'device_type': 'cisco_wlc', 'ip': '10.208.254.250', 'username': 'irg', 'password': 'N0vember24'}

def usersearch(user):
    connect = netmiko.ConnectHandler(**device1)
    connect.send_command("config paging disable")
 
    if user == "":
        output = connect.send_command("show netuser summary")
    else:
        output = connect.send_command("show netuser detail "+ user)
        if "Unable" in output:
            return -1
    
    connect.disconnect()
    return output
    



