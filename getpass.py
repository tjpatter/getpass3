import argparse
import sys
from ldap3 import Server, Connection

# Initialize command-line argument parser:
parser = argparse.ArgumentParser(description="getpass - Universal Password Retrieval Utility - Version 3.0 - 03/11/2022. This program retrieves a user's Universal Password by using an LDAP extended operation.")
parser.add_argument('-u', '--admin-user', required=True, help='CN of an administrative user, ex: cn=admin,o=lab',
                    dest='admin_user')
parser.add_argument('-p', '--admin-pass', required=True, help='Password for the administrative user',
                    dest='admin_pass')
parser.add_argument('-s', '--server-host', required=True, help='Hostname of the target server. ex: oes.lab.local',
                    dest='server_host')
parser.add_argument('-P', '--server-port', required=True, help='TLS port of the target server. ex: 636',
                    dest='server_port')
parser.add_argument('-t', '--target-user', required=True, help='CN of the target user password you want to retrieve. '
                                                               'ex: cn=test,ou=users,o=lab', dest='target_user')

args = parser.parse_args()

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
