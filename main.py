# -*- coding: utf-8 -*-

from wox import Wox

import os
import json
import subprocess
import getpass

MSG = 'There is no WindowsTerminal'
ENABLED = False
p = 'C:\\Users\\' + getpass.getuser() + '\\AppData\\Local\\Packages'
for d in os.listdir(p):
    if d.startswith('Microsoft.WindowsTerminal'):
        p = p + '\\' + d + '\\LocalState\\settings.json'
        ENABLED = True
        LIST = []
        break
if ENABLED:
    try:
        with open(p, encoding='utf-8') as f:
            ob = json.load(f)
            LIST = ob["profiles"]["list"]
    except:
        MSG = 'Error in settings.json file'
    else:
        MSG = 'There is no MATCH'

class WindowsTerminal(Wox):

    def query(self, query):
        results = []
        if ENABLED:
            for item in LIST:
                if item["name"].lower().startswith("{}".format(query).lower()):
                    results.append({
                        "Title": item["name"],
                        "SubTitle": item["guid"],
                        "IcoPath":"Images/app.png",
                        "JsonRPCAction": {
                            'method': 'take_action',
                            'parameters': [item["name"]],
                            'dontHideAfterAction': False
                        }
                    })
        if len(results) == 0:
            results.append({
                "Title": MSG,
                "SubTitle": MSG,
                "IcoPath":"Images/app.png",
                "JsonRPCAction": {
                    'method': 'take_action',
                    'parameters': ["Nothing"],
                    'dontHideAfterAction': False
                }
            })
        return results

    def take_action(self, n):
        if n != 'Nothing':
            subprocess.run('wt -p "{}"'.format(n), shell=False)
        return None

if __name__ == "__main__":
    WindowsTerminal()
