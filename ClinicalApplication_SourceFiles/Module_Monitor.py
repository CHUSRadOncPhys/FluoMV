import os, os.path
import sys
import shutil
import numpy as np
from datetime import datetime
import time
#============================================================================================================================================================
class Monitor():
	
	def __init__(self,thisListeningFolder,settingsObj):
		self.ClearLogs()
		self.Status = True
		
		self.LastImFilePath  = 'none'
		self.CurrentiCOMGantry = 999
		
		self.ListeningFolderPath = thisListeningFolder
		
		self.SettingsObj = settingsObj #Settings.Settings()

		self.MyLog("Init",self.ListeningFolderPath)

	def ClearLogs(self):
		try:
			os.remove(os.path.join(self.SettingsObj.ROOTPATH,"Logs","Monitor.log"))
		except:
			pass
#--------------------------------------------------------------------------------------------------------------------------------------------
	def MyLog(self,mess="none",value="none",level=0):
		if level<=self.SettingsObj.debugLvl:
			f = open(os.path.join(self.SettingsObj.ROOTPATH,"Logs","Monitor.log"),"a")
			f.write(str(mess)+"\t"+str(value)+"\t"+str(datetime.now())+"\n")
			f.close()
#=======================================================================================================================================================
	def ResetInfo(self):
		self.CurrentImFilePath = "none"
		self.CurrentImTime = "none"
		#~ self.CurrentiCOMGantry = "none"
		self.CurrentiCOMEnergy = "none"
		self.CurrentiCOMDoseRate = "none"
#===========================================================================================================================================================
	def FindCorrespondingICOMInfoHC(self):
		self.CurrentiCOMGantry = "130"
		self.CurrentiCOMEnergy = "6MV"
		self.CurrentiCOMDoseRate = "200"
		self.Status = True
