import getpass
import sys
import telnetlib
import socket
import time

# Variables
HOST = "146.66.3.18"
PORT = "2003"
USER = "imtech"
PASS = "Imtech"
ERROR = "FALSE"

try:
  print "** connecting to %s on port %s..." % (HOST, PORT)
  tn = telnetlib.Telnet(HOST, PORT)

except socket.error:
  print "** Could not connect!"
  error = "TRUE"
else:
  print "** waiting for login"
  tn.write("\n")
  tn.read_until("ogin:", timeout=10)
  tn.write(USER + "\n")
  print "** Logging in with username = %s" % (USER)

  if PASS:
#     tn.set_debuglevel(1)
     print "** waiting for password"
     tn.read_until("assword:", timeout=10)
     print "** Using password = %s" % (PASS)
     tn.write(PASS + "\n")
     print "** getting info from device"
     tn.read_until(">")
     tn.write("show chassis hardware\n")
     HW = tn.read_until(">")
     tn.write("show version\n")
     VER = tn.read_until(">")
     tn.write("exit\n")
     tn.close()


  else:
    print ERROR

print HW
print VER