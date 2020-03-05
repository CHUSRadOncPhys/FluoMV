#!/usr/bin/python
# -*- coding: utf-8 -*-
# The previous line is essential for python to recognise all non-generic ascii character

#///////////////////////////////////////////////////////////////////////////
#///////////////////////////////////////////////////////////////////////////
#//  Main
#//   (C) 2019 by Nicolas Tremblay <nmtremblay.chus@ssss.gouv.qc.ca>
#///////////////////////////////////////////////////////////////////////////
#///////////////////////////////////////////////////////////////////////////

import sys # command line args + exit
import os
from PyComView import *
import time

print "Starting PyComView"

#debug_file = open("C:\\temp\\debug.txt","w")
debug_file = open(os.getcwd() + "\\debugPyComView.txt","w",0)
#debug_file = os.fdopen(sys.stdout.fileno(), 'w', 0)
config_file = "config.txt"
old_stdout = sys.stdout     #Keeping old sys.stdout for later if needed
sys.stdout = debug_file


#Initialisation des valeurs par défaults
debug = 3

print "debug = {0}".format(debug)

#Nous faisons un dictionnaire avec toutes les configurations dans le fichier config.txt
try:
    test = PyComView(debug)
except:
    print "Error in main.py : PyComView(debug), initialization failed."
    debug_file.close()
    sys.stdout = old_stdout
    print "quitting software"
    sys.exit()

print "init completed"

try:
    test.loadConfigFromFile(config_file)
except:
    print "Error in main.py : test.loadConfigFromFile(config_file), Loading config file failed."
    debug_file.close()
    sys.stdout = old_stdout
    print "quitting software"
    sys.exit()

print "load of {0} completed".format(config_file)

#test.iComConnect("10.226.144.152", "stringMarche", "result\\") #Infinity3, mais de L'extérieur
try:
    test.iComConnect() #à partir du iView
except:
    print "Error in main.py : test.iComConnect(), Connecting iCOM failed."
    debug_file.close()
    sys.stdout = old_stdout
    print "quitting software"
    sys.exit()

print "connect completed"




print "Connecting iView"
try:
    iViewConnected = test.iViewInit()
except:
    print "Error in main.py : test.iViewInit(), Connecting iView failed."
    debug_file.close()
    sys.stdout = old_stdout
    print "quitting software"
    sys.exit()

    
if iViewConnected is 1:
    print "iView connection....Succeeded"
    #test.iViewSetSavingParameter("iViewtest", "image\\")
    #print "iView paramter set"
    test.iViewStartAcquireContinuous()  #On part l'acquisition en pause, en attente du trigger.
    print "iView Acquisition started"
else:
    print "iView connection...failed"
    
try:
    
    test.Save_iCOM_Messages()
    time.sleep(1)
    
except (KeyboardInterrupt, SystemExit):   #Lorsqu'on appuie sur Ctrl+c (a valider le fonctionnement)
    print "test.Save_iCOM_Messages() : Closing before finishing"
    test.iComDisconnect()
    print "iCOM disconnected"
    if iViewConnected is 1:
        test.iViewStopAcquireContinuous()
        print "iView Acquisition stopped"
        test.iViewClose()
        print "iView Disconnected"
    test.delete()
    print "pointer deleted"
    debug_file.close()
    sys.stdout = old_stdout
    print "quitting software"
    sys.exit()
except:
    print "test.Save_iCOM_Messages() : unknown Error"
    test.iComDisconnect()
    print "iCOM disconnected"
    if iViewConnected is 1:
        test.iViewStopAcquireContinuous()
        print "iView Acquisition stopped"
        test.iViewClose()
        print "iView Disconnected"
    test.delete()
    print "pointer deleted"
    debug_file.close()
    sys.stdout = old_stdout
    print "quitting software"
    sys.exit()


    

print "save finished"

test.iComDisconnect()
print "iCOM disconnected"

if iViewConnected is 1:
    
    test.iViewStopAcquireContinuous()
    print "iView Acquisition stopped"
    test.iViewClose()
    print "iView Disconnected"
    #sys.stdout.flush()



#"""
test.delete()

print "pointer deleted"

debug_file.close()

sys.stdout = old_stdout

print "quitting software"
             


