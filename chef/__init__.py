
from string import Template
import base64
import logging
USER_DATA_TEMPLATE="""#!/bin/bash -xev

exec > >(tee /var/log/user-data.log|logger -t user-data -s 2>/dev/console) 2>&1

# Do some chef pre-work
/bin/mkdir -p /etc/chef
/bin/mkdir -p /var/lib/chef
/bin/mkdir -p /var/log/chef

cd /etc/chef/

# Install chef
curl -L https://omnitruck.chef.io/install.sh | bash || error_exit 'could not install chef'

# Create first-boot.json
cat > "/etc/chef/first-boot.json" << EOF
{
   "run_list" :[
     $RUN_LIST
   ]
}
EOF

NODE_NAME=$$(/usr/bin/hostname)

# Create client.rb
cat > /etc/chef/client.rb << EOF

log_location     STDOUT
chef_server_url  "$CHEF_SERVER_URL"
validation_client_name "default-validator"
validation_key "/etc/chef/default-validator.pem"
node_name  "$${NODE_NAME}"
ssl_verify_mode :verify_none
EOF

cat > /etc/chef/default-validator.pem << EOF
$VALIDATOR_KEY
EOF

# open some ports for the demo
firewall-cmd --zone=public --add-port=8080/tcp --permanent
firewall-cmd --zone=public --add-port=80/tcp --permanent
firewall-cmd --reload

for i in 1 2 3; do chef-client -j /etc/chef/first-boot.json && break || sleep 30; done

"""

def get_validator_key(file='default-validator.pem'):
    filein = open(file)
    return filein.read()

def get_user_data(config):
    validator_key = get_validator_key(config['validator_key_file'])
    fields={
        'CHEF_SERVER_URL': config['chef_server_url'],
        'VALIDATOR_KEY': validator_key,
        'RUN_LIST': config['run_list']
    }
    logging.info("Using Chef Server: %s"%config['chef_server_url'])
    src = Template(USER_DATA_TEMPLATE)
    user_data = src.substitute(fields)
    logging.debug(user_data)
    return base64.b64encode(user_data.encode('utf-8')).decode('utf-8')
