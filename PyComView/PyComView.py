#!/usr/bin/python
# -*- coding: utf-8 -*-
# The previous line is essential for python to recognise all non-generic ascii character
#include <Python.h>

#///////////////////////////////////////////////////////////////////////////
#///////////////////////////////////////////////////////////////////////////
#//  PyComView
#//   (C) 2019 by Nicolas Tremblay <nmtremblay.chus@ssss.gouv.qc.ca>
#///////////////////////////////////////////////////////////////////////////
#///////////////////////////////////////////////////////////////////////////

import sys # command line args + exit
import os
import ctypes as c
import ctypes.wintypes as cwin
#import msvcrt as msvcrt
import time
import copy


class PyComView(object):

    def __init__(self, Debug = 0):
        """Load la librairie dll et initialise quelques variables"""

        self.debug = Debug

        #Creating the debug fil and redirecting the prints to this file
        self.debug_file = open(os.getcwd() + "\\debugPyComView.txt","w",0)
        self.old_stdout = sys.stdout     #Keeping old sys.stdout for later if needed
        sys.stdout = self.debug_file


        pathDLL = os.getcwd() + "\\iCom_iView.dll"
        self.ComViewDLL = c.CDLL(pathDLL)

        self.ComViewDLL.Create_iCOMListen.restype = c.c_void_p

        try:
            self.iCOMiViewObject = self.ComViewDLL.Create_iCOMListen()
        except:
            print "PyComView::__init__ : self.ComViewDLL.Create_iCOMListen() failed. Exiting software"
            sys.exit()


        #Setting default values that can be changed by the config.txt file
        self.configData = {}
        
        self.configData["timestamp"] = 0    #
        self.configData["ip_iCOM"] = "192.168.30.2"  #"10.226.144.152"
        self.configData["use_iView"] = True
        self.configData["use_iCOM"] = True
        self.configData["acquisition_name"] = "acq"
        self.configData["acquisition_path"] = "result\\"
        self.configData["acquisition_timout_sec"] = 120
        self.configData["iCOM_summary_only"] = False
        self.configData["iCOM_tag_list_in_summary"] = True
        self.configData["iCOM_use_start_acquisition_trigger"] = False
        self.configData["iCOMsavingPathMode"] = 0
        self.configData["debug"] = self.debug    #


    def __del__(self):
        """ """
        pass
    

       
    #Fonctions iCOM
    def iComConnect(self, linac_ip_adress = None, filenames = None, filepath = None):
        """ """
        if self.configData["use_iCOM"]:
            if linac_ip_adress is None:
                linac_ip_adress = self.configData["ip_iCOM"]
            if filenames is None:
                filenames = self.configData["acquisition_name"]
            if filepath is None:
                filepath = self.configData["acquisition_path"]

            if self.debug > 0:
                print "PyComView::iComConnect : Connecting {0}".format(linac_ip_adress)

            #For debug purposes, pinging the IP adress
            if self.debug > 1:
                if os.system("ping -t -n 1 " + linac_ip_adress) != 0:
                    print "Ping of the adress {0} doesn't work, we won't try the connection.".format(linac_ip_adress)
                    return 0

            try:
                result = self.ComViewDLL.Call_Connect_iCOM_Vx(self.iCOMiViewObject, c.c_char_p(linac_ip_adress), c.c_char_p(filenames), c.c_char_p(filepath))
            except:
                result = -1
                print "PyComView::iComConnect : Connection failed. Fonction Call_Connect_iCOM_Vx a planté."
                
            if result == 0:
                print 'PyComView::iComConnect : The C Function "Call_Connect_iCOM_Vx" returns an error.'
        else:
            result = 0
        return result
        
    def iComDisconnect(self):
        """ """

        result = self.ComViewDLL.Call_Disconnect_iCOM(self.iCOMiViewObject)

        if result == -1:
            print 'PyComView::iComDisconnect : The C Function "Call_Disconnect_iCOM" returns an error.'
        
 
    def Save_iCOM_Messages(self, nbrSeconds = None, tagListInSummary = None, SumaryOnly = None):
        """ """

        if self.configData["use_iCOM"]:
            if nbrSeconds is None:
                nbrSeconds = self.configData["acquisition_timout_sec"]
            if tagListInSummary is None:
                tagListInSummary = self.configData["iCOM_tag_list_in_summary"]
            if SumaryOnly is None:
                SumaryOnly = self.configData["iCOM_summary_only"]
                
            if tagListInSummary is False and SumaryOnly is True:
                tagListInSummary = True
            
            try:
                result = self.ComViewDLL.Call_Save_iCOM_Messages(self.iCOMiViewObject, c.c_uint(nbrSeconds),c.c_bool(tagListInSummary),c.c_bool(SumaryOnly))
            except:
                print "Error in PyComView::Save_iCOM_Messages : 'try' échoué, fait une erreur lorsque lancé dans Python."
                return -1

            if result == -1:
                print 'PyComView::Save_iCOM_Messages : The C Function "Call_Save_iCOM_Messages" returns an error.'
        else:
            #Si iCOM n'est pas utilisé, alors on ne fait q'attendre pendant l'acquisition iView
            time.sleep(self.configData["acquisition_timout_sec"])
            result = 0

        return result
       

    def iCOMSetSavingParameter(self, filenames = None, filepath = None, saving_path_mode = None):
        """ """

        if filenames == None:
            try:
                filenames = self.configData["acquisition_name"]
            except:
                filenames = ""

        if filepath == None:
            try:
                filepath = self.configData["acquisition_path"]
            except:
                filepath = "result\\"
        if saving_path_mode == None:
            try:
                saving_path_mode = self.configData["iCOMsavingPathMode"]
            except:
                saving_path_mode = 0
            
        try:
            result = self.ComViewDLL.Call_SetSavingParameter(self.iCOMiViewObject, c.c_char_p(filenames), c.c_char_p(filepath), c.c_short(saving_path_mode))
        except:
            print "Error in PyComView::iCOMSetSavingParameter : 'try' échoué, fait une erreur lorsque lancé dans Python."

        if result == -1:
            print 'PyComView::iCOMSetSavingParameter : The C Function "Call_SetSavingParameter" returns an error.'


    def iCOMSetAcquisitionParameter(self, useStartAcquisitionTrigger = None, iCOMtagListInSummary = None
                                   , iCOMsaveSummaryOnly = None, acquisitionTimeoutSeconds = None):
        """Si la valeur est à None, le paramètre dans le dictionnaire par défaut est utilisé."""

        if(useStartAcquisitionTrigger is not None):
            try:
                result = self.ComViewDLL.Set_useStartAcquisitionTrigger(self.iCOMiViewObject, c.c_bool(useStartAcquisitionTrigger))
                if result == -1:
                    print 'PyComView::SetAcquisitionParameter : The C Function "Set_useStartAcquisitionTrigger" returns an error.'
            except:
                print "Error in PyComView::iCOMSetAcquisitionParameter : useStartAcquisitionTrigger ne semble pas booléen."
        else:
            try:
                result = self.ComViewDLL.Set_useStartAcquisitionTrigger(self.iCOMiViewObject, c.c_bool(self.configData["iCOM_use_start_acquisition_trigger"]))
                if result == -1:
                    print 'PyComView::SetAcquisitionParameter : The C Function "Set_useStartAcquisitionTrigger" returns an error.'
            except:
                pass

        if(iCOMtagListInSummary is not None):
            try:
                result = self.ComViewDLL.Set_iCOMtagListInSummary(self.iCOMiViewObject, c.c_bool(iCOMtagListInSummary))
                if result == -1:
                    print 'PyComView::SetAcquisitionParameter : The C Function "Set_iCOMtagListInSummary" returns an error.'
            except:
                print "Error in PyComView::iCOMSetAcquisitionParameter : iCOMtagListInSummary ne semble pas booléen."
        else:
            try:
                result = self.ComViewDLL.Set_iCOMtagListInSummary(self.iCOMiViewObject, c.c_bool(self.configData["iCOM_tag_list_in_summary"]))
                if result == -1:
                    print 'PyComView::SetAcquisitionParameter : The C Function "Set_iCOMtagListInSummary" returns an error.'
            except:
                pass

        if(iCOMsaveSummaryOnly is not None):
            try:
                result = self.ComViewDLL.Set_iCOMsaveSummaryOnly(self.iCOMiViewObject, c.c_bool(iCOMsaveSummaryOnly))
                if result == -1:
                    print 'PyComView::SetAcquisitionParameter : The C Function "Set_iCOMsaveSummaryOnly" returns an error.'
            except:
                print "Error in PyComView::iCOMSetAcquisitionParameter : iCOMsaveSummaryOnly ne semble pas booléen."
        else:
            try:
                result = self.ComViewDLL.Set_iCOMsaveSummaryOnly(self.iCOMiViewObject, c.c_bool(self.configData["iCOM_summary_only"]))
                if result == -1:
                    print 'PyComView::SetAcquisitionParameter : The C Function "Set_iCOMsaveSummaryOnly" returns an error.'
            except:
                pass

        if(acquisitionTimeoutSeconds is not None):
            try:
                result = self.ComViewDLL.Set_acquisitionTimeoutSeconds(self.iCOMiViewObject, c.c_uint(acquisitionTimeoutSeconds))
                if result == -1:
                    print 'PyComView::SetAcquisitionParameter : The C Function "Set_acquisitionTimeoutSeconds" returns an error.'
            except:
                print "Error in PyComView::iCOMSetAcquisitionParameter : acquisitionTimeoutSeconds ne semble pas Unsigned Int."
        else:
            try:
                result = self.ComViewDLL.Set_acquisitionTimeoutSeconds(self.iCOMiViewObject, c.c_uint(self.configData["acquisition_timout_sec"]))
                if result == -1:
                    print 'PyComView::SetAcquisitionParameter : The C Function "Set_acquisitionTimeoutSeconds" returns an error.'
            except:
                pass


    def iCOMClearTriggerLists(self, ClearStartTriggerList = True, ClearPauseTriggerList = True, ClearStopTriggerList = True):
        """ """

        if ClearStartTriggerList is True:
            result = self.ComViewDLL.Call_Clear_iCOMstartTriggerList(self.iCOMiViewObject)
            if result == -1:
                print 'PyComView::iCOMClearTriggerLists : The C Function "Call_Clear_iCOMstartTriggerList" returns an error.'

        if ClearPauseTriggerList is True:
            result = self.ComViewDLL.Call_Clear_iCOMpauseTriggerList(self.iCOMiViewObject)
            if result == -1:
                print 'PyComView::iCOMClearTriggerLists : The C Function "Call_Clear_iCOMpauseTriggerList" returns an error.'

        if ClearStopTriggerList is True:
            result = self.ComViewDLL.Call_Clear_iCOMstopTriggerList(self.iCOMiViewObject)
            if result == -1:
                print 'PyComView::iCOMClearTriggerLists : The C Function "Call_Clear_iCOMstopTriggerList" returns an error.'


    def iCOMAddStartTriggerToList(self, tagValue_or_linacState, trigOnValueChange = False, tag = None, part=None, TriggerType = None):
        """ Si tag et part sont à None, alors on assume que le trigger est un état du linac (linac state)
            Les valeurs peuvent être des listes ou des valeurs simples.
        """

        if(tag is None or part is None or TriggerType == 1 or TriggerType == 2 or TriggerType == 3):    #Trigger avec un Linac State ou linac Function Mode ou Keyboard key
            if TriggerType == None:    #Default Trigger Linac State
                TriggerType = 1
                
            try:    #si ce sont des listes
                lenght = min([len(tagValue_or_linacState),len(trigOnValueChange)])

                for i in range(0,lenght):
                    result = self.ComViewDLL.Call_Add_iCOMstartTriggerToList_NonTag(self.iCOMiViewObject
                                                                                    , c.c_bool(trigOnValueChange[i])
                                                                                    , c.c_short(tagValue_or_linacState[i])
                                                                                    , c.c_short(TriggerType[i]))
                    if result == -1:
                        print 'PyComView::iCOMAddStartTriggerToList : The C Function "Call_Add_iCOMstartTriggerToList_NonTag" returns an error.'
            except: #autrement on essaie des valeurs simples.
                try:
                    result = self.ComViewDLL.Call_Add_iCOMstartTriggerToList_NonTag(self.iCOMiViewObject
                                                                                    , c.c_bool(trigOnValueChange)
                                                                                    , c.c_short(tagValue_or_linacState)
                                                                                    , c.c_short(TriggerType))
                    if result == -1:
                        print 'PyComView::iCOMAddStartTriggerToList : The C Function "Call_Add_iCOMstartTriggerToList_NonTag" returns an error.'
                except:
                    print "Error in PyComView::iCOMAddStartTriggerToList (linacFunctionMode): parametre(s) probablement invalide(s)."
        else:   #Trigger avec un tag iCOM
            try:    #si ce sont des listes
                lenght = min([len(tagValue_or_linacState),len(trigOnValueChange),len(tag),len(part)])
                for i in range(0,lenght):
                    result = self.ComViewDLL.Call_Add_iCOMstartTriggerToList_tag(self.iCOMiViewObject, c.c_ulong(tag[i])
                                                                                , c.c_char(part[i])
                                                                                , c.c_bool(trigOnValueChange[i])
                                                                                , c.c_char_p(tagValue_or_linacState)[i] )
                    if result == -1:
                        print 'PyComView::iCOMAddStartTriggerToList : The C Function "Call_Add_iCOMstartTriggerToList_tag" returns an error.'
            except: #autrement on essaie des valeurs simples.
                try:
                    result = self.ComViewDLL.Call_Add_iCOMstartTriggerToList_tag(self.iCOMiViewObject, c.c_ulong(tag)
                                                                                , c.c_char(part)
                                                                                , c.c_bool(trigOnValueChange)
                                                                                , c.c_char_p(tagValue_or_linacState))
                    if result == -1:
                        print 'PyComView::iCOMAddStartTriggerToList : The C Function "Call_Add_iCOMstartTriggerToList_tag" returns an error.'
                except:
                    print "Error in PyComView::iCOMAddStartTriggerToList (tag): parametre(s) probablement invalide(s)."

    def iCOMAddPauseTriggerToList(self, tagValue_or_linacState, trigOnValueChange = False, tag = None, part=None, TriggerType = None):
        """ Si tag et part sont à None, alors on assume que le trigger est un état du linac (linac state)
            Les valeurs peuvent être des listes ou des valeurs simples.
        """

        if(tag is None or part is None or TriggerType == 1 or TriggerType == 2 or TriggerType == 3):    #Trigger avec un Linac State ou linac Function Mode ou Keyboard key
            if TriggerType == None:    #Default Trigger Linac State
                TriggerType = 1
                
            try:    #si ce sont des listes
                lenght = min([len(tagValue_or_linacState),len(trigOnValueChange)])

                for i in range(0,lenght):
                    result = self.ComViewDLL.Call_Add_iCOMpauseTriggerToList_NonTag(self.iCOMiViewObject
                                                                                    , c.c_bool(trigOnValueChange[i])
                                                                                    , c.c_short(tagValue_or_linacState[i])
                                                                                    , c.c_short(TriggerType[i]))
                    if result == -1:
                        print 'PyComView::iCOMAddPauseTriggerToList : The C Function "Call_Add_iCOMpauseTriggerToList_NonTag" returns an error.'
            except: #autrement on essaie des valeurs simples.
                try:
                    result = self.ComViewDLL.Call_Add_iCOMpauseTriggerToList_NonTag(self.iCOMiViewObject
                                                                                    , c.c_bool(trigOnValueChange)
                                                                                    , c.c_short(tagValue_or_linacState)
                                                                                    , c.c_short(TriggerType))
                    if result == -1:
                        print 'PyComView::iCOMAddPauseTriggerToList : The C Function "Call_Add_iCOMpauseTriggerToList_NonTag" returns an error.'
                except:
                    print "Error in PyComView::iCOMAddPauseTriggerToList (linacFunctionMode): parametre(s) probablement invalide(s)."
        else:   #Trigger avec un tag iCOM
            try:    #si ce sont des listes
                lenght = min([len(tagValue_or_linacState),len(trigOnValueChange),len(tag),len(part)])
                for i in range(0,lenght):
                    result = self.ComViewDLL.Call_Add_iCOMpauseTriggerToList_tag(self.iCOMiViewObject, c.c_ulong(tag[i])
                                                                                , c.c_char(part[i])
                                                                                , c.c_bool(trigOnValueChange[i])
                                                                                , c.c_char_p(tagValue_or_linacState)[i] )
                    if result == -1:
                        print 'PyComView::iCOMAddPauseTriggerToList : The C Function "Call_Add_iCOMpauseTriggerToList_tag" returns an error.'
            except: #autrement on essaie des valeurs simples.
                try:
                    result = self.ComViewDLL.Call_Add_iCOMpauseTriggerToList_tag(self.iCOMiViewObject, c.c_ulong(tag)
                                                                                , c.c_char(part)
                                                                                , c.c_bool(trigOnValueChange)
                                                                                , c.c_char_p(tagValue_or_linacState))
                    if result == -1:
                        print 'PyComView::iCOMAddPauseTriggerToList : The C Function "Call_Add_iCOMpauseTriggerToList_tag" returns an error.'
                except:
                    print "Error in PyComView::iCOMAddPauseTriggerToList (tag): parametre(s) probablement invalide(s)."


    def iCOMAddStopTriggerToList(self, tagValue_or_linacState, trigOnValueChange = False, tag = None, part=None, TriggerType = None):
        """ Si tag et part sont à None, alors on assume que le trigger est un état du linac (linac state)
            Les valeurs peuvent être des listes ou des valeurs simples.
        """

        if(tag is None or part is None or TriggerType == 1 or TriggerType == 2 or TriggerType == 3):    #Trigger avec un Linac State ou linac Function Mode ou Keyboard key
            if TriggerType == None:    #Default Trigger Linac State
                TriggerType = 1
                
            try:    #si ce sont des listes
                lenght = min([len(tagValue_or_linacState),len(trigOnValueChange)])

                for i in range(0,lenght):
                    result = self.ComViewDLL.Call_Add_iCOMstopTriggerToList_NonTag(self.iCOMiViewObject
                                                                                    , c.c_bool(trigOnValueChange[i])
                                                                                    , c.c_short(tagValue_or_linacState[i])
                                                                                    , c.c_short(TriggerType[i]))
                    if result == -1:
                        print 'PyComView::iCOMAddStopTriggerToList : The C Function "Call_Add_iCOMstopTriggerToList_NonTag" returns an error.'
            except: #autrement on essaie des valeurs simples.
                try:
                    result = self.ComViewDLL.Call_Add_iCOMstopTriggerToList_NonTag(self.iCOMiViewObject
                                                                                    , c.c_bool(trigOnValueChange)
                                                                                    , c.c_short(tagValue_or_linacState)
                                                                                    , c.c_short(TriggerType))
                    if result == -1:
                        print 'PyComView::iCOMAddStopTriggerToList : The C Function "Call_Add_iCOMstopTriggerToList_NonTag" returns an error.'
                except:
                    print "Error in PyComView::iCOMAddStopTriggerToList (linacFunctionMode): parametre(s) probablement invalide(s)."
        else:   #Trigger avec un tag iCOM
            try:    #si ce sont des listes
                lenght = min([len(tagValue_or_linacState),len(trigOnValueChange),len(tag),len(part)])
                for i in range(0,lenght):
                    result = self.ComViewDLL.Call_Add_iCOMstopTriggerToList_tag(self.iCOMiViewObject, c.c_ulong(tag[i])
                                                                                , c.c_char(part[i])
                                                                                , c.c_bool(trigOnValueChange[i])
                                                                                , c.c_char_p(tagValue_or_linacState)[i] )
                    if result == -1:
                        print 'PyComView::iCOMAddStopTriggerToList : The C Function "Call_Add_iCOMstopTriggerToList_tag" returns an error.'
            except: #autrement on essaie des valeurs simples.
                try:
                    result = self.ComViewDLL.Call_Add_iCOMstopTriggerToList_tag(self.iCOMiViewObject, c.c_ulong(tag)
                                                                                , c.c_char(part)
                                                                                , c.c_bool(trigOnValueChange)
                                                                                , c.c_char_p(tagValue_or_linacState))
                    if result == -1:
                        print 'PyComView::iCOMAddStopTriggerToList : The C Function "Call_Add_iCOMstopTriggerToList_tag" returns an error.'
                except:
                    print "Error in PyComView::iCOMAddStopTriggerToList (tag): parametre(s) probablement invalide(s)."


    def iCOMClearTagList(self):
        """ """
        result = self.ComViewDLL.Call_ClearTagList(self.iCOMiViewObject)
        if result == -1:
            print 'PyComView::iCOMClearTagList : The C Function "Call_ClearTagList" returns an error.'


    def iCOMAddTagToList(self, tag, part):
        """ Ajoute des tags a la liste des tags enregistres dans le resume d'acquisition iCOM.
            Peut ajouter des listes de tag ou des tags individuels
            Part possible : 'P' Prescribed, 'S' Set, 'R' Run
        """
        try:
            lenght = min([len(tag),len(part)])

            for i in range(0,lenght):
                result = self.ComViewDLL.Call_AddTagToList(self.iCOMiViewObject, c.c_ulong(tag[i]), c.c_char(part[i]))
                if result == -1:
                    print 'PyComView::iCOMAddTagToList : The C Function "Call_AddTagToList" returns an error.'
        except:
            try:
                result = self.ComViewDLL.Call_AddTagToList(self.iCOMiViewObject, c.c_ulong(tag), c.c_char(part))
                if result == -1:
                    print 'PyComView::iCOMAddTagToList : The C Function "Call_AddTagToList" returns an error.'
            except:
                print "Error in PyComView::iCOMAddTagToList : tag or part invalid."

    def loadConfigFromFile(self, configFile = "config.txt", ):
        """ Charge les configurations a partir d'un fichier texte.
            La fonction charge le document ligne par ligne et crée un dictionnaire qui
            permet de charger diverses valeurs. Si la valeur et inconnue elle ne sera
            pas utilisee.
            La nomencalture doit etre respectee pour que la fonction marche correctement.
            Le nom de la valeur est a gauche, suivi du symole "=" avec la valeur a assigner a droite.
            Si plusieurs parametres son necessaires, ceux-ci doivent etre separes par des ","
            Si plusieurs valeurs (ou series de parametres) doivent etre entre, ils doivent etre separes par des ";"
            le symbole "#" precede les commentaire (ignore par le code)
            Exemple de "config.txt":
                    #Commentaires
                    debug[int]=2
                    use_iView[bool]=1
                    use_iCOM[bool]=1
                    ip_iCOM=192.168.30.2  #10.226.144.152
                    acquisition_name=test
                    acquisition_path=C:\\temp\\
                    acquisition_timout_sec[int]=90
                    iCOM_summary_only[bool]=0
                    iCOM_tag_list_in_summary[bool]=1
                    iCOM_use_start_acquisition_trigger[bool]=1
                    iCOMSetStartTriggerList[int,bool,None,None,int]=10,0,None,None,1
                    iCOMSetPauseTriggerList[int,bool,None,None,int]=13,0,None,None,1
                    #iCOMSetStopTriggerList[int,bool,None,None,int]+=10,0,None,None,1
                    #iCOMSetStopTriggerList[longHexa,str,bool,str]+=0x50010007,R,0,valueExemple,0
                    iCOMSetSummaryTagList[longHexa,str]=0x50010007,R;0x50010006,R;0x70010007,P;0x70010008,R;0x70010001,P;0x50010003,R
            """

        #Nous faisons un dictionnaire avec toutes les configurations dans le fichier config.txt
        newConfigData = {}
        
        with open(configFile, "r") as f:
            for line in f:
                try:
                    #On enlève les commentaire (à partir du caractère "#"
                    #On enleve les espaces à gauche
                    #On sépare le nom des variables et les valaur qui sont séparées par le "+="
                    #On sépare le nom des variables et les valaur qui sont séparées par le "="
                    result1 = ((line.split("#")[0]).lstrip()).split("+=")
                    ajout = False
                    
                    if len(result1) < 2:    #S'il n'y a pas de "+=" dans la ligne
                        result1 = ((line.split("#")[0]).lstrip()).split("=")
                        if len(result1) < 2:    #S'il n'y a pas de "=" dans la ligne
                            continue
                    else:
                        ajout = True

                    
                    #On isoles les types des variables qui sont entre []
                    result2 = (result1[0].rstrip()).split("[")
                    nom = result2[0]
                    if len(result2) > 1:
                        varTypes = (result2[1].rstrip("]")).split(",")
                    else:
                        varTypes = []

                    if len(varTypes) > 0: #pour eviter des erreurs
                        for i in range(len(varTypes)):
                            if varTypes[i] == "None" or varTypes[i] == "none":
                                varTypes[i] = "self.NoneValue"
                            elif varTypes[i] == "bool" or varTypes[i] == "boolStr":
                                varTypes[i] = "self.boolStr"
                            elif varTypes[i] == "longHexa":
                                varTypes[i] = "self.longHexa" 

                    #On sépare les series de valeurs qui sont separees par de ";"
                    result3 = ((result1[1].rstrip()).lstrip()).split(";")   #On passage, on s'assure qu'il n'y a pas d'espace à la fin

                    #On separe les valeurs de chaque series qui sont separees par des ","
                    result4 = []
                    for serie in result3:   #pour chaque serie
                        temp1 = (serie.split(","))  #on separe les valeurs qui sont separees par des virgules
                        temp2 = []

                        if len(varTypes) >= len(temp1):
                            for i in range(len(temp1)): #pour toutes les valeurs
                                try:
                                   exec("temp2.append(" + varTypes[i] + "(temp1[i]))")  #on donne le bon type (bool, int, etc.) à la valeur
                                except:
                                    temp2.append(temp1[i])   #Si ca ne marche pas on laisse ca en string
                        else:
                            temp2 = temp1     #S'il n'y a pas de string, on fait un copie de la liste de string

                        if len(temp2) == 1: #S'il n'y a qu'un objet, on n'envoie pas un liste, mais un objet seul
                            result4.append(copy.deepcopy(temp2[0]))
                        else: #S'il y a plus qu'un elements, on fait la compe de la liste et on la rajoute
                            result4.append(copy.deepcopy(temp2))

                    #S'il n'y a qu'une serie, on n'envoie pas une liste de serie
                    if ajout is True: #if "+="
                        if nom in newConfigData:    #Si le même paramètre revient plusieurs fois, on l'ajoute au données précédentes
                            newConfigData[nom] = newConfigData[nom] + copy.deepcopy(result4)
                        else:
                            newConfigData[nom] = copy.deepcopy(result4)
                    else: #if "=" on ne s'occupe pas si la valeur existe deja, et si valeur simple, on ne laisse pas dans une liste
                        if len(result4) == 1:
                            newConfigData[nom] = copy.deepcopy(result4[0])
                        else:
                            newConfigData[nom] = copy.deepcopy(result4)
                except:
                    pass

        if self.debug > 1:
            print "PyComView:loadConfigFromFile : values loaded : "
            for key, val in newConfigData.iteritems():
                print "\t{0}: {1}".format(key, val)

        #On met a jour le dictionnaire des valeurs par defaut de la classe, et on applique ces valeurs
        self.updateParametersWithDefaultDictionary(newConfigData)
                
        


    def updateParametersWithDefaultDictionary(self, dictionary = None):
        """ Set tous les parametres en utilisant le dictionaire "self.configData"
            si "Dictionary est à None.
            Ne reconnecte pas de nouveau même si l'IP est changé. Il faut deconnecter et conncter dans ce cas.
        """

        if dictionary is None:
            dictionary = self.configData
        else:
            self.updateConfigData(dictionary)

        #for key,val in d.iteritems():
        #    exec(key + '=val')
        
        #Update debug
        if "debug" in dictionary:
            try:
                result = self.ComViewDLL.Call_SetDebug(self.iCOMiViewObject, c.c_short(self.debug))
                if result == -1:
                    print 'PyComView::updateParametersWithDefaultDictionary : The C Function "Call_SetDebug" returns an error.'                
            except:
                print "PyComView::updateParametersWithDefaultDictionary : Incapable de modifier la valeur debug ({0}) ...".format(self.debug)

        if "timestamp" in dictionary:
            try:
                result = self.ComViewDLL.Call_SetTimeStampType(self.iCOMiViewObject, c.c_short(dictionary["timestamp"]))
                if result == -1:
                    print 'PyComView::updateParametersWithDefaultDictionary : The C Function "Call_SetTimeStampType" returns an error.'                
            except:
                print "PyComView::updateParametersWithDefaultDictionary : Incapable de modifier la valeur timestamp ({0}) ...".format(dictionary["timestamp"])


        #Om met a jour les parametre de sauvegarde et d'acquisition
        self.iCOMSetSavingParameter()    
        self.iCOMSetAcquisitionParameter()

        #On remplace la liste du Summary de iCOM
        if "iCOMSetSummaryTagList" in dictionary:
            #On efface la liste
            self.iCOMClearTagList()
            #on rajoute les nouveau Tags
            try:
                if isinstance((dictionary["iCOMSetSummaryTagList"])[0], list):    #S'il y a une liste de Tags
                    for aTag in dictionary["iCOMSetSummaryTagList"]:
                        self.iCOMAddTagToList(aTag[0], aTag[1])
                else: #S'il n'y a qu'un seul Tag
                    aTag = dictionary["iCOMSetSummaryTagList"]
                    self.iCOMAddTagToList(aTag[0], aTag[1])
            except: pass

        #On remplace les listes de trigger
        if "iCOMSetStartTriggerList" in dictionary:
            #On efface la liste
            self.iCOMClearTriggerLists(True, False, False)
            #On met les nouveaux trigger
            try:
                if isinstance((dictionary["iCOMSetStartTriggerList"])[0], list):    #S'il y a une liste de Triggers
                    for trig in dictionary["iCOMSetStartTriggerList"]:
                        if len(trig) >= 5:
                            self.iCOMAddStartTriggerToList(trig[0], trig[1], trig[2], trig[3], trig[4])
                        elif len(trig) == 4:
                            self.iCOMAddStartTriggerToList(trig[0], trig[1], trig[2], trig[3])
                        else:
                            self.iCOMAddStartTriggerToList(trig[0], trig[1], None, None)
                else:  #S'il n'y a qu'un seul trigger
                    trig = dictionary["iCOMSetStartTriggerList"]
                    if len(trig) >= 5:
                        self.iCOMAddStartTriggerToList(trig[0], trig[1], trig[2], trig[3], trig[4])
                    elif len(trig) == 4:
                        self.iCOMAddStartTriggerToList(trig[0], trig[1], trig[2], trig[3])
                    else:
                        self.iCOMAddStartTriggerToList(trig[0], trig[1], None, None)
            except: pass

        if "iCOMSetPauseTriggerList" in dictionary:
            #On efface la liste
            self.iCOMClearTriggerLists(False, True, False)
            #On met les nouveaux trigger
            try:
                if isinstance((dictionary["iCOMSetPauseTriggerList"])[0], list):    #S'il y a une liste de Triggers
                    for trig in dictionary["iCOMSetPauseTriggerList"]:
                        if len(trig) >= 5:
                            self.iCOMAddPauseTriggerToList(trig[0], trig[1], trig[2], trig[3], trig[4])
                        elif len(trig) == 4:
                            self.iCOMAddPauseTriggerToList(trig[0], trig[1], trig[2], trig[3])
                        else:
                            self.iCOMAddPauseTriggerToList(trig[0], trig[1], None, None)
                else:  #S'il n'y a qu'un seul trigger
                    trig = dictionary["iCOMSetPauseTriggerList"]
                    if len(trig) >= 5:
                        self.iCOMAddPauseTriggerToList(trig[0], trig[1], trig[2], trig[3], trig[4])
                    elif len(trig) == 4:
                        self.iCOMAddPauseTriggerToList(trig[0], trig[1], trig[2], trig[3])
                    else:
                        self.iCOMAddPauseTriggerToList(trig[0], trig[1], None, None)
            except: pass

        if "iCOMSetStartTriggerList" in dictionary:
            #On efface la liste
            self.iCOMClearTriggerLists(False, False, True)
            #On met les nouveaux trigger
            try:
                if isinstance((dictionary["iCOMSetStopTriggerList"])[0], list):    #S'il y a une liste de Triggers
                    for trig in dictionary["iCOMSetStopTriggerList"]:
                        if len(trig) >= 5:
                            self.iCOMAddStopTriggerToList(trig[0], trig[1], trig[2], trig[3], trig[4])
                        elif len(trig) == 4:
                            self.iCOMAddStopTriggerToList(trig[0], trig[1], trig[2], trig[3])
                        else:
                            self.iCOMAddStopTriggerToList(trig[0], trig[1], None, None)
                else:  #S'il n'y a qu'un seul trigger
                    trig = dictionary["iCOMSetStopTriggerList"]
                    if len(trig) >= 5:
                        self.iCOMAddStopTriggerToList(trig[0], trig[1], trig[2], trig[3], trig[4])
                    elif len(trig) == 4:
                        self.iCOMAddStopTriggerToList(trig[0], trig[1], trig[2], trig[3])
                    else:
                        self.iCOMAddStopTriggerToList(trig[0], trig[1], None, None)
            except: pass
                                                

    def updateConfigData(self, dictionary):
        """ Update le dictionnaire "self.configData" avec de nouvelles valeurs.
        """

        try:
            for key, value in dictionary.iteritems():    #.items() pour Python 3
                self.configData[key] = value
        except:
            print "Error in PyComView::updateConfigData : Dictionnaire pas mis-a-jour."

        if "debug" in dictionary:
            try:
                self.debug = dictionary["debug"]
            except:
                print "Error in PyComView::updateConfigData : Debug pas mis à jour !?!"
                

    def boolStr(self,aString):
        """ convertis les caractères "0" and "1" en booleen. """

        if (aString.lower()) == "true":
            return True
        elif (aString.lower()) == "false":
            return False
        
        try: return bool(int(aString))
        except:
            print "Error dans PyComView::boolStr : Apparemment pas le bon type."
            return None


    def longHexa(self,aString):
        """ convertis un string en type "long" hexadecimal."""

        try:
            return long(aString,base=16)
        except:
            print "Error dans PyComView::longHexa : Apparemment pas le bon type."
            return None


    def NoneValue(self,unusedParam = None):
        """ returns None value """
        return None


    #########################################################################
    #Fonctions iView
    #########################################################################
    def iViewInit(self):
        """ """
        if self.configData["use_iView"]:
            result = self.ComViewDLL.Call_Init_iView(self.iCOMiViewObject)
            if result == -1:
                print 'PyComView::iViewInit : The C Function "Call_Init_iView" returns an error.'
        else:
            result = 0
        return result


    def iViewClose(self):
        """ """
        result = self.ComViewDLL.Call_Close_iView(self.iCOMiViewObject)
        if result == -1:
            print 'PyComView::iViewClose : The C Function "Call_Close_iView" returns an error.'
        elif result == 0:
            print "PyComView::iViewClose : iView pas connecte ou initialise de toute facon..."

            
    def iViewStartAcquireContinuous(self, StartOnPause = None):
        """ Démarre l'Acquisition iView. On laisse le paramètre à None si on veut
            que la situation de démarrage soit gérée par le paramètre
        """

        if self.configData["use_iView"]:
            if(self.configData["use_iCOM"]==False): # si iCOM n'est pas usilisé, les triggers ne seront pas actifs
                StartOnPause = False
            elif(StartOnPause == None):
                StartOnPause = self.configData["iCOM_use_start_acquisition_trigger"]

            result = self.ComViewDLL.Call_iView_StartAcquireContinuous(self.iCOMiViewObject, StartOnPause)
            if result == -1:
                print 'PyComView::iViewStartAcquireContinuous : The C Function "Call_iView_StartAcquireContinuous" returns an error.'
            elif result == 0:
                print "PyComView::iViewStartAcquireContinuous : iView pas connecte ou initialise."
        else:
            result = 0

        return result
            

    def iViewPauseImageSavingWithoutStopingAcquisition(self):
        """ """
        if self.configData["use_iView"]:
            result = self.ComViewDLL.Call_iView_PauseImageSavingWithoutStopingAcquisition(self.iCOMiViewObject)
            if result == -1:
                print 'PyComView::iViewPauseImageSavingWithoutStopingAcquisition : The C Function "Call_iView_PauseImageSavingWithoutStopingAcquisition" returns an error.'                
            elif result == 0:
                print "PyComView::iViewPauseImageSavingWithoutStopingAcquisition : iView pas connecte ou initialise."
        else:
            result = 0

        return result

 
    def iViewResumeSavingImageSaving(self):
        """ """
        if self.configData["use_iView"]:
            result = self.ComViewDLL.Call_iView_ResumeSavingImageSaving(self.iCOMiViewObject)
            if result == -1:
                print 'PyComView::iViewResumeSavingImageSaving : The C Function "Call_iView_ResumeSavingImageSaving" returns an error.'                
            elif result == 0:
                print "PyComView::iViewResumeSavingImageSaving : iView pas connecte ou initialise."
        else:
            result = 0

        return result

 
    def iViewStopAcquireContinuous(self):
        """ """
        if self.configData["use_iView"]:
            result = self.ComViewDLL.Call_iView_StopAcquireContinuous(self.iCOMiViewObject)
            if result == -1:
                print 'PyComView::iViewStopAcquireContinuous : The C Function "Call_iView_StopAcquireContinuous" returns an error.'
            elif result == 0:
                print "PyComView::iViewStopAcquireContinuous : iView pas connecte ou initialise."
        else:
            result = 0

        return result


    def iViewSetSavingParameter(self, filenames = "", filepath = "result\\"):
        """ Ne pas utiliser cette fonction dans le cadre de l'utilsation avec iCOM. Ce dernier gère
            les sauvegardes avec les parametres de config dans le dictionnaire.
        """
        if self.configData["use_iView"]:
            result = self.ComViewDLL.Call_iView_SetSavingParameter(self.iCOMiViewObject, c.c_char_p(filenames), c.c_char_p(filepath))
            if result == -1:
                print 'PyComView::iViewSetSavingParameter : The C Function "Call_iView_SetSavingParameter" returns an error.'
            elif result == 0:
                print "PyComView::iViewSetSavingParameter : iView pas connecte ou initialise."
        else:
            result = 0

        return result


    def delete(self):
        """ """
        if self.debug > 0:
            print "PyComView::delete : Deleting iCOMiViewObject."
        self.ComViewDLL.Delete_iCOMListen(self.iCOMiViewObject)



