# Private Internet Access Wireguard Configuration Generator
This project was forked from https://github.com/hsand/pia-wg, to which this project owes all its thanks.

pia-wg is a Python-based WireGuard configuration utility for Private Internet Access. 

This fork has been modified from the original to facilitate automating config generation by using fixed PIA user credentials and region as to not require user interaction. It also outputs a fixed config filename for ease of referencing (and not accumulating an archive of stale config files). This is especially useful as your PIA WireGuard configuration can be refreshed and updated automatically with one command. This fork uses the lastest version of the PIA serverlist ("v6" as of 20221202); version "v4" used in the upstream was seeming to cause authentication issues (I assume somewhere in the token generation).

I find myself needing to periodically regenerate my PIA WireGuard config file when the VPN connection eventually breaks when the endpoints change. Generating a new config seems to remedy this issue.

For Linux users, I've included a `auto-generate-config.sh` shell script to simplify the installation procedure and make it easier to regenerage the config on a timer. 

# Installation
## Windows

1. Install the latest version of [Python 3](https://www.python.org/downloads/windows/)
   - Make sure to select "Add Python to environment variables" during installation
1. Install [WireGuard](https://www.wireguard.com/install/)
1. Open a command prompt and navigate to the directory where you placed the pia-wg utility.
1. Edit the `.env` file in the base `pia-wg` directory and input your PIA username, password, and valid VPN region of your choosing.

The following commands will create a virtual Python environment, install the dependencies, and run the tool.

```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python generate-config.py
deactivate
```

- The script should generate a `PIA-wg.conf` file that can be imported into the WireGuard utility.


## Linux

1. Install dependencies, clone pia-wg project, and create a virtual Python environment:

```
sudo apt install git wireguard-tools openresolv
git clone https://github.com/djtroyal/pia-wg <directory>
cd <directory>/pia-wg
python3 -m venv venv
./venv/bin/pip install -r requirements.txt
chmod +x auto-generate-config.sh
```

2. Save your PIA user credentials and region in the (hidden) `.env` file in the `pia-wg` base directory:

Edit the `.env` file in the base `pia-wg` directory and input your PIA username, password, and valid VPN region of your choosing.

3. [Run the utility](https://github.com/djtroyal/pia-wg/edit/master/README.md#running-the-utility)

### Running the Utility

Following any one of these options will generate a `PIA-wg.conf` file in your cloned pia-wg folder:

- Use the shell script
```
./auto-generate-config.sh
```

- Activate the venv and run the Python script
```
source venv/bin/activate
python3 generate-config.py
```

- Run the venv'd Python script in one line without having to activate the venv
```
./venv/bin/python3 generate-config.py
```


Copy  `PIA-wg.conf` file to `/etc/wireguard/`, and start the interface

```
sudo cp PIA-wg.conf /etc/wireguard/wg0.conf
sudo wg-quick up wg0
```

You can shut down the interface with `sudo wg-quick down wg0`

## Check if it's Working

- If you have `curl` installed, you can check to see if your WAN (public) IP address has changed from your ISP-provided one using the command line:
```
curl icanhazip.com
```

- And/or visit https://dnsleaktest.com/ to make sure you see a strange new IP and check for DNS leaks.


## Speculative To-Dos
- Auto copy the output `PIA-wg.config` to `/etc/wireguard` (how to best/most securely accomplish `su` elevation?)
- Restrict permissions on output config file (Linux)
- Add instruction for making a cron job and/or a systemd timer for auto-gen script
- Generate new config when VPN connection breaks (assumed stale) 
  - Would need to bring down wg0 service to re-establish WAN connection first
- Modify `region` parameter in `generate-config.py` to accept a variable-length list of regions
  - `region` var in `.env` would also have to be formatted as list
- Auto-populate the `.env` file on first run of `auto-generate-config.sh` script (check if fields are empty first)
- Incorporate region (server) latency function to auto-select most response region(s)
  - Also consider adding function to optionally randomize servers upon config generation (could also bake in some latency criteria)
- Fork and incorporate into official Wireguard Docker container
