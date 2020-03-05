from datetime import datetime
import numpy as np
import os, os.path
from matplotlib import pyplot as plt
import sys
#~ import scipy.signal
#~ import Settings
import shutil
#========================================================================================================
class Calibration:
	
	def __init__( self, thisSettingsObj):

		
		self.SettingsObj = thisSettingsObj
		self.LevelList = list() #Dose rate levels for multi level gain

		self.ImCount = 0
		self.Offset = np.zeros((1024,1024),dtype=np.float64)
		self.Slope = np.zeros((1024,1024),dtype=np.float64)
		self.Residual = np.zeros((1024,1024),dtype=np.float64)
		self.LinearMask = np.zeros((1024,1024),dtype=np.float32)
		self.FrameCalibrated = np.zeros((1024,1024),dtype=np.float32) #The frame calibrated
		self.BackgroundFrame = np.zeros((1024,1024),dtype=np.float32) #The background frame
		self.MedianArray3D = np.zeros((9,1024,1024),np.float64)
		
		self.MLG = None #3D array [level,1024,1024] dtype=float32
		self.MLGSlopes = None #3D array [bin-level,1024,1024] dtype=float32
		
		#****Functions****
		self.ClearLogs()
		self.MyLog("__init__","end of init")
#--------------------------------------------------------------------------------------------------------------------------------------------
	def ClearLogs(self):
		try:
			os.remove(os.path.join(self.SettingsObj.ROOTPATH,"Logs","Mod_Calibration.log"))
		except:
			pass
#--------------------------------------------------------------------------------------------------------------------------------------------
	def MyLog(self,mess="none",value="none"):
		f = open(os.path.join(self.SettingsObj.ROOTPATH,"Logs","Mod_Calibration.log"),"a")
		f.write(str(mess)+"\t"+str(value)+"\t"+str(datetime.now())+"\n")
		f.close()
#-----------------------------------------------------------------------------------------------------------------------------
	def DefineBackground(self,thisFilePathList):
		BGFrames = np.zeros((len(thisFilePathList),1024,1024),np.uint16)
		incr =0
		for f in thisFilePathList:
			A = np.fromfile(f,dtype=np.uint16)
			A=A.reshape(1024,1024)
			BGFrames[incr] = A
			incr = incr +1

		self.BackgroundFrame = np.median(BGFrames,axis=0) #float64
		self.BackgroundFrame = self.BackgroundFrame.astype(np.float32)
		#self.BackgroundFrame.tofile(os.path.join(self.SettingsObj.ROOTPATH,"Background.raw"))        
#----------------------------------------------------------------------------------------------------------------------------		
	def LoadFiles(self,thisROOT):
		#print thisROOT
		self.ROOTPATH = thisROOT
		self.LevelList = list() #Dose rate levels for multi level gain
		
		f = open(os.path.join(self.ROOTPATH,'Files.Calib'))
		Contenu = f.read()
		f.close()
		Lines = Contenu.split("\n")
		Lines = filter(None,Lines)
		
		
		thisList = list()
		for l in Lines:
			if l.endswith('.raw'):
				thisList.append(os.path.join(self.ROOTPATH,l))
				els = l.split(".raw")
				dr = els[0].replace("DR","")
				#dr = dr.replace(".bin","")
				self.LevelList.append(float(dr))

		self.MLG = np.zeros((len(self.LevelList),1024,1024),dtype=np.float32)
		self.MLGSlopes = np.zeros((len(self.LevelList),1024,1024),dtype=np.float32)
		
		#***Load MLG
		incr = 0
		for l in thisList:
			#print l
			a= np.fromfile(l,dtype=np.float32)
			b=a.reshape(1024,1024)
			b[b<=0] = 1
			self.MLG[incr,:,:] = b[:,:]
			incr = incr +1

		#***Compute MLGSlopes
		self.MLGSlopes[0] = self.LevelList[0]*(1.0/self.MLG[0])
		for k in range(1,len(self.LevelList)):
			DeltaI = self.MLG[k]-self.MLG[k-1] #Change in pixel intensity
			DeltaI[DeltaI<=0] = 1
			DeltaD = self.LevelList[k]-self.LevelList[k-1] #Change in dose rate
			self.MLGSlopes[k] = DeltaD*(1.0/DeltaI)
			#self.MLGSlopes[k].tofile("Slope_"+str(k)+".raw")
			#~ print DeltaI[512,512], DeltaD,slope[512,512]

		#***Load linear calibration
		self.Offset = np.fromfile(os.path.join(self.ROOTPATH,'Offset.raw'),dtype=np.float64)
		self.Offset = self.Offset.reshape(1024,1024)

		self.Slope = np.fromfile(os.path.join(self.ROOTPATH,'Slope.raw'),dtype=np.float64)
		self.Slope = self.Slope.reshape(1024,1024)
		
		self.Residual = np.fromfile(os.path.join(self.ROOTPATH,'Residual.raw'),dtype=np.float64)
		self.Residual = self.Residual.reshape(1024,1024)
		
		self.LinearMask[self.Residual >=0.999] =  1
		self.MyLog("LoadFiles","Completed")

