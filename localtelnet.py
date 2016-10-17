import getpass
import sys
import telnetlib
import socket

HOST = "localhost"
user = "andrew"
password = "bd45.am1"
error = "FALSE"



try
  tn = telnetlib.Telnet(HOST)
  tn.write("\n")
except socket.error:
  print "Could not connect!"
  error = "TRUE"
else:
  tn.read_until("login:")
  tn.write(user + "\n")
  print "** Logging in with username = %s **" % (user)
  if password:
     tn.read_until("Password:")
     tn.write(password + "\n")
     print "** Using password = %s **" % (password)
     tn.write("show chassis hardware\n")
     tn.write("exit\n")
     print tn.read_all()

  else:
    print error
print tn.read_all()
tn.close()
print "end"
