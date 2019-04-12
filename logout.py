## Script used for testing only:
## Logs out of device on term server line
## Useful when bootstrap script fails and leaves the device logged in.
import getpass
import sys
import telnetlib
import socket
import time

# Variables
HOST = "146.66.3.18"
PORT = "2003"

print "** Clearing the login for %s port %s" % (HOST, PORT)
tn = telnetlib.Telnet(HOST, PORT)
time.sleep(2)
tn.write("\n")
time.sleep(1)
tn.write("exit\n")

try:
    tn.read_until("ogin:")
    tn.close()
except:
    print "not logged out"
print "** Done"