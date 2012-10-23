#!/bin/python26

import os, sys
import yaml
import pycurl
import StringIO, exceptions

def getInstanceId():
    curlObj = pycurl.Curl()
    curlObj.setopt(pycurl.URL, "http://localhost/") #This index.html should return an arbitrary string for instanceId
    #    curlObj.setopt(pycurl.URL, "http://169.254.169.254/latest/meta-data/instance-id") #production use
    buffer = StringIO.StringIO()
    curlObj.setopt(pycurl.WRITEFUNCTION, buffer.write)
    curlObj.setopt(pycurl.FOLLOWLOCATION, 1)
    curlObj.setopt(pycurl.MAXREDIRS, 1)
    curlObj.perform()
    return buffer.getvalue()

def getInstanceMeta():
    instance = getInstanceId()
    stream = file('SALTCMDB.yml', 'r')

#debugging
    for configDict in yaml.load_all(stream):
        if configDict['instance']['Id'] == instance:
#            print configDict['instance']['Id']
            #debug output, just return the configDict for usage by updateConfig in production use
            for key, value in configDict.iteritems():
                print "key: ", key, "value: ", value

    #return configDict

def updateConfigFile():
    MINION_CONFIG_FILE = "/etc/salt/minion"
    try:
        os.path.isfile(MINION_CONFIG_FILE)
    except IOError as e:
        print "Cannot read minion config file"

def main():
    getInstanceMeta() #replace with updateConfigFile when search and replace function is complete

if __name__ == "__main__":
    main()