#===========================================================================================================================================================
	def FindCorrespondingICOMInfo(self,TimeOffset = 0):
		TargetTime = self.CurrentImTime - TimeOffset
		self.MyLog("FindCorrespondingICOMInfo","Beginning")
		StartTime = time.time()
		timeout = 0
		localstate = False
		iter = 0
		iter1 = 0
		iter2 = 0 
		while localstate == False and timeout < 2 and self.Status == True:

			try:
				f = open(os.path.join(self.ListeningFolderPath,"iCOM","acq_detail.txt"),"r")
				Contenu = f.read()
				f.close()
				Lines = Contenu.split("\n")
				Lines = filter(None,Lines)

				TimeStampList = list()
				LineStartList = list()
				
				istart = 'none'
				istop = 'none'
				increment = 'none'
				
				if len(Lines)> 110:
					istart = -8
					istop = -100
					increment = -1
				else:
					istart = 1
					istop = len(Lines)-7
					increment = 1
				
				for k in range(istart,istop,increment):
					if Lines[k].find("Date")!=-1: #and k < -6: #-6 pour s'assurer que tous les infos d'une serie sont present
						info = Lines[k-1].split(",")
						info = filter(None,info)
						TimeStampList.append(int(info[1]))
						LineStartList.append(k-1)
				

				if TargetTime>= min(TimeStampList) and TargetTime<=max(TimeStampList):
					iter1 = iter1+1
					StartLine = "none"

					TimeStampListArray = np.asarray(TimeStampList)
					TDiffs = np.abs(TimeStampListArray - int(TargetTime))
					indice = np.argmin(TDiffs)
					difftimeMin = abs(TargetTime - TimeStampList[indice])
					
					if  indice < (len(TimeStampList)-2) and difftimeMin < 10000000:
						StartLine = LineStartList[indice]
						PreviousLine = LineStartList[indice-increment]
						NextLine = LineStartList[indice+increment]

						#~ self.MyLog("increment",str(increment))
						#~ self.MyLog("StartLine",str(StartLine))
						#~ self.MyLog("PreviousLine",str(PreviousLine))
						#~ self.MyLog("NextLine",str(NextLine))
						localstate = True
					
					
					if localstate == True:
						self.MyLog("FindCorrespondICOMInfo","difftimeMin="+str(difftimeMin))
						GantryAngleinterp = 0
						if (TargetTime - TimeStampList[indice])>=0:
							
							GantryInfo_0 = Lines[StartLine+3].split(",")
							GantryInfo_0 = filter(None,GantryInfo_0)
							GantryAngle_0 = float(GantryInfo_0[2])
							#self.MyLog("Lines[StartLine+3]",str(Lines[StartLine+3]))
							GantryInfo_1 = Lines[NextLine+3].split(",")
							GantryInfo_1 = filter(None,GantryInfo_1)
							GantryAngle_1 = float(GantryInfo_1[2])
							#self.MyLog("Lines[NextLine+3]",str(Lines[NextLine+3]))

							DeltaGantry = GantryAngle_1-GantryAngle_0
							DeltaTime = TimeStampList[indice+increment] - TimeStampList[indice]
							
							GSpeed = float(DeltaGantry)/float(DeltaTime)
							self.MyLog("Gantry speed",str(GSpeed))
							
							GantryAngleinterp = DeltaGantry/float(DeltaTime)*(TargetTime-TimeStampList[indice]) + GantryAngle_0
							GantryAngleinterp = np.around(GantryAngleinterp,2)
							
							msg = "G0="+str(GantryAngle_0)+",G1="+str(GantryAngle_1)+",G_interp="+str(GantryAngleinterp)
							self.MyLog("FindCorrespondingICOMInfo_GantryAngleInterpolation",msg)
						else:
							GantryInfo_0 = Lines[PreviousLine+3].split(",")
							GantryInfo_0 = filter(None,GantryInfo_0)
							GantryAngle_0 = float(GantryInfo_0[2])
							self.MyLog("Lines[PreviousLine+3]",str(Lines[PreviousLine+3]))
							GantryInfo_1 = Lines[StartLine+3].split(",")
							GantryInfo_1 = filter(None,GantryInfo_1)
							GantryAngle_1 = float(GantryInfo_1[2])
							self.MyLog("Lines[StartLine+3]",str(Lines[StartLine+3]))
														
							DeltaGantry = GantryAngle_1-GantryAngle_0
							DeltaTime = TimeStampList[indice] - TimeStampList[indice-increment]
							
							GSpeed = float(DeltaGantry)/float(DeltaTime)
							self.MyLog("Gantry speed",str(GSpeed))
							
							GantryAngleinterp = DeltaGantry/float(DeltaTime)*(TargetTime-TimeStampList[indice-increment]) + GantryAngle_0
							GantryAngleinterp = np.around(GantryAngleinterp,2)
							
							msg = "G0="+str(GantryAngle_0)+",G1="+str(GantryAngle_1)+",G_interp="+str(GantryAngleinterp)					
							self.MyLog("FindCorrespondingICOMInfo_GantryAngleInterpolation",msg)
					
					#~ difftimeMin = 9999999999
					#~ for k in range(0,len(TimeStampList)):
						#~ diff = abs(TargetTime - TimeStampList[k])
						#~ if diff < difftimeMin and diff < 10000000:
							#~ difftimeMin = diff
							#~ StartLine = LineStartList[k]
							#~ localstate = True
					
					#if localstate == True:
						#self.MyLog("FindCorrespondICOMInfo","difftimeMin="+str(difftimeMin))
						#GantryInfo = Lines[StartLine+3].split(",")
						#GantryInfo = filter(None,GantryInfo)
						DoseRateInfo = Lines[StartLine+4].split(",")
						DoseRateInfo = filter(None,DoseRateInfo)
						check1 = Lines[StartLine+7].find(":0x50010003")
						if check1!=-1:
							EnergyInfo = Lines[StartLine+7].split(",")
							EnergyInfo = filter(None,EnergyInfo)
						else:
							check1 = Lines[StartLine+8].find(":0x50010003")
							if check1!=-1:
								EnergyInfo = Lines[StartLine+8].split(",")
								EnergyInfo = filter(None,EnergyInfo)								
								
						#if len(GantryInfo)==3 or len(EnergyInfo) ==3 or len(DoseRateInfo) ==3:
						if len(EnergyInfo) ==3 or len(DoseRateInfo) ==3:
							#self.CurrentiCOMGantry = GantryInfo[2]
							self.CurrentiCOMGantry = str(GantryAngleinterp)
							self.CurrentiCOMEnergy = EnergyInfo[2].replace(" MV","MV")
							self.CurrentiCOMDoseRate = DoseRateInfo[2]
							self.MyLog("FindCorrespondICOMInfo: (Gantry,Energy)=",self.CurrentiCOMGantry+","+self.CurrentiCOMEnergy)
						else:
							iter2 = iter2+1
							localstate = False
							self.MyLog("FindCorrespondICOMInfo","else for: if len(GantryInfo)==3 ....")
					
					else:
						self.MyLog("FindCorrespondICOMInfo","else for: if localstate == True:")
					
				else:
					localstate = False
					self.MyLog("FindCorrespondICOMInfo else of"," if TargetTime>= min(TimeStampList) and TargetTime<=max(TimeStampList):")
					self.MyLog(str(TargetTime-min(TimeStampList)),str(TargetTime-max(TimeStampList)))
			except:
				self.MyLog("FindCorrespondICOMInfo","Exception")
				localstate = False
			
			time.sleep(0.03)
			timeout = time.time() - StartTime
			iter = iter+1
		
		if self.CurrentiCOMGantry!= "none" and self.CurrentiCOMEnergy!="none":
			self.Status = True
		else:
			self.Status = False
			self.MyLog("FindCorrespondICOMInfo","OUT of while =>info = none")
			
		TDIFF1 = time.time()-StartTime
		self.MyLog("FindCorrespondICOMInfo timediffs:",str(TDIFF1)+"\t"+str(iter)+"\t"+str(iter1)+"\t"+str(iter2))
		#~ f = open(os.path.join(self.SettingsObj.ROOTPATH,"Monitor.log"),"a")
		#~ f.write("FindCorrespondICOMInfo timediff: "+str(TDIFF1)+"\t"+str(iter)+"\t"+str(iter1)+"\t"+str(iter2)+"\n")
		#~ f.close()
