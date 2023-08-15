import argparse
import sys
from ldap3 import Server, Connection

# Function to read environment variables from a file
def read_env_file(file_path):
    env_vars = {}
    with open(file_path, 'r') as file:
        for line in file:
            key, value = line.strip().split('=', 1)
            env_vars[key] = value
    return env_vars

# Initialize command-line argument parser:
parser = argparse.ArgumentParser(description="getpass - Universal Password Retrieval Utility - Version 3.0 - 03/11/2022. This program retrieves a user's Universal Password by using an LDAP extended operation.")
parser.add_argument('-u', '--admin-user', help='CN of an administrative user, ex: cn=admin,o=lab', dest='admin_user')
parser.add_argument('-p', '--admin-pass', help='Password for the administrative user', dest='admin_pass')
parser.add_argument('-s', '--server-host', help='Hostname of the target server. ex: oes.lab.local', dest='server_host')
parser.add_argument('-P', '--server-port', help='TLS port of the target server. ex: 636', dest='server_port')
parser.add_argument('-t', '--target-user', help='CN of the target user password you want to retrieve. ex: cn=test,ou=users,o=lab', dest='target_user')
parser.add_argument('-e', '--use-env', action='store_true', help='Use .env file for connection info', dest='use_env')
args = parser.parse_args()

if args.use_env:
    env_vars = read_env_file(".env")
    server_host = env_vars['SERVER_HOST']
    server_port = env_vars['SERVER_PORT']
    admin_user = env_vars['ADMIN_USER']
    admin_pass = env_vars['ADMIN_PASS']
    target_user_dn = env_vars['TARGET_USER']
else:
    server_host = args.server_host
    server_port = args.server_port
    admin_user = args.admin_user
    admin_pass = args.admin_pass
    target_user_dn = args.target_user

# Build connection string:
server = Server('ldaps://' + server_host + ':' + server_port)

# Build connection object:
connection = Connection(server, admin_user, admin_pass)
# Initiate TLS connection:
connection.start_tls()

# Try to bind to the server by using the connection's credentials.
connection.bind()
if not connection.bound:
    print("Could not bind as '" + admin_user + "' to server 'ldaps://" + server_host + ":" + server_port + "'")
    print("Check username, password, and connection string.")
    sys.exit(1)

# Retrieve password:
password = connection.extend.novell.get_universal_password(target_user_dn)
if password is None:
    print("Could not retrieve password for user '" + target_user_dn + "'.")
    print("This could be due to the user not having a Universal Password set, no Universal Password Policy applied, ")
    print("or the admin user may not have permission to retrieve the user's password.")
    sys.exit(2)

print(password)
sys.exit(0)
