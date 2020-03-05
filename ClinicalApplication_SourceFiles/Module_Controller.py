import os, os.path
import sys
import time
import subprocess
import threading
from datetime import datetime
import numpy as np

import Module_Monitor
import Mod_LiveCalibration
#============================================================================================================================================================
class Controller():
	
	def __init__(self,settingsObj):

		self.InitDT = datetime.now()
		
		self.State = "StopAcquisition"  #"Acquisition" or "StopAcquisition"

		self.MeasurementFolderPath = "none"

		self.PatientID = "none"

		self.GantryForTimeOffsetDict = {}
		self.TimeOffsetDict = {}
		self.GantryAngleByROIDict = {}


		self.SettingsObj = settingsObj #Settings.Settings()
		self.DebugLvl = self.SettingsObj.debugLvl
		self.CalibObj = Mod_LiveCalibration.Calibration(self.SettingsObj)

		#self.ROOTPATH = os.path.join(self.SettingsObj.ROOTPATH,"EPID_Fluoroscopie")
		#self.PyCOMView_OUTPATH =  os.path.join(self.SettingsObj.ROOTPATH,"EPID_Listening")

		#****Functions****
		self.ClearLogs()		
#--------------------------------------------------------------------------------------------------------------------------------------------
	def ClearLogs(self):
		try:
			os.remove(os.path.join(self.SettingsObj.ROOTPATH,"Logs","Controller.log"))
		except:
			pass
#--------------------------------------------------------------------------------------------------------------------------------------------
	def MyLog(self,mess="none",value="none",level=0):
		if level<=self.SettingsObj.debugLvl:
			f = open(os.path.join(self.SettingsObj.ROOTPATH,"Logs","Controller.log"),"a")
			f.write(str(mess)+"\t"+str(value)+"\t"+str(datetime.now())+"\n")
			f.close()
#---------------------------------------------------------------------------------------------------------------------------------------------------
	def FindMostRecentMeasurementFolder(self):
		self.MeasurementFolderPath = "none"
		LastDT = self.InitDT #Most recent folder since the class was instantiated
		
		thisROOT = os.path.join(self.SettingsObj.ROOTPATH,"EPID_Listening",self.PatientID)
		AllFolder = os.listdir(thisROOT)
		for foldername in AllFolder:
			if os.path.isdir(os.path.join(thisROOT,foldername)) == True :
				folderelement = foldername.split("_")
				dateelement = folderelement[0].split("-")
				timeelement = folderelement[1].split("-")
				thisDateTime = datetime(int(dateelement[0]),int(dateelement[1]),int(dateelement[2]),int(timeelement[0]),int(timeelement[1]),int(timeelement[2]))
				
				if thisDateTime>LastDT:
					self.MeasurementFolderPath = os.path.join(thisROOT,foldername)
					LastDT = thisDateTime
		
		self.MyLog("FindMostRecentMeasurementFolder",self.MeasurementFolderPath)

#---------------------------------------------------------------------------------------------------------------------------------------------------------
	def CheckLastCreationTime(self):
		#~ if os.path.isfile(os.path.join(self.MeasurementFolderPath,"image","acq_im_detail.txt")):
			#~ self.MyLog("CheckLastCreationTime","File exist")
		#~ else:
			#~ self.MyLog("CheckLastCreationTime","File doesn't exist")
		try:
			g = open(os.path.join(self.MeasurementFolderPath,"image","acq_im_detail.txt"),"r")
			Lines = g.readlines()
			g.close()
			Lines = filter(None,Lines)
			line = Lines[-1]
			info = line.split(",")
			
			thisImFilePath = os.path.join(self.MeasurementFolderPath ,"image","acq"+str(info[0])+".bin")
			self.MyLog("CheckLastCreationTime",thisImFilePath)

			if abs(time.time()-os.path.getctime(thisImFilePath))<2:
				self.MyLog("CheckLastCreationTime return True:" + thisImFilePath,"DiffTime="+ str(abs(time.time()-os.path.getctime(thisImFilePath))))
				return True
				
			else:
				self.MyLog("CheckLastCreationTime:else",str(abs(time.time()-os.path.getctime(thisImFilePath))))
				return False

		except:
			self.MyLog("CheckLastCreationTime","except")
			return False
#---------------------------------------------------------------------------------------------------------------------------------------------------
	def CallStopAcquisition(self):
		self.State = "StopAcquisition"
		self.MyLog("CallStopAcquisition",self.State)
#---------------------------------------------------------------------------------------------------------------------------------------------------
	def CallStartAcquisition(self):
		
		def ThreadedFunc():
			
			while self.State == "StartAcquisition":
				
				self.FindMostRecentMeasurementFolder() 
				check1 = self.CheckLastCreationTime() #Check 	if abs(time.time()-os.path.getctime(thisImFilePath))<2 seconds
				
				if self.MeasurementFolderPath != "none" and check1==True:
					
					thisMonitor = Module_Monitor.Monitor(self.MeasurementFolderPath,self.SettingsObj)
					
					while self.State == "StartAcquisition" and thisMonitor.Status == True:
						thisMonitor.ResetInfo()
						rtn1 = thisMonitor.GetLastImageInfo() #Get FilePath and timestamp of the last image
						if rtn1 == True:

							thisMonitor.FindCorrespondingICOMInfo()
							NewGAngle = float(thisMonitor.CurrentiCOMGantry)
							if NewGAngle<0:
								NewGAngle = float(thisMonitor.CurrentiCOMGantry) + 360.0
							
							ROIs = self.TimeOffsetDict.keys()
							for k in range(len(ROIs)):
								thisTimeOffset = 4330000-np.interp(NewGAngle,self.GantryForTimeOffsetDict[ROIs[k]],self.TimeOffsetDict[ROIs[k]])
								thisMonitor.FindCorrespondingICOMInfo(int(np.rint(thisTimeOffset)))
								self.GantryAngleByROIDict[ROIs[k]] = thisMonitor.CurrentiCOMGantry

							self.CalibObj.CalibrateFrame(thisMonitor.CurrentImFilePath,thisMonitor.CurrentiCOMEnergy,self.GantryAngleByROIDict)
						time.sleep(0.05)
				time.sleep(0.05)
			
		self.State = "StartAcquisition"
		self.MyLog("CallStartAcquisition",self.State)
		t = threading.Thread(target = ThreadedFunc)
		t.start()
#===========================================================================================================================================================
if __name__ == "__main__":
	Controller()
