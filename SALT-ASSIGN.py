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

    # Using yaml.load only returns the last document.
    # This returns a generator type object instead of a dict, the Python docs
    # don't really describe how to work with this
    myDict = yaml.load(stream)
    #changing this to load_all creates a generator object, something I'm not sure why
    # or how to match my dict.

# simpler printing
#    if myDict.has_key('instanceId') == True:
#        for key in myDict:
#             print key, myDict[key] #just get this to print for now

#debug printing:
##bug key, value mappings for nested keys not working

    if myDict.has_key('instance') == True:
        for key in myDict:
            print "key:" + key + " " + "value: " +  myDict[key] + "\n"

    #return myDict


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
