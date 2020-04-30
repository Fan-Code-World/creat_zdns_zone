#!/usr/bin/env python
# coding=utf-8
import os
import requests
import json
import base64
import time
import glob
import sys
requests.packages.urllib3.disable_warnings()


class Creat:
    
    def creatMasterZone(self,view_id, name, zone_content):
        url = 'https://%s:20120/views/%s/zones' % (ZDNS_CMS_ADDRESS, view_id)
        params = {'name': name,
                  'owners': ['local.master'],
                  'server_type': 'master',
                  'default_ttl': '3600',
                  'slaves': [],
                  'ad_controller': [],
                  'zone_content': zone_content}
        headers = {'Content-type': 'application/json'}
        r = requests.post(url, data=json.dumps(params),headers=headers, auth=('admin', 'admin'), verify=False)
        return (r.status_code)
    
    
    def creatSlaveZone(self,view_id, name):
        url = 'https://10.1.112.92:20120/views/%s/zones' % (view_id)
        params = {'name': name,
                  'owners': ['local.master'],
                  'server_type': 'slave',
                  'masters': ['10.1.112.91'],
                  'slaves': [],
                  'ad_controller': [],
                  'update_controller': [],
                  'renewal': 'no'}
        headers = {'Content-type': 'application/json'}
        r = requests.post(url, data=json.dumps(params),
                          headers=headers, auth=('admin', 'admin'), verify=False)
        return (r.status_code)
    
    
    def encodeZoneFile(self, file_name):
        f = file('zone_file/' + file_name, 'r')
        content = f.read()
        f.close()
        zone_content = base64.b64encode(content)
        return zone_content

if __name__ == '__main__':
    path_filename = os.listdir('zone_file')
    VIEW_NAME = 'default'
    ZDNS_CMS_ADDRESS = '127.0.0.1'

    t = Creat()
    for i  in  range(len(path_filename) ):
        suffix = path_filename[i].split('.')[-1]
        zone_name = path_filename[i].replace(suffix, '')  
        return_code = t.creatMasterZone(VIEW_NAME, zone_name ,t.encodeZoneFile(path_filename[i]))  

        if return_code == 200:
            print zone_name, return_code, '------>', 'creat success'
        else:
            print zone_name, return_code, '------>', 'creat failed'
        time.sleep(1)
 