#----------------------------------------------------------------------------------------------------------------------------
	def LMSRegression(self,thisEnergy):
		#print self.LevelList
		NbLevel = len(self.LevelList)
		
		#Compute Means
		MeanDR = np.mean(self.LevelList)
		MeanArray = np.mean(self.MLG,axis=0)
		#MeanArray.tofile(os.path.join(self.SettingsObj.ROOTPATH,"MeanArray.raw"))
		
		#Compute PCA vectors
		XPCAVectors = self.LevelList - MeanDR
		#print XPCAVectors
		YPCAVectors = np.zeros((NbLevel,1024,1024),np.float64)
		for k in range(NbLevel):
			YPCAVectors[k,:,:] = self.MLG[k,:,:] - MeanArray[:,:]
		#	XPCAVectors.append(self.LevelList[k]-MeanDR)
		#MeanArray.tofile(os.path.join(self.SettingsObj.ROOTPATH,"MeanArray.raw"))

		#Compute covariant matrix elements
		CovArray = np.zeros((1024,1024),np.float64)
		CovxArray = np.zeros((1024,1024),np.float64)
		CovyArray = np.zeros((1024,1024),np.float64)
		
		for k in range(NbLevel):
			CovArray[:,:] = CovArray[:,:] + XPCAVectors[k]*YPCAVectors[k,:,:]
			CovxArray[:,:] = CovxArray[:,:] + XPCAVectors[k]*XPCAVectors[k]
			CovyArray[:,:] = CovyArray[:,:] + YPCAVectors[k,:,:]*YPCAVectors[k,:,:]

		CovArray[CovArray ==0] = 0.00001
		#~ CovxArray[CovxArray ==0] = 1
		#~ CovyArray[CovyArray ==0] = 1

		#CovArray.tofile(os.path.join(self.SettingsObj.ROOTPATH,"CovArray.raw"))
		#CovxArray.tofile(os.path.join(self.SettingsObj.ROOTPATH,"CovxArray.raw"))
		#CovyArray.tofile(os.path.join(self.SettingsObj.ROOTPATH,"CovyArray.raw"))
		
		SlopeArray = np.zeros((1024,1024),np.float64)
		OffsetArray = np.zeros((1024,1024),np.float64)		
		
		SlopeArray[:,:] = CovxArray[:,:]*(1.0/CovArray[:,:])
		SlopeArray.tofile(os.path.join(self.SettingsObj.ROOTPATH,thisEnergy,"Slope.raw"))
		OffsetArray[:,:] = MeanDR - SlopeArray[:,:]*MeanArray[:,:]
		OffsetArray.tofile(os.path.join(self.SettingsObj.ROOTPATH,thisEnergy,"Offset.raw"))
		
		rvalue = np.zeros((1024,1024),np.float64)
		sstot = np.zeros((1024,1024),np.float64)
		ssres = np.zeros((1024,1024),np.float64)
		for k in range(NbLevel):
			sstot[:,:] = sstot[:,:] + (self.LevelList[k]-MeanDR)*(self.LevelList[k]-MeanDR)
			ssres[:,:] = ssres[:,:] + (OffsetArray[:,:]+SlopeArray[:,:]*self.MLG[k,:,:]-self.LevelList[k])*(OffsetArray[:,:]+SlopeArray[:,:]*self.MLG[k,:,:]-self.LevelList[k])
			#print ssres[512,512],OffsetArray[512,512],SlopeArray[512,512],self.LevelList[k],self.MLG[k,512,512]
		
		
		#sstot.tofile(os.path.join(self.SettingsObj.ROOTPATH,"sstot.raw"))
		#ssres.tofile(os.path.join(self.SettingsObj.ROOTPATH,"ssres.raw"))
		sstot[sstot ==0] = 0.00001
		rvalue[:,:] = 1.0-ssres[:,:]*(1.0/sstot[:,:])
		rvalue[rvalue <0] = 0
		rvalue = np.sqrt(rvalue)
		rvalue.tofile(os.path.join(self.SettingsObj.ROOTPATH,thisEnergy,"Residual.raw"))
