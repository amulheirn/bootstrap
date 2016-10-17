import sys
import telnetlib
import socket
import re

# Variables
HOST = "192.168.30.10"
PORT = "2001"




def stateCheck():
    # Check the prompt that is being given by the device, and
    # log out as necessary so we get to a known state
    SHELLPROMPT = "\n(.*)\%"   # Match Junos bash shell prompt
    CLIPROMPT = "\n(.*)>"      # Match the Junos operational mode prompt
    EDITPROMPT = "\n(.*)#"     # Match edit mode in Junos
    LOGINPROMPT = "\n.ogin:"   # Match either 'Login' or 'login'

    tn.write("\n")
    STATE = tn.expect([SHELLPROMPT, CLIPROMPT, LOGINPROMPT, EDITPROMPT], timeout = 2)


    if STATE[0] == 0:
        print '** Bash'
        tn.write("exit\n")
    elif STATE[0] == 1:
        print '** Junos operational mode prompt'
        tn.write("exit\n")
    elif STATE[0] == 2:
        print '** login prompt'
    elif STATE[0] == 3:
        print '** Junos edit prompt'
        tn.write("exit\n")
    else:
        print 'No match'
    return STATE[0]


print "** connecting to %s on port %s..." % (HOST, PORT)
tn = telnetlib.Telnet(HOST, PORT)


if stateCheck() != 2:
    stateCheck()
else:
    print 'State is login prompt'


tn.close()
