import os,os.path
import sys
import time
from datetime import datetime
#========================================================================================

class AcquisitionManager:
	
	def __init__(self,settingsObj):
		self.InitDT = datetime.now()
		self.State = None # 2 mode: None, "Acquisition"
		self.CalibState =False

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
		
		self.GantryList = list()
		self.CrosslineIsoList = list()
		self.InlineIsoList = list()
		#****functions *****
		self.ClearLogs()
		#~ self.GetActiveCalibrations()
		#~ if self.FlexmapDT is not None:
			#~ self.GetFlexmapData()
#--------------------------------------------------------------------------------------------------------------------------------------------
	#~ def GetFlexmapData(self,thisFilePath = None):
		#~ self.GantryList = list()
		#~ self.CrosslineIsoList = list()
		#~ self.InlineIsoList = list()
		
		#~ if thisFilePath == None:
			#~ thisFilePath = os.path.join(self.SettingsObj.ROOTPATH,"CalibrationFiles","Panel.flexmap")
		
		#~ f = open(thisFilePath)
		#~ Contenu = f.read()
		#~ f.close()
		#~ Lines = Contenu.split("\n")
		#~ Lines = filter(None,Lines)
		#~ for k in range(1,len(Lines)):
			#~ els = Lines[k].split(";")
			#~ els = filter(None,els)
			#~ self.GantryList.append(float(els[0]))
			#~ self.InlineIsoList.append(int(els[1]))
			#~ self.CrosslineIsoList.append(int(els[2]))
#--------------------------------------------------------------------------------------------------------------------------------------------
	def ClearLogs(self):
		try:
			os.remove(os.path.join(self.SettingsObj.ROOTPATH,"Logs","Mod_AcquisitionManager.log"))
		except:
			pass
#--------------------------------------------------------------------------------------------------------------------------------------------
	def MyLog(self,mess="none",value="none",level=0):
		if level<=self.SettingsObj.debugLvl:
			f = open(os.path.join(self.SettingsObj.ROOTPATH,"Logs","Mod_AcquisitionManager.log"),"a")
			f.write(str(mess)+"\t"+str(value)+"\t"+str(datetime.now())+"\n")
			f.close()
#--------------------------------------------------------------------------------------------------------------------------------------------
	def ResetLists(self):
		self.ImageFilePathListBefore = list()
		self.ImageFilePathListAfter = list()
		self.NewImageFilePathList = list()
		self.NewImageTSList = list()
#-------------------------------------------------------------------------------------------------------------------------------------------
	def GetList(self):
		thisList = list()
		AllFiles = os.listdir(os.path.join(self.MeasurementFolderPath,"image"))
		for f in AllFiles:
			if f.endswith('.bin'):
				thisList.append(os.path.join(self.MeasurementFolderPath,"image",f))
		return thisList
#--------------------------------------------------------------------------------------------------------------
	#~ def GetActiveCalibrations(self):
		#~ self.ActiveCalibrationDTList = list() #List of tuple (EnergyName,DateTime)
		#~ self.ActiveCalibrationList = list() #List of Energy namae
		#~ self.FlexmapDT = None #Date time of the flexmap

		#~ #Check if flexmap exist
		#~ if os.path.isfile(os.path.join(self.SettingsObj.ROOTPATH,"CalibrationFiles","Panel.flexmap")):
			#~ thisTime = os.path.getmtime(os.path.join(self.SettingsObj.ROOTPATH,"CalibrationFiles","Panel.flexmap"))
			#~ thisTime = time.localtime(thisTime)
			#~ self.FlexmapDT = self.ConvertTime(thisTime)

		#~ AllFiles = os.listdir(os.path.join(self.SettingsObj.ROOTPATH,"CalibrationFiles"))
		#~ for f in AllFiles:
			#~ if os.path.isfile(os.path.join(self.SettingsObj.ROOTPATH,"CalibrationFiles",f,"Files.Calib")):
				#~ thisTime = os.path.getmtime(os.path.join(self.SettingsObj.ROOTPATH,"CalibrationFiles",f,"Files.Calib"))
				#~ thisTime = time.localtime(thisTime)
				#~ thisDT = self.ConvertTime(thisTime)
				#~ self.ActiveCalibrationDTList.append((f,thisDT)) #tuple
				#~ self.ActiveCalibrationList.append(f)