#===========================================================================================================================================================
	def FindCorrespondingICOMInfoApprox(self):
		StartTime = time.time()
		timeout = 0
		localstate = False
		iter = 0
		iter1 = 0
		while localstate == False and timeout < 2 and self.Status == True:

			try:
				f = open(os.path.join(self.ListeningFolderPath,"iCOM","acq_detail.txt"),"r")
				Contenu = f.read()
				f.close()
				Lines = Contenu.split("\n")
				Lines = filter(None,Lines)

				TimeStampList = list()
				LineStartList = list()
				
				istart = 'none'
				istop = 'none'
				increment = 'none'
				
				if len(Lines)> 110:
					istart = -8
					istop = -100
					increment = -1
				else:
					istart = 1
					istop = len(Lines)
					increment = 1
					
				for k in range(istart,istop,increment):
					if Lines[k].find("Date")!=-1: #and k < -6: #-6 pour s'assurer que tous les infos d'une serie sont present
						info = Lines[k-1].split(",")
						info = filter(None,info)
						#TimeStampList.append(abs(int(info[1])-self.CurrentImTime))
						#LineStartList.append(k-1)
						
						
						if abs(self.CurrentImTime - int(info[1])) < 3000000:
							iter1=iter1+1
							StartLine = k-1
							
							
							localstate = True
							GantryInfo = Lines[StartLine+3].split(",")
							GantryInfo = filter(None,GantryInfo)
							EnergyInfo = Lines[StartLine+7].split(",")
							EnergyInfo = filter(None,EnergyInfo)
							DoseRateInfo = Lines[StartLine+4].split(",")
							DoseRateInfo = filter(None,DoseRateInfo)
							
							if len(GantryInfo)==3 or len(EnergyInfo) ==3 or len(DoseRateInfo) ==3:
								
								self.CurrentiCOMGantry = GantryInfo[2]
								self.CurrentiCOMEnergy = EnergyInfo[2].replace(" MV","")
								self.CurrentiCOMDoseRate = DoseRateInfo[2]
								localstate = True
							else:
								localstate = False

			except:
				localstate = False
				
			#print "self.CurrentiCOMGantry",self.CurrentiCOMGantry
			#print "self.CurrentiCOMEnergy",self.CurrentiCOMEnergy
			timeout = time.time() - StartTime
			iter = iter+1
		
		if self.CurrentiCOMGantry!= "none" and self.CurrentiCOMEnergy!="none":
			self.Status = True
		else:
			self.Status = False
			
		TDIFF1 = time.time()-StartTime
		f = open(os.path.join("C:\\EPID\\EPID_Fluoroscopie","Monitor.log"),"a")
		f.write("FindCorrespondICOMInfo timediff: "+str(TDIFF1)+"\t"+str(iter)+"\t"+str(iter1)+"\n")
		f.close()