#----------------------------------------------------------------------------------------------------------------------------
	def GetLevelTemporalMedian(self,thisFilePathList,thisDoseRate,thisEnergy):
		self.LevelList.append(thisDoseRate)
		self.MyLog("GetLevelTemporalMedian: this level dose rate",str(thisDoseRate))
		Nb = len(thisFilePathList)
		if len(thisFilePathList)>	100:
			Nb = 100
		Frames = np.zeros((Nb,1024,1024),np.uint16)

		for k in range(Nb):
			im = np.fromfile(thisFilePathList[k],np.uint16)
			im = im.reshape(1024,1024)
			Frames[k] = im
			self.MyLog("GetLevelTemporalMedian:",thisFilePathList[k])
		
		LevelMedian = np.median(Frames,axis=0) - self.BackgroundFrame
		#~ print LevelMedian.shape, type(LevelMedian[0,0])
		#LevelMedian = LevelMedian.astype(np.int32)
		#~ LevelMedian.tofile("DR__"+str(thisDoseRate)+".raw")
		LevelMedian = LevelMedian.astype(np.float32)
		self.MLG[len(self.LevelList)-1] = LevelMedian
		#LevelMedian = LevelMedian.astype(np.int32)
		LevelMedian.tofile(os.path.join(self.SettingsObj.ROOTPATH,thisEnergy,"DR"+str(int(thisDoseRate))+".raw"))
#----------------------------------------------------------------------------------------------------------------------------
	def CalibrateFrame(self,thisFilePath):
		self.MyLog("CalibrateFrame",thisFilePath)
		#head,tail = os.path.split(thisFilePath)
		A = np.fromfile(thisFilePath,dtype=np.uint16)
		A = A.reshape(1024,1024)
		#print A[512,512], self.BackgroundFrame[512,512]
		#A = A-self.BackgroundFrame 
		#print A[512,512]
		self.FrameCalibrated = np.multiply(np.subtract(A,self.BackgroundFrame),self.Slope) + self.Offset
		#print A[512,512],self.Slope[512,512],self.Offset[512,512]
		#print self.FrameCalibrated[512,512]
		#self.FrameCalibrated = scipy.signal.medfilt(self.FrameCalibrated,(3,3))
		#print self.FrameCalibrated[512,512]

		#Spatial Median 3x3
		self.MedianArray3D[0,1:1023,1:1023] = self.FrameCalibrated[0:1022,0:1022]
		self.MedianArray3D[1,1:1023,1:1023] = self.FrameCalibrated[0:1022,1:1023]
		self.MedianArray3D[2,1:1023,1:1023] = self.FrameCalibrated[0:1022,2:1024]

		self.MedianArray3D[3,1:1023,1:1023] = self.FrameCalibrated[1:1023,0:1022]
		self.MedianArray3D[4,1:1023,1:1023] = self.FrameCalibrated[1:1023,1:1023]
		self.MedianArray3D[5,1:1023,1:1023] = self.FrameCalibrated[1:1023,2:1024]

		self.MedianArray3D[6,1:1023,1:1023] = self.FrameCalibrated[2:1024,0:1022]
		self.MedianArray3D[7,1:1023,1:1023] = self.FrameCalibrated[2:1024,1:1023]
		self.MedianArray3D[8,1:1023,1:1023] = self.FrameCalibrated[2:1024,2:1024]
		
		#Sorting is faster than median
		#self.FrameCalibrated = np.median(self.MedianArray3D,axis=0)
		self.MedianArray3D.sort(axis=0)
		self.FrameCalibrated[:,:] = self.MedianArray3D[4,:,:]


		if self.SettingsObj.SAVERAW==True:
			fname = "FlexmapFrame_"+str(self.ImCount) + ".raw"
			self.FrameCalibrated.tofile(os.path.join(self.SettingsObj.ROOTPATH,"SaveRaw",fname))

		self.ImCount = self.ImCount + 1

		#~ plt.imshow(self.FrameCalibrated)
		#~ plt.show()
		#print type(self.FrameCalibrated[512,512])
		#self.FrameCalibrated = self.FrameCalibrated.astype(np.float32)
		#self.FrameCalibrated.tofile(os.path.join(self.SettingsObj.ROOTPATH,tail+".raw"))
		
		#~ mask = np.less(A,self.MLG[0]).astype(float)
		
		#~ for k in range(0,5):
			#~ D1 = np.less(A,self.MLG[k]).astype(float)
			#~ print A[512,512],self.MLG[k,512,512],D1[512,512]
			#~ print D1[0,0].astype(float)
			#~ plt.imshow(D1)
			#~ plt.show()
