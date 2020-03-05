import os, os.path
import sys
import numpy as np
from datetime import datetime
#========================================================================================================
class IcomManager:
	
	def __init__( self,thisFolderPath,thisSettingsObj):

		self.FilePath = os.path.join(thisFolderPath,'iCOM','acq_detail.txt')
		self.SettingsObj = thisSettingsObj

		self.TimeStampList = list()
		self.GantryAngleList = list() #float
		self.EnergyList = list()
		self.DoseRateList = list() #float
		self.BeamNameList = list()
		self.SegIDList = list()

		self.BeamNameSet = list()
		self.SegIDSet = list()
		self.BeamNameSegIDSet = list()

		self.LastLine = 0
		self.LastIndex =0
		self.TimeStampMin = 0
		self.TimeStampMax = 0
		
		#***Functions***
		self.ClearLogs()
		self.MyLog("Init:",self.FilePath)
#--------------------------------------------------------------------------------------------------------------------------------------------
	def ClearLogs(self):
		try:
			os.remove(os.path.join(self.SettingsObj.ROOTPATH,"Logs","Mod_IcomManager.log"))
		except:
			pass
#--------------------------------------------------------------------------------------------------------------------------------------------
	def MyLog(self,mess="none",value="none",level=0):
		if level<=self.SettingsObj.debugLvl:
			f = open(os.path.join(self.SettingsObj.ROOTPATH,"Logs","Mod_IcomManager.log"),"a")
			f.write(str(mess)+"\t"+str(value)+"\t"+str(datetime.now())+"\n")
			f.close()
#--------------------------------------------------------------------------------------------------------------------------------------------
	def GetSegmentTimeLimits(self,thisBeamName,thisSegID): #return minTime,MaxTime,np.median(thisDRList),thisEnergy
		thisEnergy = None
		thisDRList = list() #Dose rate list
		thisTimeStampList = list()
		for k in range(len(self.TimeStampList)):

			if self.BeamNameList[k]==thisBeamName and self.SegIDList[k]==thisSegID and self.DoseRateList[k]>0:
				thisTimeStampList.append(self.TimeStampList[k])
				thisDRList.append(self.DoseRateList[k])
				thisEnergy = self.EnergyList[k]
				
		if len(thisTimeStampList)>5:
			self.MyLog("GetSegmentTimeLimits: MinTime",str(np.min(thisTimeStampList)),level=2)
			self.MyLog("GetSegmentTimeLimits: MaxTime",str(np.max(thisTimeStampList)),level=2)
			return True, np.min(thisTimeStampList), np.max(thisTimeStampList),np.median(thisDRList),thisEnergy
		else:
			self.MyLog("GetSegmentTimeLimits","FAILS",level=0)
			return False, None, None,None,None

#--------------------------------------------------------------------------------------------------------------------------------------------
	def GetFrameInfo(self,thisTimeStamp):
		self.MyLog("GetFrameInfo: thisTimeStamp",str(thisTimeStamp),level=2)
		A = np.asarray(self.TimeStampList)
		B = np.abs(A-thisTimeStamp)
		IndexFound = np.argmin(B)
		
		self.MyLog("GetFrameInfo, MinDiffTime found",str(B[IndexFound]),level=2)
		if B[IndexFound]<=10000000 and self.EnergyList[IndexFound]!=None and self.DoseRateList[IndexFound]!=None:
			self.MyLog("GetFrameInfo:Gantry",str(self.GantryAngleList[IndexFound]),level=2)
			self.MyLog("GetFrameInfo:DoseRateList",str(self.DoseRateList[IndexFound]),level=2)
			self.MyLog("GetFrameInfo:EnergyList",str(self.EnergyList[IndexFound]),level=2)
			self.MyLog("GetFrameInfo:IndexFound",str(IndexFound),level=2)
			return True, IndexFound
		else:
			self.MyLog("GetFrameInfo:","return False",level=0)
			return False, None