#===========================================================================================================================================================
	def FindCorrespondingICOMInfoHybrid(self):
		self.MyLog("FindCorrespondingICOMInfoHybrid","Beginning")
		self.TimeDiffMax = 10000000
		StartTime = time.time()
		timeout = 0
		localstate = False
		iter = 0
		iter1 = 0
		while localstate == False and timeout < 2 and self.Status == True:

			try:
				f = open(os.path.join(self.ListeningFolderPath,"iCOM","acq_detail.txt"),"r")
				Contenu = f.read()
				f.close()
				Lines = Contenu.split("\n")
				Lines = filter(None,Lines)

				TimeStampList = list()
				LineStartList = list()
				
				istart = 'none'
				istop = 'none'
				increment = 'none'
				
				if len(Lines)> 110:
					istart = -8
					istop = -100
					increment = -1
				else:
					istart = 1
					istop = len(Lines)-7
					increment = 1
					
				for k in range(istart,istop,increment):
					if Lines[k].find("Date")!=-1: #and k < -6: #-6 pour s'assurer que tous les infos d'une serie sont present
						info = Lines[k-1].split(",")
						info = filter(None,info)
						#TimeStampList.append(abs(int(info[1])-self.CurrentImTime))
						#LineStartList.append(k-1)
						
						if abs(self.CurrentImTime - int(info[1])) < self.TimeDiffMax:
							iter1=iter1+1
							StartLine = k-1
							localstate = True
							GantryInfo = Lines[StartLine+3].split(",")
							GantryInfo = filter(None,GantryInfo)
							DoseRateInfo = Lines[StartLine+4].split(",")
							DoseRateInfo = filter(None,DoseRateInfo)

							#~ EnergyInfo = Lines[StartLine+7].split(",")
							#~ EnergyInfo = filter(None,EnergyInfo)

							check1 = Lines[StartLine+7].find(":0x50010003")
							if check1!=-1:
								EnergyInfo = Lines[StartLine+7].split(",")
								EnergyInfo = filter(None,EnergyInfo)
							else:
								check1 = Lines[StartLine+8].find(":0x50010003")
								if check1!=-1:
									EnergyInfo = Lines[StartLine+8].split(",")
									EnergyInfo = filter(None,EnergyInfo)						

							
							if len(GantryInfo)==3 or len(EnergyInfo) ==3 or len(DoseRateInfo) ==3:
								NewICOMGantry = GantryInfo[2]
								
								
								if self.TimeDiffMax == 10000000 and abs(float(self.CurrentiCOMGantry) - float(NewICOMGantry))<2 :								
									self.CurrentiCOMGantry = GantryInfo[2]
									self.CurrentiCOMEnergy = EnergyInfo[2].replace(" MV","MV")
									self.CurrentiCOMDoseRate = DoseRateInfo[2]
									localstate = True
									self.MyLog("FindCorrespondingICOMInfoHybrid: in DiffGantry<2 (Gantry,Energy)=",self.CurrentiCOMGantry+","+self.CurrentiCOMEnergy)
								
								else:
									
									if self.TimeDiffMax==3000000:
										self.CurrentiCOMGantry = GantryInfo[2]
										self.CurrentiCOMEnergy = EnergyInfo[2].replace(" MV","MV")
										self.CurrentiCOMDoseRate = DoseRateInfo[2]
										localstate = True
										self.MyLog("FindCorrespondingICOMInfoHybrid: in if self.TimeDiffMax==3000000: (Gantry,Energy)=",self.CurrentiCOMGantry+","+self.CurrentiCOMEnergy)
										
									else:
										localstate = False
										self.TimeDiffMax = 3000000
							else:
								localstate = False
								self.MyLog("FindCorrespondingICOMInfoHybrid","else for: if len(GantryInfo)==3 ....")

			except:
				self.MyLog("FindCorrespondingICOMInfoHybrid","Exception")
				localstate = False

			timeout = time.time() - StartTime
			iter = iter+1
		
		if self.CurrentiCOMGantry!= "none" and self.CurrentiCOMEnergy!="none":
			self.Status = True
		else:
			self.Status = False
			self.MyLog("FindCorrespondingICOMInfoHybrid","OUT of while =>info = none")
			
		TDIFF1 = time.time()-StartTime
		self.MyLog("FindCorrespondingICOMInfoHybrid timediffs:",str(TDIFF1)+"\t"+str(iter)+"\t"+str(iter1))
		#~ f = open(os.path.join(self.SettingsObj.ROOTPATH,"Monitor.log"),"a")
		#~ f.write("FindCorrespondingICOMInfoHybrid timediff: "+str(TDIFF1)+"\t"+str(iter)+"\t"+str(iter1)+"\n")
		#~ f.close()
