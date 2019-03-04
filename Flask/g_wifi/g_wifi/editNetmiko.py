import netmiko 

device1 = {'device_type': 'cisco_wlc', 'ip': '10.208.254.250', 'username': 'irg', 'password': 'N0vember24'}
device2 = {'device_type': 'cisco_wlc', 'ip': '10.200.254.250', 'username': 'irg', 'password': 'N0vember24'}
hosts = [device1, device2]

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
    
def extenduser(user, time):
    for i in hosts:
        connect = netmiko.ConnectHandler(**hosts[i])
        result = connect.send_command("config netuser lifetime " + user + " " + time)
        if "Invalid" in result:                         #could not find user, error
            return -1
        else:                                           #user was extended 
            pass
        connect.disconnect()
    return 0 
    
def deleteuser(user):
    count = 0
    for i in hosts:
        connect = netmiko.ConnectHandler(**hosts[i])
        result = connect.send_command("config netuser delete username "+ user)
        if "exist" in result:                       #user not found
            count += 1
            pass
        if "Deleted" in result:             #user was successfully deleted 
            pass
        else:
            return -1               #something happened outside of expectations, error
        connect.disconnect()    
    if count == 2:
        return 1                #user never existed 
    return 0                    #user was deleted                   



