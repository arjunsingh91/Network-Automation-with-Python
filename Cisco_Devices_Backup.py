import json
import netmiko
import paramiko
import datetime
from getpass import getpass

#to get current time stamp

def get_input(prompt=''):
    try:
        line = raw_input(prompt)
    except NameError:
        line = input(prompt)
    return line


def get_credentials():
    """Prompt for and return a username and password."""
    username = get_input('Enter Username: ')
    password = None
    while not password:
        password = getpass()
        password_verify = getpass('Retype your password: ')
        if password != password_verify:
            print('Passwords do not match.  Try again.')
            password = None
    return username, password


username, password = get_credentials()

device_type = 'cisco_ios'

now = datetime.datetime.now()
today = str(now.year)+ '-' + str(now.month)+ '-' + str(now.day)



#def failed(device_name, exception) :
#	with open('failed.txt') as f:
#		f.write('Failed ', device_name, exception, '\n')

with open('Devices.txt') as f:          #opening devices from device IP list
		devices = f.read().splitlines()
#fail = failedbackup +'-'+'.txt'		
for device in devices:
	#device['username'] = username
	#device['password'] = password

	try:

		#connection = netmiko.ConnectHandler(**device)
		connection = netmiko.ConnectHandler(ip=device, device_type=device_type,username=username, password=password)
					
					#getting prompt for hostname 
		prompt= connection.find_prompt()
		hostname = prompt[:-1]
					
					#sending command 
		
		file = 'file location /'+today +'-'+ hostname +'.txt'
					
		with open(file,'w') as backup:
			
			tech = prompt +'sh tech'+ '\n'
			connection.send_command('set length 0')			
			backup.write(tech)	


#The issue is that Netmiko doesn't know that the command is done. 
#By default Netmiko is waiting for the trailing router prompt to come back to determine the command is done. 
#You can change this behavior by using the expect_string argument, see this example here:
#https://github.com/ktbyers/netmiko/blob/develop/examples/use_cases/case4_show_commands/send_command_expect.py

#Note, expect_string takes a regular expression pattern so your probably should use a raw Python string and 
#you should be careful with respect to using special regular expression characters.
#You will need to use the expect_string argument to handle the confirmation prompt that the Catalyst is sending.

#expect_string takes regular expressions so you just need to do a regular expression "or" for that so probably:
#expect_string = r"(>|#)"

			backup.write(connection.send_command('sh running-config',expect_string= r"#") + '\n\n')
			intbr = prompt + 'sh ip int br'+ '\n'
			backup.write(intbr)
			backup.write(connection.send_command('sh ip int brief',expect_string= r"#") + '\n\n')
			#connection.send_command('copy running-config startup-config',expect_string= r"#")
			print('backup of '+ hostname + ' completed successfully')
					
			#closing the connection
			connection.disconnect()	
				
	except (netmiko.ssh_exception.NetMikoTimeoutException,
			  netmiko.ssh_exception.NetMikoAuthenticationException, 
			  paramiko.ssh_exception.SSHException,paramiko.ssh_exception.SSHException, OSError, Exception) as e:
			failed = 'Failed ', device, e, '\n'
			failed = str(print('Failed ', device, e, '\n'))
			#with open('failedbackup.txt','w') as fail:
			#fail.write(failed)
					
					
