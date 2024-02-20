#########################################################################################################
#                                                       |  _   _      _   ____     _ ____   ___  _   _  #
#                                                       | | \ | | ___| |_|___ \   | / ___| / _ \| \ | | #
#       Author        : Rux aka. RuxUnderscore          | |  \| |/ _ | __| __) _  | \___ \| | | |  \| | #
#       Email         : jonathan.e.rux@underscore.com   | | |\  |  __| |_ / __| |_| |___) | |_| | |\  | #
#       Version       : 2.0                             | |_| \_|\___|\__|_____\___/|____/ \___/|_| \_| #
#       OS Support    : ALL                             |                                               #
#                                                       |           Network to JSON mapping.            #
#                                                       |                                               #
#########################################################################################################

    # Copyright (C) 2024  RuxUnderscore
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

# Iterates through common ports (1-1024) for each live system to get live ports. 
def check_ports(ip, delay = 0.5):
    open_ports = []
    for port in range(1,1025):
        sock = s.socket(s.AF_INET, s.SOCK_STREAM)
        sock.settimeout(0.1)
        result = sock.connect_ex((ip, port))
        if result == 0:
            open_ports.append(port)
        sock.close()
        time.sleep(delay)
    return open_ports

def is_host_alive(ip):
    response = subprocess.run(["ping", "-c", "1", "-W", "500", ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return response

def get_hostname(ip):
    try:
        return s.gethostbyaddr(ip)[0]
    except s.herror:
        return "Unknown"

# Iterates through each subnet's IP addresses.
def scan_network(network):
    subnet = network["subnet"]
    print(f"Scanning subnet {subnet} for live systems...")
    
    # Convert the subnet mask to a network object
    network_obj = ipaddress.ip_network(subnet, strict=False)
    
    # Loop through each IP address in the subnet range
    id = 0
    live_systems = []
    for ip in network_obj.hosts():
        ip = str(ip)
        # Ping the IP address to see if it's live
        print(f"Pinging {ip} to check if it's live...")
        if is_host_alive(ip):
            print(f"{ip} is live!")
            hostname = get_hostname(ip)
            print(f"Hostname for {ip}: {hostname}")
            ports = check_ports(ip)
            print(f"Open ports for {ip}: {ports}")
            
            # Add the data to the list
            data = {"id": id, "ip": ip, "hostname": hostname, "ports_open": ports}
            id += 1
            live_systems.append(data)
    return live_systems

# Load the networks from the networks.json file
print("Loading network configuration from networks.json...")
with open("networks.json", "r") as f:
    networks = json.load(f)

# Create an empty list to store the live systems with web servers
all_live_systems = []

# Loop through each network to ge information for live_systems_<unix-time>.json file.
for network in networks:
    live_systems = scan_network(network)
    all_live_systems.extend(live_systems)

# print(f"Live Systems Data:\n{all_live_systems}")
# Generate the file name with Unix time
filename = f"live_systems_{int(time.time())}.json"

# Write the live systems list to the output file
with open(filename, "w") as f:
    json.dump(all_live_systems, f, separators=(',', ':'))

print(f"Live systems data written to {filename}")