if __name__ == "__main__":

    
    #debug_file = open("C:\\temp\\debug.txt","w")
    debug_file = open(os.getcwd() + "\\debugPyComView.txt","w",0)
    #debug_file = os.fdopen(sys.stdout.fileno(), 'w', 0)
    config_file = "config.txt"
    old_stdout = sys.stdout     #Keeping old sys.stdout for later if needed
    sys.stdout = debug_file


    #Initialisation des valeurs par défaults
    debug = 2


    #Nous faisons un dictionnaire avec toutes les configurations dans le fichier config.txt
    test = PyComView(debug)
    print "init fini"

    test.loadConfigFromFile(config_file)
    print "load of {0} fini".format(config_file)

    #test.iComConnect("10.226.144.152", "stringMarche", "result\\") #Infinity3, mais de L'extérieur
    test.iComConnect() #à partir du iView
    print "connect fini"




    print "Connecting iView"
    iViewConnected = test.iViewInit()
        
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


        

    print "save finish"

    if iViewConnected is 1:
        test.iViewStopAcquireContinuous()
        print "iView Acquisition stopped"
        test.iViewClose()
        print "iView Disconnected"
        #sys.stdout.flush()
    test.iComDisconnect()

    print "iCOM disconnected"
    #"""
    test.delete()

    print "pointer deleted"

    debug_file.close()

    sys.stdout = old_stdout

    print "quitting software"