#===========================================================================================================================================================
	def GetLastImageInfo(self):
		Flag = False
		try:
			f = open(os.path.join(self.ListeningFolderPath,"image","acq_im_detail.txt"),"r")
			Contenu = f.read()
			f.close()
			Lines = Contenu.split("\n")
			Lines = filter(None,Lines)
			
			if len(Lines) > 3:
				info = Lines[-2].split(",") #On choisit la derniere image ***-3***
				info = filter(None,info)
				
				if len(info) == 2:
					self.CurrentImFilePath = os.path.join(self.ListeningFolderPath,"image","acq"+str(info[0])+".bin")
					self.CurrentImTime = int(info[1]) + self.SettingsObj.ImageTimeOffset #Add an offset to the timestamp of the image because we dont know the exact moment the time stamp is corresponding to.
					self.Status = True
					
					
					if self.CurrentImFilePath!=self.LastImFilePath and abs(os.path.getctime(self.CurrentImFilePath)-time.time())<=2:
						self.LastImFilePath = self.CurrentImFilePath
						Flag = True
						self.MyLog("GetLastImageInfo Flag=True"+ self.LastImFilePath + "TimeDiff=",str(abs(os.path.getctime(self.CurrentImFilePath)-time.time())))
						
						#~ if abs(os.path.getctime(self.CurrentImFilePath)-time.time())>2:
							#~ Flag = False
							#~ self.MyLog("GetLastImageInfo TimeDiff > 2 sec:",str(abs(os.path.getctime(self.CurrentImFilePath)-time.time())))
							
					else:
						Flag = False
						self.MyLog("GetLastImageInfo: else for: self.CurrentImFilePath!=self.LastImFilePath ....:",str(abs(os.path.getctime(self.CurrentImFilePath)-time.time())))

				else:
					self.MyLog("GetLastImageInfo","else for:  if len(info) == 2:")
							
			else:
				self.MyLog("GetLastImageInfo","else for:    if len(Lines) > 3:")
				
		except:
			self.Status = False
			self.MyLog("GetLastImageInfo","fail except")

		return Flag
#===========================================================================================================================================================
if __name__ == "__main__":
	PatientID = "1234"
	Monitor(PatientID)
