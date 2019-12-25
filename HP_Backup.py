import json
import netmiko
import paramiko
import datetime
from getpass import getpass


# cd  /volumes/netscripts/Backup
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


#username, password = get_credentials()

device_type = 'hp_comware'

now = datetime.datetime.now()
today = str(now.year)+ '-' + str(now.month)+ '-' + str(now.day)


with open('DevicesBackup.txt') as f:          #opening devices from device IP list
		devices = f.read().splitlines()
		
for device in devices:
	
	try:

		#connection = netmiko.ConnectHandler(**device)
		connection = netmiko.ConnectHandler(ip=device, device_type=device_type,username='', password='', global_delay_factor= 0)
					
					#getting prompt for hostname 
		prompt= connection.find_prompt()
		print(prompt)
		#hostname = prompt[:-1]
					
						
		file = 'file location'
					
		with open(file,'w') as backup:
			
		
			
		#connection.sendCommand('screen-length disable')
		
			q = connection.sendCommand_expect('display current-configuration')
			connection.send_command('copy running-config startup-config',expect_string= r"#")
			print('Saving configuration')
			q = connection.sendCommand_expect('display current-configuration')
			backup.write(connection.send_command('save force', delay_factor=2))
			backup.write('\n\n'+ q +'\n\n')
			print('backup of '+ hostname + ' completed successfully')
					
			#closing the connection
		connection.disconnect()	
				
	except (netmiko.ssh_exception.NetMikoTimeoutException,
			  netmiko.ssh_exception.NetMikoAuthenticationException, 
			  paramiko.ssh_exception.SSHException,paramiko.ssh_exception.SSHException, OSError, Exception) as e:
			failed = 'Failed ', device, e, '\n'
			backup.write(device + '\n')		
					
