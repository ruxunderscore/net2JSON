# net2JSON
Checks for pingable clients on 1 or more subnets, then checks if they have open ports on the configured port range. Then, the results are recorded to a unix timestamped json file for easy parsing.  

## Prerequisites
- python3

## How to Use
- OPTIONAL: change `networks.json` file to have the port ranges *AND* one or more of the network subnets that you want to scan with CIDR notation. (For one client, you can specify the ip followed with a /32.)
- Run `net2json.py`.
- Watch as each step in the scan is written out to the console.
- Find your new json file of the scanned network in the working project directory. The file is minified for space savings.
- Now you have a easily parsable json file you can use for anything!
- BONUS: I recommend using [jq](https://github.com/jqlang/jq) if you want to manually parse and read the file easily.

## Ideas
If you would like to see something implemented in this script let me know in an issue or create a pull request! Feel free to fork it for your own projects as well! This project uses GNU GPL v3.0!
