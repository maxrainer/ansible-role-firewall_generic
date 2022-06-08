# **Ansible Role for Firewall Demos**
## **Overview**
Generic Ansible role for different Firewall platforms.
Goal is to provide a generic useable way to configure Firewall rules on different platforms with the same input data schema.
Easy to be extended for other FW platforms. 
More features (p.e. NAT) to come. 

## **Plaforms supported**
* Juniper SRX
* PaloAlto PanOS
* Fortigate FortiOS
## **Topics covered**
* policy and rule configuration
* address book configuration
* methode: CLI commands
* methode: Jinja templates

## **Service Match**
For each supported platform there must be a static variable file defined in folder /vars.
These dicts match each generic service to a platform specific one. 
## **requirements**
depends on collections: 
* junipernetworks.junos
* paloaltonetworks.panos
* fortinet.fortios
## **data schema for rules**
```
fw_rules:
  - name: rule_C
    src:
      zone: "port2"
      addresses:
        - name: "inside_host_D"
          ipv4: "10.10.2.3"
    dest:
      zone: "port3"
      addresses:
        - name: "pub_host_A"
          type: host
          ipv4: "7.7.7.1"
        - name: "pub_host_B"
          type: host
          ipv4: "7.7.7.2"
    services:
      - http
      - https
    rule:
      action: "permit"
      logging_init: false
      logging_close: true
      ips_sensor: "default"
```
