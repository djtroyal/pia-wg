from piawg import piawg
from pick import pick
from datetime import datetime
from dotenv import load_dotenv
import os 

pia = piawg()

# Load in environment variables from super secret PIA credentials .env file
load_dotenv()

# Generate public and private key pair
pia.generate_keys()

# Select region
pia.set_region(os.environ.get('region'))

# Get token
while True:
    username = os.environ.get('PIA_user')
    password = os.environ.get('PIA_pass')
    if pia.get_token(username, password):
        print("Login successful!")
        break
    else:
        print("Error logging in, please try again...")

# Add key
status, response = pia.addkey()
if status:
    print("Added key to server!")
else:
    print("Error adding key to server")
    print(response)

# Build config
timestamp = int(datetime.now().timestamp())
location = pia.region.replace(' ', '-')
config_file = 'PIA-wg.conf'
print("Saving configuration file {}".format(config_file))
with open(config_file, 'w') as file:
    file.write('[Interface]\n')
    file.write('Address = {}\n'.format(pia.connection['peer_ip']))
    file.write('PrivateKey = {}\n'.format(pia.privatekey))
    file.write('DNS = {},{}\n\n'.format(pia.connection['dns_servers'][0], pia.connection['dns_servers'][1]))
    # Added PostUp/PreDown routing rules to support docker container routing 
    # Ref: https://www.linuxserver.io/blog/routing-docker-host-and-container-traffic-through-wireguard#routing-a-containers-traffic-through-the-wireguard-container-via)
    file.write('# Uncomment the below two PostUp and PreDown routing rules if routing containers through WireGuard container\n')
    file.write('# PostUp = iptables -t nat -A POSTROUTING -o wg+ -j MASQUERADE\n')
    file.write('# PreDown = iptables -t nat -D POSTROUTING -o wg+ -j MASQUERADE\n\n')
    file.write('[Peer]\n')
    file.write('PublicKey = {}\n'.format(pia.connection['server_key']))
    file.write('Endpoint = {}:1337\n'.format(pia.connection['server_ip']))
    file.write('AllowedIPs = 0.0.0.0/0\n')
    file.write('PersistentKeepalive = 25\n')
