# **Ansible Role for Firewall Demos**
## **Overview**
Ansible role for different Firewall platforms.
## **Plaforms supported
* Juniper SRX
* PaloAlto PanOS
## **Topics covered**
* policy and rule configuration
* address book configuration
* methode: CLI commands
* methode: Jinja templates

## Service Match
For each supported platform there must be a static variable file defined in folder /vars.
These dicts match each generic service to a platform specific one. 
## **requirements**
depends on collections: 
* junipernetworks.junos
* paloaltonetworks.panos


