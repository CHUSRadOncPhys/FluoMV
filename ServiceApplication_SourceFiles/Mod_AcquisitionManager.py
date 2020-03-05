import os,os.path
import sys
import time
from datetime import datetime
#===============================================================================================================
class AcquisitionManager:
	
	def __init__(self,settingsObj):
		
		self.InitDT = datetime.now() #Only file create after this time are valid.
		self.State = None # 2 mode: None, "Acquisition". Used in ServiceApplication.py/StartSagMonitoring()
		
		self.SettingsObj = settingsObj #Settings.Settings()
		
		self.ActiveCalibrationDTList = list() #List of tuple (EnergyName,DateTime)
		self.ActiveCalibrationList = list() #List of Energy namae
		self.FlexmapDT = None #Date time of the flexmap
		
		self.MeasurementFolderPath = None		
		self.ImageFilePathListBefore = list()
		self.ImageFilePathListAfter = list()
		self.NewImageFilePathList = list()
		self.NewImageTSList = list() #List of timestamp for the new images 

		self.BackgroundFilePathList = list() #FilePath list
		
		#Flexmap
		self.GantryList = list()
		self.YIsoList = list()
		self.XIsoList = list()

		#****functions *****
		self.ClearLogs()
		self.GetActiveCalibrations()
		if self.FlexmapDT is not None:
			self.GetFlexmapData()

#--------------------------------------------------------------------------------------------------------------------------------------------------------------
	def ClearLogs(self):
		try:
			os.remove(os.path.join(self.SettingsObj.ROOTPATH,"Logs","Mod_AcquisitionManager.log"))
		except:
			pass
#---------------------------------------------------------------------------------------------------------------------------------------------------------------
	def MyLog(self,mess="none",value="none",level=0):
		if level<=self.SettingsObj.debugLvl:
			f = open(os.path.join(self.SettingsObj.ROOTPATH,"Logs","Mod_AcquisitionManager.log"),"a")
			f.write(str(mess)+"\t"+str(value)+"\t"+str(datetime.now())+"\n")
			f.close()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------
	def GetActiveCalibrations(self):
		self.ActiveCalibrationDTList = list() #List of tuple (EnergyName,DateTime)
		self.ActiveCalibrationList = list() #List of Energy namae
		self.FlexmapDT = None #Date time of the flexmap

		#Check if flexmap exist
		if os.path.isfile(os.path.join(self.SettingsObj.ROOTPATH,"CalibrationFiles","Panel.flexmap")):
			thisTime = os.path.getmtime(os.path.join(self.SettingsObj.ROOTPATH,"CalibrationFiles","Panel.flexmap"))
			thisTime = time.localtime(thisTime)
			self.FlexmapDT = time.strftime("%Y-%m-%d  %H:%M:%S",thisTime)

		AllFiles = os.listdir(os.path.join(self.SettingsObj.ROOTPATH,"CalibrationFiles"))
		for f in AllFiles:
			if os.path.isfile(os.path.join(self.SettingsObj.ROOTPATH,"CalibrationFiles",f,"Files.Calib")):
				thisTime = os.path.getmtime(os.path.join(self.SettingsObj.ROOTPATH,"CalibrationFiles",f,"Files.Calib"))
				thisTime = time.localtime(thisTime)
				thisDT = time.strftime("%Y-%m-%d  %H:%M:%S",thisTime)
				self.ActiveCalibrationDTList.append((f,thisDT)) #tuple
				self.ActiveCalibrationList.append(f)
#----------------------------------------------------------------------------------------------------------------------------------------------------------------
	def GetFlexmapData(self,thisFilePath = None): #For displaying in the figure
		self.GantryList = list()
		self.YIsoList = list()
		self.XIsoList = list()
		
		if thisFilePath == None:
			thisFilePath = os.path.join(self.SettingsObj.ROOTPATH,"CalibrationFiles","Panel.flexmap")
		
		f = open(thisFilePath)
		Contenu = f.read()
		f.close()
		Lines = Contenu.split("\n")
		Lines = filter(None,Lines)
		for k in range(1,len(Lines)):
			els = Lines[k].split(";")
			els = filter(None,els)
			self.GantryList.append(float(els[0]))
			self.XIsoList.append(float(els[1])) #BBX dans le referentiel PyComView
			self.YIsoList.append(float(els[2])) #BBY dans le referentiel  PyComView

#----------------------------------------------------------------------------------------------------------------------------------------------------------------
	def FindMostRecentMeasurementFolder(self): #Find the Most recent folder since the Service software was started
		self.MeasurementFolderPath = None
		LastDT = self.InitDT 
		
		PatientIDList = os.listdir(os.path.join(self.SettingsObj.ROOTPATH,"EPID_Listening"))
		for id in PatientIDList:
			thisPath = os.path.join(self.SettingsObj.ROOTPATH,"EPID_Listening",id)
			if os.path.isdir(thisPath)==True:
				MeasureList = os.listdir(thisPath)
				#print "MeasureList",MeasureList
				for m in MeasureList:
					thisPath2 = os.path.join(thisPath,m)
					#print thisPath2
					if os.path.isdir(thisPath2):
						folderelement = m.split("_")
						dateelement = folderelement[0].split("-")
						timeelement = folderelement[1].split("-")
						thisDateTime = datetime(int(dateelement[0]),int(dateelement[1]),int(dateelement[2]),int(timeelement[0]),int(timeelement[1]),int(timeelement[2]))
						#print "thisDateTime:",thisDateTime
						if thisDateTime>LastDT: #If the Measurement folder was created after launching the apps
							self.MeasurementFolderPath = thisPath2
							LastDT = thisDateTime
							#print "LastDT",LastDT

		self.MyLog("self.FindMostRecentMeasurementFolder:",self.MeasurementFolderPath,level=0)
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	def ResetLists(self): #Reset lists: self.ImageFilePathListBefore, self.ImageFilePathListAfter, self.NewImageFilePathList, self.NewImageTSList
		self.ImageFilePathListBefore = list()
		self.ImageFilePathListAfter = list()
		self.NewImageFilePathList = list()
		self.NewImageTSList = list()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	def FindNewImages(self,TimeStampListAfter,NbMin=1): #Fill  self.NewImageFilePathList , self.NewImageTSList
		self.NewImageFilePathList = list()
		self.NewImageTSList = list()
		
		#Add the new images to the list
		idx=0
		for f in self.ImageFilePathListAfter:
			if f not in self.ImageFilePathListBefore:
				self.NewImageFilePathList.append(f)
				self.NewImageTSList.append(TimeStampListAfter[idx])
			idx = idx + 1

		if len(self.NewImageFilePathList)>=NbMin:
			for k in self.NewImageFilePathList:
				self.MyLog("FindNewImages:",k,level=2)			
			self.MyLog("FindNewImages: len(self.NewImageFilePathList)",str(len(self.NewImageFilePathList)),level=1)
			return True
			
		else:
			self.MyLog("FindNewImages","return False",level=0)
			return False
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	def DefineBackgroundFiles(self): #Fill  self.BackgroundFilePathList
		self.BackgroundFilePathList = list() #reset the list
		for k in range(len(self.NewImageFilePathList)):			
			self.BackgroundFilePathList.append(os.path.join(self.MeasurementFolderPath,"image",self.NewImageFilePathList[k]))
			self.MyLog("DefineBackgroundFiles",os.path.join(self.MeasurementFolderPath,"image",self.NewImageFilePathList[k]),level=2)
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