#----------------------------------------------------------------------------------------------------------------------------------------------------
	def InitNewFlexmap(self):
		self.GantryAngleList = list()
		self.YIsoList = list()
		self.XIsoList = list()
#-----------------------------------------------------------------------------------------------------------------------------------------------------
	def GetFlexmapDirection(self):
		if self.GantryAngleList[25] < self.GantryAngleList[50]:
			return "CW"
		elif self.GantryAngleList[25] > self.GantryAngleList[50]:
			return "CCW"
		else:
			return "None"
#----------------------------------------------------------------------------------------------------------------------------------------------------
	#~ def DeleteOldFlexmap(self):
		#~ success = True
		#~ FileList = ["Panel.flexmap","Panel_CW.flexmap","Panel_CCW.flexmap"]
		#~ for fname in FileList:		
			#~ if os.path.isfile(os.path.join(self.SettingsObj.ROOTPATH,"CalibrationFiles",fname)):
				#~ try:
					#~ os.remove(os.path.join(self.SettingsObj.ROOTPATH,"CalibrationFiles",fname))
				#~ except:
					#~ success = False
		#~ return success
#-------------------------------------------------------------------------------------------------------------------------------------------------
	def DeleteOldGainCalibration(self,thisEnergy):
		success = True
		if os.path.isdir(os.path.join(self.SettingsObj.ROOTPATH,"CalibrationFiles",thisEnergy)):
			try:
				shutil.rmtree(os.path.join(self.SettingsObj.ROOTPATH,"CalibrationFiles",thisEnergy))
			except:
				success = False
		return success
#------------------------------------------------------------------------------------------------------------------------------------------
	def UpdateAverageFlexmap(self):
		
		Commit = True
		
		CW_GList = list()#Clockwise 
		CW_XList = list()
		CW_YList = list()

		CCW_GList = list()
		CCW_XList = list()
		CCW_YList = list()

		AVG_GList = np.arange(-180.0,181.0,2.0)
		AVG_XList = list()
		AVG_YList = list()

		thisFilePath = os.path.join(self.SettingsObj.ROOTPATH,"CalibrationFiles","Panel_CW.flexmap")
		if os.path.isfile(thisFilePath)==True:
			f = open(thisFilePath)
			Contenu = f.read()
			f.close()
			Lines = Contenu.split("\n")
			Lines = filter(None,Lines)
			for k in range(1,len(Lines)):
				els = Lines[k].split(";")
				els = filter(None,els)
				CW_GList.append(float(els[0]))
				CW_XList.append(float(els[1])) #BBX dans le referentiel PyComView
				CW_YList.append(float(els[2])) #BBY dans le referentiel  PyComView


		thisFilePath = os.path.join(self.SettingsObj.ROOTPATH,"CalibrationFiles","Panel_CCW.flexmap")
		if os.path.isfile(thisFilePath)==True:
			f = open(thisFilePath)
			Contenu = f.read()
			f.close()
			Lines = Contenu.split("\n")
			Lines = filter(None,Lines)
			for k in range(1,len(Lines)):
				els = Lines[k].split(";")
				els = filter(None,els)
				CCW_GList.append(float(els[0]))
				CCW_XList.append(float(els[1])) #BBX dans le referentiel PyComView
				CCW_YList.append(float(els[2])) #BBY dans le referentiel  PyComView


		if len(CW_GList)>0 and len(CCW_GList)>0:
			CW_xs = np.interp(AVG_GList,CW_GList,CW_XList)
			CW_ys = np.interp(AVG_GList,CW_GList,CW_YList)
			
			CCW_xs = np.interp(AVG_GList,CCW_GList[::-1],CCW_XList[::-1])#Reverse list order, np.interp needs ascending order,
			CCW_ys = np.interp(AVG_GList,CCW_GList[::-1],CCW_YList[::-1])
			
			AVG_XList = np.mean([CW_xs,CCW_xs],axis=0)
			AVG_YList = np.mean([CW_ys,CCW_ys],axis=0)

		elif len(CW_GList)>0 and len(CCW_GList)==0:
			AVG_XList = np.interp(AVG_GList,CW_GList,CW_XList) #Reverse order
			AVG_YList = np.interp(AVG_GList,CW_GList,CW_YList)

		elif len(CW_GList)==0 and len(CCW_GList)>0:
			AVG_XList = np.interp(AVG_GList,CCW_GList[::-1],CCW_XList[::-1]) #Reverse list order, np.interp needs ascending order,
			AVG_YList = np.interp(AVG_GList,CCW_GList[::-1],CCW_YList[::-1])
		else:
			Commit = False
		
		filepath = os.path.join(self.SettingsObj.ROOTPATH,"CalibrationFiles","Panel.flexmap")
		if os.path.isfile(filepath):
			try:
				os.remove(filepath)
			except:
				Commit = False

		if Commit == True:
			f = open(filepath,"w")
			f.write("GantryAngle;BBX;BBY"+"\n")
			for k in range(len(AVG_GList)):
				f.write(str(AVG_GList[k]) + ";" + str(np.around(AVG_XList[k],1)) + ";" + str(np.around(AVG_YList[k],1))+"\n")
			f.close()			

