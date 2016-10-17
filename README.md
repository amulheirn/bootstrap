# Readme
This module is (initially) Junos only.  It performs the following things:

* Gets to the Junos login prompt
* Logs in as root with no password
* Goes into edit mode
* Applies IP/mask, default route and root user's password
* Commits and quits

The script allows the operator to specify the interface name which will be used for the pre-staging activity.  This is to allow any interface to be used - me0, fxp0, ge-0/0/0 etc.

# Usage
Password, management interface, address/mask are all mandatory elements which must be passed as command-line arguments.
The default route is optional. 

` usage: bootstrap2.py [-h] -p PASSWORD -i INTERFACE -a ADDRESS [-r ROUTE]`