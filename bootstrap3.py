#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

# Bootstrap3 creates SSH public key logins for 'axians-prestage' user so
# that Ansible can log in over SSH to do upgrades etc.

import sys
import telnetlib
import socket
import argparse


# Variables
HOST = "192.168.30.10"
PORT = "2001"
USER = "root"
PASS = "Imtech"
ERROR = "FALSE"
PASSPROMPT = ".*assword\:"  # Check for presence of password prompt
PASSFAIL = ".*incorrect"    # was the password wrong?
HW = ""
VER = ""

# Parse some arguments from the command-line
parser = argparse.ArgumentParser(description="Bootstrap program for setting IP and root password on Junos")
#parser.add_argument('-t', '--termserv', help='IPv4 address of the terminal server', required=True)
#parser.add_argument('-s', '--serial', help='Serial line to use (e.g. 2001)', required=True)
parser.add_argument('-p', '--password', help='Root user password to be put onto device', required=True)
parser.add_argument('-i', '--interface', help='Interface to be used as management for pre-staging', required=True)
parser.add_argument('-a', '--address', help='IPv4 address AND mask to put on the interface (e.g. 192.168.1.1/24)', required=True)
parser.add_argument('-r', '--route', help='Default gateway', required=False)
args = parser.parse_args()

def stateCheck():
    # Check the prompt that is being given by the device, and
    # log out as necessary so we get to a known state

    # Define some regex matches for prompt types:
    SHELLPROMPT = "\n(.*)\%"   # Match Junos bash shell prompt
    CLIPROMPT = "\n(.*)>"      # Match the Junos operational mode prompt
    EDITPROMPT = "\n(.*)#"     # Match edit mode in Junos
    LOGINPROMPT = "\n.ogin:"   # Match either 'Login' or 'login'

    # Send a carriage-return to kick the term server's serial line into
    # action and match on what comes back with a timeout in case nothing
    # is connected

    tn.write("\n")
    STATE = tn.expect([SHELLPROMPT, CLIPROMPT, LOGINPROMPT, EDITPROMPT], timeout = 2)
    while STATE[0] != 2:
        if STATE[0] == 0:
            print '** Logging out of bash shell'
            tn.write("exit\n")
            STATE = tn.expect([SHELLPROMPT, CLIPROMPT, LOGINPROMPT, EDITPROMPT], timeout = 2)
        elif STATE[0] == 1:
            print '** Logging out of Junos operational mode'
            tn.write("exit\n")
            STATE = tn.expect([SHELLPROMPT, CLIPROMPT, LOGINPROMPT, EDITPROMPT], timeout = 2)
        elif STATE[0] == 3:
            print '** Logging out of Junos edit mode'
            tn.write("exit\n")
            STATE = tn.expect([SHELLPROMPT, CLIPROMPT, LOGINPROMPT, EDITPROMPT], timeout = 2)
        else:
            # Not a prompt we recognise?  Exit.
            sys.exit('** Unknown prompt - unable to continue.')
    return STATE[0]


def writeConfig():
    print "** Entering edit mode"
    tn.write("edit\n")
    tn.read_until("#")
    # Set the root user's password:
    print "** creating config"
    tn.write("set system root-authentication plain-text-password\n")
    tn.read_until("assword:")
    tn.write(args.password + "\n")
    tn.read_until("assword:")
    tn.write(args.password + "\n")
    tn.read_until("#")
    # Set the IP address on the selected interface:
    tn.write("set interfaces " + args.interface + " unit 0 family inet address " + args.address + "\n")
    tn.read_until("#")
    # Set a static route:
    tn.write("set routing-options static route 0/0 next-hop " + args.route + "\n")
    tn.read_until("#")
    # Enable SSH so Ansible can do its stuff:
    tn.write("set system services ssh\n")
    tn.read_until("#")
    tn.write("set system services netconf ssh\n")
    tn.read_until("#")
    # Create user with password Axians:
    tn.write('set system login user axians-prestage class super-user authentication encrypted-password "$1$6EGiSTA8$QDcbHazUHHF9OH44QHjrw/"\n')
    tn.read_until("#")
    print "** Applying config"
    tn.write("commit and-quit\n")
    tn.read_until(">")




# Connect to the host
try:
  print "** connecting to %s on port %s..." % (HOST, PORT)
  tn = telnetlib.Telnet(HOST, PORT)

except socket.error:
  print "** Could not connect!"
  error = "TRUE"
else:
# Check the state of the device, logging out as necessary using stateCheck function
    deviceState = stateCheck()
    if deviceState != 2:
        print '** Device is in an unknown state - cannot continue: ' + deviceState
        deviceState = stateCheck()
    elif deviceState == 2:
        # Log into device
        print "** waiting for login"
        tn.write("\n")
        tn.read_until("ogin:", timeout=5)
        print "** Logging in with username = %s" % (USER)
        tn.write(USER + "\n")

        if PASS:
#            tn.set_debuglevel(1)
            print "** waiting for password"
            # Check if there's a prompt for a password
            passRequired = tn.expect([PASSPROMPT], timeout = 3)
            if passRequired[0] == 0:
                print "** Using password = %s" % (PASS)
                tn.write(PASS + "\n")
                # Check if the password is wrong
                passBad  = tn.expect([PASSFAIL], timeout = 3)
                if passBad[0] == 0:
                    sys.exit("Device needs a password but the wrong one was given")
                else:
                    # If password is good, start the CLI
                    print "** starting CLI"
                    tn.write("cli\n")
                    tn.read_until(">")
            else:
                # If no password, this must be a new box, so start CLI
                print "** No root password set - starting CLI"
                tn.write("cli\n")
                print tn.read_until(">")

            writeConfig()
            print "Device has been configured with IP address %s and a password of %s" % (args.address, args.password)
            tn.close()
        else:
           print ERROR

# print HW
# print VER