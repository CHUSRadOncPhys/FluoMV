import sys
import os, os.path
from datetime import datetime
#========================================================================================================
class ViewManager:
	
	def __init__( self,thisFolderPath,thisSettingsObj):

		self.FolderPath = thisFolderPath
		self.FilePath = os.path.join(thisFolderPath,'image','acq_im_detail.txt')
		self.SettingsObj = thisSettingsObj

		self.FrameFilePathList = list()
		self.TimeStampList = list()
		
		#***Functions***
		#~ self.ClearLogs()
		self.GetAcquisitionList()
#--------------------------------------------------------------------------------------------------------------------------------------------
	def ClearLogs(self):
		try:
			os.remove(os.path.join(self.SettingsObj.ROOTPATH,"Logs","Mod_ViewManager.log"))
		except:
			pass
#--------------------------------------------------------------------------------------------------------------------------------------------
	def MyLog(self,mess="none",value="none",level=0):
		if level<self.SettingsObj.debugLvl:
			f = open(os.path.join(self.SettingsObj.ROOTPATH,'Logs',"Mod_ViewManager.log"),"a")
			f.write(str(mess)+"\t"+str(value)+"\t"+str(datetime.now())+"\n")
			f.close()
#--------------------------------------------------------------------------------------------------------------------------------------------
	def GetAcquisitionList(self): #Fill self.FrameFilePathList, self.TimeStampList
		if os.path.isfile(self.FilePath):
			
			f = open(self.FilePath)
			Contenu = f.read()
			f.close()
			Lines = Contenu.split("\n")
			Lines = filter(None,Lines)
			
			for k in range(0,len(Lines)):
				els = Lines[k].split(",")
				els = filter(None,els)
				self.FrameFilePathList.append(os.path.join(self.FolderPath,'image','acq'+els[0]+'.bin'))
				self.TimeStampList.append(int(els[1]))

#--------------------------------------------------------------------------------------------------------------------------------------------
	def GetFrameFilePathList(self,LimitMin,LimitMax):
		thisList = list()
		for k in range(len(self.TimeStampList)):
			if self.TimeStampList[k]>=LimitMin and self.TimeStampList[k]<=LimitMax:
				thisList.append(self.FrameFilePathList[k])
		return thisList
