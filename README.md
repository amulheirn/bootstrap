# Readme
This module is (initially) Junos only.  It performs the following things:

* Gets to the Junos login prompt
* Logs in as root with no password
* Goes into edit mode
* Applies IP/mask, default route and root user's password
* Commits and quits

# Usage
Password, management interface, address/mask are all mandatory elements which must be passed as command-line arguments.
The default route is optional. 

` usage: bootstrap2.py [-h] -p PASSWORD -i INTERFACE -a ADDRESS [-r ROUTE]`