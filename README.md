# net2JSON
Checks for pingable clients on 1 or more subnets, then checks if they have open ports between 1..1024. Then, the results are recorded to a unix timestamped json file for easy parsing.  

## Prerequisites
- python3

## How to Use
- OPTIONAL: change `networks.json` file to have one or more of the network subnets that you want to scan in CIDR notation.
- Run `net2json.py`.
- Watch as each step in the scan is written out to the console.
- Find your new json file of the scanned network in the working project directory. 
- Now you have a easily parsable json file you can use for anything!

## Ideas
If you would like to see something implemented in this script let me know in an issue or create a pull request! Feel free to fork it for your own projects as well! This project uses GNU GPL v3.0!
