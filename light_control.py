#!/bin/py????????
import cgi, os, sys

print 'Content-Type: text/plain\n'

if 'PATH_INFO' in os.environ:
    print os.environ['PATH_INFO']
form = cgi.FieldStorage()
if 'param' in form:
    print form['param'].value

import datetime
from os import rename

signal_dict_on = {
'la': 1111,
'l1': 1110,
'l2': 1010,
'l3': 1100,
'l4': 1000 }

signal_dict_off = {
'la': 0111,
'l1': 0110,
'l2': 0010,
'l3': 0100,
'l4': 0000 }

def getCurrentTime():
    hour = datetime.datetime.now().hour
    minute = str(datetime.datetime.now().minute)
    currentTime = hour*2
    if len(minute) > 1 and minute[0] == '3':
        currentTime += 1
    return currentTime

def getCurrentState(light):
    r = open("light_state","r")
    line = r.readline()
    while line != '':
        if line[:2] == light:
            r.close()
            return line[3]
        line = r.readline()
    r.close()
    return '1'

def getOverrideState(light):
    r = open("light_state","r")
    line = r.readline()
    while line != '':
        if line[:2] == light and line[4] == 'o':
            r.close()
            return True
        elif line[:2] == light and line[4] != 'o':
            r.close()
            return False
        line = r.readline()
    r.close()
    return False

def removeOverride(light):
    r = open("light_state","r")
    r1 = open("light_state_temp","w")
    line = r.readline()
    while line != '':
        if line[:2] == light:
            state = line[3]
            r1.write(light+' '+state+'\n')
            print(light+': REMOVE OVERRIDE')
        else:
            r1.write(line)
        line = r.readline()
    rename("light_state_temp", "light_state")
    r.close()
    r1.close()

def writeState(light, state, override):
    r = open("light_state","r")
    r1 = open("light_state_temp","w")
    line = r.readline()
    while line != '':
        if line[:2] == light:
            if override == True:
                r1.write(light+' '+state+'o\n')
                print(light+': OVERRIDDEN')
            elif override == False:
                r1.write(light+' '+state+'\n')
        else:
            r1.write(line)
        line = r.readline()
    rename("light_state_temp", "light_state")
    r.close()
    r1.close()

def switch(light, newState, override):
    if newState == '0':
        print(light+' signal OFF: '+str(signal_dict_off[light]))
        writeState(light, '0', override)
    elif newState == '1':
        print(light+' signal ON: '+str(signal_dict_on[light]))
        writeState(light, '1', override)

def executeSchedule():
    ignoreOverride = False
    currentTime = getCurrentTime()
    currentState = '0'
    
    r = open("light_schedule","r")
    line = r.readline()
    
    while line != '':
        if line[:2] == 'la':
            data = line[3:52]
            newState = data[currentTime]
            r1 = open("light_state","r")
            line1 = r1.readline()
            while line1 != '':
                light = line1[:2]
                if getOverrideState(light) == False and getCurrentState(light) != newState:
                    switch(light, newState, False)
                if getOverrideState(light) == True and getCurrentState(light) == newState:
                    removeOverride(light)
        
        elif line[0] == 'l' and line[1] != '#' and line[:2] != 'la':
            light = line[:2]
            data = line[3:52]
            newState = data[currentTime]
            print(light+' '+getCurrentState(light)+' '+str(getCurrentTime())+' '+newState+' '+data)
            
            if getOverrideState(light) == False and getCurrentState(light) != newState:
                switch(light, newState, False)
            if getOverrideState(light) == True and getCurrentState(light) == newState:
                removeOverride(light)
            line = r.readline()
        else:
            line = r.readline()
    r.close()