#-------------------------------------------------------------------------------------------------------------------------------------------
	def ConvertTime(self,thisTime):
		this = time.strftime("%Y-%m-%d  %H:%M:%S",thisTime)
		return this
#------------------------------------------------------------------------------------------------------------------------------------------
	def FindNewImages(self,NbMin=1):
		
		#Add the new images to the list
		for f in self.ImageFilePathListAfter:
			if f not in self.ImageFilePathListBefore:
				self.NewImageFilePathList.append(f)
				self.NewImageTSList.append(self.FindFrameTimeStamp(f))


		if len(self.NewImageFilePathList)>=NbMin:
			self.NewImageFilePathList.sort()
			self.NewImageTSList.sort()
			for k in self.NewImageFilePathList:
				self.MyLog("FindNewImages:",k)			
			self.MyLog("FindNewImages: len(self.NewImageFilePathList)",str(len(self.NewImageFilePathList)))
			return True
			
		else:
			self.MyLog("FindNewImages","return False")
			return False
#--------------------------------------------------------------------------------------------------------------------------------------------
	def DefineBackgroundFiles(self):
		self.BackgroundFilePathList = list() #reset the list
		for k in range(len(self.NewImageFilePathList)):			
			self.BackgroundFilePathList.append(os.path.join(self.MeasurementFolderPath,"image",self.NewImageFilePathList[k]))
			self.MyLog("DefineBackgroundFiles",os.path.join(self.MeasurementFolderPath,"image",self.NewImageFilePathList[k]))
		#self.MyLog("DefineBackgroundFiles","Terminated")
#--------------------------------------------------------------------------------------------------------------------------------------------
	def FindFrameTimeStamp(self,thisFilePath):
		thisTS = None #Time stamps
		head,thisFrameName = os.path.split(thisFilePath)
		#print "head",head
		#print "thisFrameName",thisFrameName

		f = open(os.path.join(self.MeasurementFolderPath,"image","acq_im_detail.txt"))
		Contenu = f.read()
		f.close()
		Lines = Contenu.split("\n")
		Lines = filter(None,Lines)
		for line in Lines:
			els = line.split(",")
			els = filter(None,els)
			if els[0]==thisFrameName[3:8]:
				thisTS = els[1]
				

		self.MyLog("FindFrameTimeStamp",thisTS)
		return int(thisTS)

#--------------------------------------------------------------------------------------------------------------------------------------------
	def FindMostRecentMeasurementFolder(self):
		self.MeasurementFolderPath = None
		LastDT = self.InitDT #Most recent folder since the Service software was started
		
		PatientIDList = os.listdir(os.path.join(self.SettingsObj.ROOTPATH,"EPID_Listening"))
		for id in PatientIDList:
			thisPath = os.path.join(self.SettingsObj.ROOTPATH,"EPID_Listening",id)
			if os.path.isdir(thisPath):
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
		
		#~ print "self.MeasurementFolderPath:",self.MeasurementFolderPath
		self.MyLog("self.FindMostRecentMeasurementFolder:",self.MeasurementFolderPath)
#===================================================================================================================
#~ if __name__ == "__main__":
	
	#~ A = GainCalibration()
	#~ if A.MeasurementFolderPath is None:
		#~ print "not foound"
	#~ A.FindMostRecentMeasurementFolder()
	#~ print A.MeasurementFolderPath
	#~ if A.MeasurementFolderPath is None:
		#~ print "not foound"