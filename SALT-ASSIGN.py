#!/bin/python26

import yaml
import pycurl
import StringIO

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
    instanceId = getInstanceId()
    stream = file('SALTCMDB.yml', 'r')

    # Using yaml.load only returns the last document.
    # This returns a generator type object instead of a dict, the Python docs
    # don't really describe how to work with this
    myDict = yaml.load(stream)

    #the following does not work
    if myDict.has_key('instanceId') == True:
        for key in myDict:
             print key, myDict[key] #just get this to print for now


def main():
    getInstanceMeta()

if __name__ == "__main__":
    main()