#------------------------------------------------------------------------------------------------------------------------------------------
	def CommitFlexmap(self):
		#Directional flexmap
		dir = self.GetFlexmapDirection()
		filepath = os.path.join(self.SettingsObj.ROOTPATH,"CalibrationFiles","Panel_"+dir+".flexmap")
		
		success = True
		if os.path.isfile(filepath):
			try:
				os.remove(filepath)
			except:
				success = False

		f = open(filepath,"w")
		f.write("GantryAngle;BBX;BBY"+"\n")
		for k in range(len(self.GantryAngleList)):
			f.write(str(self.GantryAngleList[k]) + ";" + str(np.around(self.XIsoList[k],1)) + ";" + str(np.around(self.YIsoList[k],1))+"\n")
		f.close()	

		self.UpdateAverageFlexmap()

		return success
#-------------------------------------------------------------------------------------------------------------------------------------------
	def CommitGainCalibration(self,thisEnergy):
		success = True
		if os.path.isdir(os.path.join(self.SettingsObj.ROOTPATH,"CalibrationFiles",thisEnergy)):
			try:
				shutil.rmtree(os.path.join(self.SettingsObj.ROOTPATH,"CalibrationFiles",thisEnergy))
			except:
				success = False

		shutil.move(os.path.join(self.SettingsObj.ROOTPATH,thisEnergy),os.path.join(self.SettingsObj.ROOTPATH,"CalibrationFiles",thisEnergy))

		return success
#===================================================================================================================
if __name__ == "__main__":
	ROOTPATH = os.path.join('C:\\EPID','CalibrationFiles','6MV')
	A = Calibration()
	A.LoadFiles(ROOTPATH)
#	sys.exit()
	
	BGList = list()
	thisFilePath = os.path.join('C:\EPID\EPID_Listening\unknown\\2020-02-05_14-31-03\image','acq00000.bin')
	BGList.append(thisFilePath)
	thisFilePath = os.path.join('C:\EPID\EPID_Listening\unknown\\2020-02-05_14-31-03\image','acq00001.bin')
	BGList.append(thisFilePath)
	thisFilePath = os.path.join('C:\EPID\EPID_Listening\unknown\\2020-02-05_14-31-03\image','acq00002.bin')
	BGList.append(thisFilePath)
	A.DefineBackground(BGList)
	thisFilePath = os.path.join('C:\EPID\EPID_Listening\unknown\\2030-11-26_18-26-21\image','acq00050.bin')
	A.CalibrateFrame(thisFilePath)
	
	