#########################################################################################################
#                                                       |  _   _      _   ____     _ ____   ___  _   _  #
#                                                       | | \ | | ___| |_|___ \   | / ___| / _ \| \ | | #
#       Author        : Jonathan Rux                    | |  \| |/ _ | __| __) _  | \___ \| | | |  \| | #
#       Email         : jonathan.e.rux@underscore.com   | | |\  |  __| |_ / __| |_| |___) | |_| | |\  | #
#       Version       : 1.0                             | |_| \_|\___|\__|_____\___/|____/ \___/|_| \_| #
#       OS Support    : ALL                             |                                               #
#                                                       |           Network to JSON mapping.            #
#                                                       |                                               #
#########################################################################################################

import json
import subprocess
import socket
import urllib.request
import time
import ipaddress

# Load the networks from the networks.json file
print("Loading network configuration from networks.json...")
with open("networks.json", "r") as f:
    networks = json.load(f)

# Create an empty list to store the live systems with web servers
live_systems = []

# Loop through each network
for network in networks:
    subnet = network["subnet"]
    print(f"Scanning subnet {subnet} for live systems...")
    
    # Convert the subnet mask to a network object
    network_obj = ipaddress.ip_network(subnet, strict=False)
    
    # Loop through each IP address in the subnet range
    for ip in network_obj.hosts():
        ip = str(ip)
        
        # Ping the IP address to see if it's live
        print(f"Pinging {ip} to check if it's live...")
        response = subprocess.Popen(["ping", "-n", "1", "-w", "500", ip], stdout=subprocess.PIPE).stdout.read()
        if "Reply from" in str(response):
            print(f"{ip} is live!")
            
            # If the IP address is live, check if port 80 and 443 are open
            port_80 = False
            port_443 = False
            try:
                # Try to connect to port 80 and check if it's open
                print(f"Checking if port 80 is open on {ip}...")
                urllib.request.urlopen("http://" + ip, timeout=1)
                port_80 = True
                print(f"Port 80 is open on {ip}")
            except:
                pass
            
            try:
                # Try to connect to port 443 and check if it's open
                print(f"Checking if port 443 is open on {ip}...")
                urllib.request.urlopen("https://" + ip, timeout=1)
                port_443 = True
                print(f"Port 443 is open on {ip}")
            except:
                pass
            
            # Get the hostname for the IP address
            try:
                hostname = socket.gethostbyaddr(ip)[0]
                print(f"Hostname for {ip} is {hostname}")
            except:
                hostname = "Unknown"
                print(f"Could not resolve hostname for {ip}")
            
            # Add the data to the list
            data = {"ip": ip, "hostname": hostname, "port_80_open": port_80, "port_443_open": port_443}
            live_systems.append(data)

# Generate the file name with Unix time
filename = f"live_systems_{int(time.time())}.json"

# Write the live systems list to the output file
with open(filename, "w") as f:
    json.dump(live_systems, f, indent=4)

print(f"Live systems data written to {filename}")