#-----------------------------------------------------------------------------------------------------------------------------
	def FetchInfo(self,StartTime,StopTime): #Fill iCom info lists between StartTime and StopTime
		self.MyLog("Fetch",self.FilePath,level=1)
		if os.path.isfile(self.FilePath):
			
			f = open(self.FilePath)
			Contenu = f.read()
			f.close()
			Lines = Contenu.split("\n")
			Lines = filter(None,Lines)
			
			if len(Lines)>30:
				
				#We neglect the last message because we don't know if the message is completed
				LastValidLine = None
				for k in range(-1,-15,-1):
					if  Lines[k].find("Date")!=-1:
						LastValidLine = len(Lines) + k -1
						break
				self.MyLog( "Update:LastValidLine",str(LastValidLine),level=2)
				
				
				for k in range(0,LastValidLine):
					
					if Lines[k].find("Date")!=-1:
						info = Lines[k-1].split(",")
						info = filter(None,info)

						if int(info[1])>=StartTime and int(info[1])<=StopTime:

							self.TimeStampList.append(int(info[1]))
							
							jmax = 0
							for j in range(1,10):
								if (k+j)<LastValidLine and Lines[k+j].find("Date")!=-1:
									jmax = j-1
							self.MyLog("LastIncludedLine",Lines[k+jmax-1],level=2)
							
							for j in range(2,jmax):

								if Lines[k+j].find(":0x50010007")!=-1:
									info = Lines[k+j].split(",")
									info = filter(None,info)
									self.GantryAngleList.append(float(info[2]))

								if Lines[k+j].find(":0x50010006")!=-1:
									info = Lines[k+j].split(",")
									info = filter(None,info)
									self.DoseRateList.append(float(info[2]))

								if Lines[k+j].find(":0x50010003")!=-1:
									info = Lines[k+j].split(",")
									info = filter(None,info)
									self.EnergyList.append(info[2].replace(' ',''))

								if Lines[k+j].find(":0x70010007")!=-1:
									info = Lines[k+j].split(",")
									info = filter(None,info)
									self.BeamNameList.append(info[2].replace(' ',''))

								if Lines[k+j].find(":0x70010008")!=-1:
									info = Lines[k+j].split(",")
									info = filter(None,info)
									self.SegIDList.append(info[2].replace(' ',''))
							
							if  len(self.TimeStampList)!=len(self.BeamNameList):
								if len(self.BeamNameList)==0:
									self.BeamNameList.append(None)
								else:
									self.BeamNameList.append(self.BeamNameList[-1])

							if len(self.TimeStampList)!=len(self.SegIDList):
								self.SegIDList.append(None)
							
							if self.BeamNameList[-1]!=None and self.SegIDList[-1]!=None:
								self.BeamNameSegIDSet.append((self.BeamNameList[-1],self.SegIDList[-1]))

							if len(self.TimeStampList)!=len(self.GantryAngleList):
								self.GantryAngleList.append(None)
								
							if len(self.TimeStampList)!=len(self.DoseRateList):
								self.DoseRateList.append(None)
							
							if len(self.TimeStampList)!=len(self.EnergyList):
								self.EnergyList.append(None)

				self.TimeStampMin = np.min(self.TimeStampList)
				self.TimeStampMax = np.max(self.TimeStampList)
			
			self.BeamNameSet = list(set(self.BeamNameList))
			self.SegIDSet = list(set(self.SegIDList))
			self.BeamNameSegIDSet = list(set(self.BeamNameSegIDSet))

			for tag in self.BeamNameSegIDSet:
				self.MyLog("BeamNameSegID found",tag,level=1)

#-----------------------------------------------------------------------------------------------------------------------------
	def Update(self):
		self.MyLog("Update",self.FilePath,level=1)
		if os.path.isfile(self.FilePath):
			
			f = open(self.FilePath)
			Contenu = f.read()
			f.close()
			Lines = Contenu.split("\n")
			Lines = filter(None,Lines)
			
			if len(Lines)>30:
				
				#We neglect the last message because we don't know if the message is completed
				LastValidLine = None
				for k in range(-1,-15,-1):
					if  Lines[k].find("Date")!=-1:
						LastValidLine = len(Lines) + k -1
						break
				self.MyLog( "Update:LastValidLine",str(LastValidLine))
				
				
				for k in range(self.LastLine,LastValidLine):
					
					if Lines[k].find("Date")!=-1:
						info = Lines[k-1].split(",")
						info = filter(None,info)
						self.TimeStampList.append(int(info[1]))
						self.LastLine = k +1
						self.MyLog("Update:self.LastLine",str(self.LastLine))
						
						
						jmax = 0
						for j in range(1,10):
							if (k+j)<LastValidLine and Lines[k+j].find("Date")!=-1:
								jmax = j-1
						self.MyLog("Update:k+jmax-1",str(k+jmax-1))
						self.MyLog("LastIncludedLine",Lines[k+jmax-1])
						
						for j in range(2,jmax):
							#~ if Lines[k+j].find("Date")!=-1:
								#~ break
							if Lines[k+j].find(":0x50010007")!=-1:
								info = Lines[k+j].split(",")
								info = filter(None,info)
								self.GantryAngleList.append(float(info[2]))

							if Lines[k+j].find(":0x50010006")!=-1:
								info = Lines[k+j].split(",")
								info = filter(None,info)
								self.DoseRateList.append(float(info[2]))

							if Lines[k+j].find(":0x50010003")!=-1:
								info = Lines[k+j].split(",")
								info = filter(None,info)
								self.EnergyList.append(info[2].replace(' ',''))

							if Lines[k+j].find(":0x70010007")!=-1:
								info = Lines[k+j].split(",")
								info = filter(None,info)
								self.BeamNameList.append(info[2].replace(' ',''))

							if Lines[k+j].find(":0x70010008")!=-1:
								info = Lines[k+j].split(",")
								info = filter(None,info)
								self.SegIDList.append(info[2].replace(' ',''))
						
						if  len(self.TimeStampList)!=len(self.BeamNameList):
							if len(self.BeamNameList)==0:
								self.BeamNameList.append(None)
							else:
								self.BeamNameList.append(self.BeamNameList[-1])

						if len(self.TimeStampList)!=len(self.SegIDList):
							self.SegIDList.append(None)
						
						if self.BeamNameList[-1]!=None and self.SegIDList[-1]!=None:
							self.BeamNameSegIDSet.append((self.BeamNameList[-1],self.SegIDList[-1]))

						if len(self.TimeStampList)!=len(self.GantryAngleList):
							self.GantryAngleList.append(None)
							
						if len(self.TimeStampList)!=len(self.DoseRateList):
							self.DoseRateList.append(None)
						
						if len(self.TimeStampList)!=len(self.EnergyList):
							self.EnergyList.append(None)
							
				self.TimeStampMin = np.min(self.TimeStampList)
				self.TimeStampMax = np.max(self.TimeStampList)
			
			self.BeamNameSet = list(set(self.BeamNameList))
			self.SegIDSet = list(set(self.SegIDList))
			self.BeamNameSegIDSet = list(set(self.BeamNameSegIDSet))
