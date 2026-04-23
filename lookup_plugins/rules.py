#!/usr/bin/python
# Make coding more python3-ish, this is required for contributions to Ansible
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


from ansible.errors import AnsibleError, AnsibleParserError
from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display

display = Display()

import pandas as pd

def load_excel_file(file):
  df = pd.read_excel( file,
                    skiprows=1,
                    index_col=None,
                    dtype=object,
                    names=[
                        "rule_name",
                        "src_zone",
                        "src_name",
                        "src_ip",
                        "dst_zone",
                        "dst_name",
                        "dst_ip",
                        "service",
                        "action",
                        "logging_init",
                        "logging_close",
                        "ips_sensor",
                    ])
  return df

def generate_rules(df):
    lines=[]
    for index,row in df.iterrows():
        lines.append({
            "rule_name":row["rule_name"],
            "src_zone":row["src_zone"],
            "src_name":row["src_name"],
            "src_ip":row["src_ip"],
            "dst_zone":row["dst_zone"],
            "dst_name":row["dst_name"],
            "dst_ip":row["dst_ip"],
            "service":row["service"],
            "action":row["action"],
            "logging_init":row["logging_init"],
            "logging_close":row["logging_close"],
            "ips_sensor":row["ips_sensor"],
        })
    fw_rules=[]
    for line in lines:
        rule_name=line["rule_name"]
        src_adresses=[]
        dst_adresses=[]
        services=[]
        for a in lines:
            if a["rule_name"] == rule_name:
                src_zone=a["src_zone"]
                address={"name":a["src_name"],"ipv4":a["src_ip"]}
                if address not in src_adresses:
                    src_adresses.append({"name":a["src_name"],"ipv4":a["src_ip"]})

                dst_zone=a["dst_zone"]
                address={"name":a["dst_name"],"ipv4":a["dst_ip"]}
                if address not in dst_adresses:
                    dst_adresses.append({"name":a["dst_name"],"ipv4":a["dst_ip"]})

                if a["service"] not in services:
                    services.append(a["service"])

                rule = {
                        "action": a["action"],
                        "logging_init":a["logging_init"],
                        "logging_close":a["logging_close"],
                        "ips_sensor":a["ips_sensor"]
                    }

        fw_rule={ 
               "name":rule_name,
               "src":{
                   "zone": src_zone,
                   "addresses": src_adresses
               },
               "dest":{
                   "zone": dst_zone,
                   "addresses": dst_adresses
               },
               "services": services,
               "rule": rule
            }
        if fw_rule not in fw_rules:
            fw_rules.append(fw_rule)

    return fw_rules

class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        for term in terms:
            display.debug("File lookup term: %s" % term)
            lookupfile = self.find_file_in_search_path(variables, 'files', term)
            display.vvvv(u"File lookup using %s as file" % lookupfile)
            try:
                if lookupfile:
                    df = load_excel_file(lookupfile)
                else:
                      # Always use ansible error classes to throw 'final' exceptions,
                      # so the Ansible engine will know how to deal with them.
                      # The Parser error indicates invalid options passed
                    raise AnsibleParserError()
            except Exception:
                raise AnsibleError("could not locate file in lookup: %s" % term)

        return generate_rules(df)

