
import ipaddress
import argparse
import regex as re

#Intialization of argparse
parser=argparse.ArgumentParser()

#Adding the --ip argument
parser.add_argument('--ip', required=True)

#Parsing the argument
args = parser.parse_args()

try:

	#Taking File name from user
	File_name = input (" Enter the File's Name:")

	file_read = open (File_name, "r")

	lines = file_read.readlines()

	#Declaring new list to insert matched rows
	new_list = []

	index=0 # position index variable
	
	#Used to return the provided address with their subnet	For ex 1.2.3.4 returns with 1.2.3.4/32
	interface=ipaddress.ip_interface(args.ip)
	
	#Checking if the provided IP address is a single ip or a network
	if str(interface.netmask) == '255.255.255.255':  

		#Block for matching the condition if someone provides input with /32 at end

		#Regex if someone provides the input /32 eg 1.2.3.4/32
		subnet_32=re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\/32",args.ip)
		
		#checks if the regex matches the provided IP
		if  str(bool(subnet_32))=='True':
			
			#Provides address without network information 
			without_network=interface.ip
			
			for line in range(len(lines)):
				
				if str(without_network) in lines[line]:
				
				#inserting the matched rows in empty list
					new_list.insert(index,lines[line])
				
					index +=1 # incrementing position index variable

		else:

		#Block for matching single IP address in Log file
			
			address = ipaddress.ip_address(args.ip)
			
			for line in range(len(lines)):
				
				if str(address) in lines[line]:
				
				#inserting the matched rows in empty list
					new_list.insert(index,lines[line])
				
					index +=1 # incrementing position index variable
				
	else:

		#Block for matching IP's belonging to a specific IP CIDR network in Log file

		#Calculating and storing all ip address for a given network
		all_ips=[]
		address = ipaddress.ip_network(args.ip, strict=False)
		for i in address:
			
			all_ips.insert(-1,str(i))

		#Comparing the stored IP addresses with log file 
		for line in range(len(lines)):
			
			#splitting the lines in log file to be used in and condition
			y=(lines[line].split())
			
			for ip in range(len(all_ips)):
			
				'''
				And condition was required to match the exact same IP address as use of In operator resulted in fetching the same rows multiple times
				for example 31.184.238.1,31.184.238.12,31.184.238.128 all were displayed when in operatoe was used when checking for ip 31.184.238.128

				'''
				if all_ips[ip] in lines[line] and all_ips[ip] == y[0]:
			
					new_list.insert(index,lines[line])
			
					index +=1 #incrementing position index variable

							
	file_read.close()

	if len(new_list) == 0:
		
		print ("!!Sorry, No matching logs found for given address !!")
			
	else:
			
		for i in range(len(new_list)):
		
			print(new_list[i])
except:
	
	print("The file does not exist or the format of provided network is not correct")
