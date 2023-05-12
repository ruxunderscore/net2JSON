#########################################################################################################
#                                                       |  _   _      _   ____     _ ____   ___  _   _  #
#                                                       | | \ | | ___| |_|___ \   | / ___| / _ \| \ | | #
#       Author        : Jonathan Rux                    | |  \| |/ _ | __| __) _  | \___ \| | | |  \| | #
#       Email         : jonathan.e.rux@underscore.com   | | |\  |  __| |_ / __| |_| |___) | |_| | |\  | #
#       Version       : 1.1                             | |_| \_|\___|\__|_____\___/|____/ \___/|_| \_| #
#       OS Support    : ALL                             |                                               #
#                                                       |           Network to JSON mapping.            #
#                                                       |                                               #
#########################################################################################################

    # Copyright (C) 2023  RuxUnderscore
    # This program is free software: you can redistribute it and/or modify
    # it under the terms of the GNU General Public License as published by
    # the Free Software Foundation, either version 3 of the License, or
    # (at your option) any later version.

    # This program is distributed in the hope that it will be useful,
    # but WITHOUT ANY WARRANTY; without even the implied warranty of
    # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    # GNU General Public License for more details.

    # You should have received a copy of the GNU General Public License
    # along with this program.  If not, see <https://www.gnu.org/licenses/>.


import json
import subprocess
import socket as s
import time
import ipaddress

def checkPorts():
    ports = []
    for port in range(1,1024):
        try:
            address = (ip, int(port))
            s.socket().connect(address)
            print(f"Port {port} is open.")
            ports.append(port)
        except s.error:
            print(f"Port {port} is closed.")

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
            
            ports = []

            try:
                hostname = s.gethostbyaddr(ip)[0]
                print(f"Hostname for {ip} is {hostname}.")
            except:
                hostname = "Unknown"
                print(f"Could not resolve hostname for {ip}.")

            open_ports = checkPorts()
            ports.append(open_ports)
            
            # Add the data to the list
            data = {"ip": ip, "hostname": hostname, "ports_open": ports}
            live_systems.append(data)

# Generate the file name with Unix time
filename = f"live_systems_{int(time.time())}.json"

# Write the live systems list to the output file
with open(filename, "w") as f:
    json.dump(live_systems, f, indent=4)


print(f"Live systems data written to {filename}")
