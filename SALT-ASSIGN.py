#!/bin/python26

import os, sys
import yaml
import pycurl
import StringIO


# TODO check if the minion config already exists, if so, delete it
# TODO instead of doing a search and replace, dump yaml to conf.d

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

def writeSaltMinionConfig():
    instance = getInstanceId()
    stream = file('SALTCMDB.yml', 'r')
    MINION_CONFIG_FILE = "minion"
    TEST_CONFIG_FILE = open("testMinionConfig", "w")

    #   MINION_CONFIG_FILE = "/etc/salt/minion" #production use

    for configDict in yaml.load_all(stream):
        if configDict['instance']['id'] == instance:
            #assign local variables
#            saltId =

            TEST_CONFIG_FILE.write("id: " + configDict['instance']['saltId'] + "\n")
            yaml.dump(configDict['instance']['grains'], TEST_CONFIG_FILE)

            TEST_CONFIG_FILE.close()

            #debug:
#            for key, value in configDict.iteritems():
#                print "key: ", key, "value: ", value


#def fixShit():
##ugly hack to add tabs, I know yaml.dump will maintain the format, but its not for some reason
#    with open("testMinionConfig", "w") as minionConfig:
#        lines = minionConfig.readlines()
#        for line in lines:
#            try:
#                minionConfig.write(re.sub(r'^environment', '\tenvironment', line))
#            except ValueError:
#                print "Could not parse regex"

def main():
    writeSaltMinionConfig()
    fixShit()

if __name__ == "__main__":
    main()
