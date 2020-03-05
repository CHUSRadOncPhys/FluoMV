import os, os.path
import sys
sys.path += ['.'] #For scipy
import numpy as np
from datetime import datetime
import time
import scipy
import scipy.ndimage
#~ from matplotlib import pyplot as plt
import Settings
#============================================================================================================================================================
class Calibration():
	
	def __init__(self,settingsObj):
		
		self.SettingsObj = settingsObj #Settings.Settings()
		
		self.EnergyList = list()
		self.Slopes = None #[(len(self.EnergyList),1024,1024]
		self.Offsets = None #[(len(self.EnergyList),1024,1024]
		self.Residuals = None #[(len(self.EnergyList),1024,1024]
		
		self.FlexmapGantryList = list()
		self.FlexmapGantryListArray = None #Numpy array == self.FlexmapGantryList. Need a array to use np.argmin()
		self.FlexmapOffsetXList = list()
		self.FlexmapOffsetYList = list()
		
		self.ImCount = 0
		self.ImGantryAngle = 0
		self.BackgroundFrame = np.zeros((1024,1024),dtype=np.float32) #The median background frame 
		self.FrameCalibrated = np.zeros((1024,1024),dtype=np.float32) #The frame calibrated
		self.FrameCalibratedShift = np.zeros((4,1024,1024),dtype=np.float32) #The frame calibrated shifted by the flexmap calibration

		self.BinArray3D = np.zeros((4,1024,1024),np.float64) #Use for binning the image 2x2 => 1024x1024=>512x512
		self.MedianArray3D = np.zeros((9,512,512),np.float64) #Use for calculating spatial median filter 3x3
		self.FrameCalibratedBinned = np.zeros((512,512),np.float32) #Final image calibrated and binned
		self.FrameDisplayed = np.zeros((512,512),np.float32)

		#*****Functions*****
		self.ClearLogs()
		if self.SettingsObj.debugLvl!=2079:
			self.LoadCalibrations()
			self.LoadFlexmap()
		
		if os.path.isdir(os.path.join(self.SettingsObj.ROOTPATH,"SaveRaw"))==False:
			try:
				os.mkdir(os.path.join(self.SettingsObj.ROOTPATH,"SaveRaw"))
			except:
				pass
#--------------------------------------------------------------------------------------------------------------------------------------------
	def ClearLogs(self):
		try:
			os.remove(os.path.join(self.SettingsObj.ROOTPATH,"Logs","LiveCalibration.log"))
		except:
			pass
#--------------------------------------------------------------------------------------------------------------------------------------------
	def MyLog(self,mess="none",value="none",level=0):
		if level<=self.SettingsObj.debugLvl:
			f = open(os.path.join(self.SettingsObj.ROOTPATH,"Logs","LiveCalibration.log"),"a")
			f.write(str(mess)+"\t"+str(value)+"\t"+str(datetime.now())+"\n")
			f.close()
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	def LoadCalibrations(self):
		AllFiles = os.listdir(os.path.join(self.SettingsObj.ROOTPATH,"CalibrationFiles"))
		for f in AllFiles:
			if os.path.isdir(os.path.join(self.SettingsObj.ROOTPATH,"CalibrationFiles",f)):
				self.EnergyList.append(f)
		self.MyLog("LoadCalibrations: len(self.EnergyList)",str(len(self.EnergyList)))
		
		self.Slopes = np.zeros((len(self.EnergyList),1024,1024),np.float64)
		self.Offsets = np.zeros((len(self.EnergyList),1024,1024),np.float64)
		self.Residuals = np.zeros((len(self.EnergyList),1024,1024),np.float64)
		
		incr = 0
		for E in self.EnergyList:
			thisSlope = np.fromfile(os.path.join(self.SettingsObj.ROOTPATH,"CalibrationFiles",E,"Slope.raw"),np.float64)
			thisSlope = thisSlope.reshape(1024,1024)
			self.Slopes[incr,:,:] =thisSlope[:,:]

			thisOffset = np.fromfile(os.path.join(self.SettingsObj.ROOTPATH,"CalibrationFiles",E,"Offset.raw"),np.float64)
			thisOffset = thisOffset.reshape(1024,1024)
			self.Offsets[incr,:,:] =thisOffset[:,:]
			
			thisResidual = np.fromfile(os.path.join(self.SettingsObj.ROOTPATH,"CalibrationFiles",E,"Residual.raw"),np.float64)
			thisResidual = thisResidual.reshape(1024,1024)
			self.Residuals[incr,:,:] =thisResidual[:,:]
			incr = incr + 1
#--------------------------------------------------------------------------------------------------------------------------------------------
	def LoadFlexmap(self):
		self.FlexmapGantryList = list()
		self.FlexmapOffsetXList = list()
		self.FlexmapOffsetYList = list()
		
		f = open(os.path.join(self.SettingsObj.ROOTPATH,"CalibrationFiles","Panel.flexmap"))
		Contenu = f.read()
		f.close()
		Lines = Contenu.split("\n")
		Lines = filter(None,Lines)
		for k in range(1,len(Lines)): #skip the header
			els = Lines[k].split(";")
			els = filter(None,els)
			self.FlexmapGantryList.append(float(els[0]))
			self.FlexmapOffsetXList.append(float(els[1])-512)
			self.FlexmapOffsetYList.append(float(els[2])-512)
		self.FlexmapGantryListArray = np.asarray(self.FlexmapGantryList)
#-----------------------------------------------------------------------------------------------------------------------------
	def DefineBackgroundImage(self,thisFilePathList):
		BGFrames = np.zeros((len(thisFilePathList),1024,1024),np.uint16)
		incr =0
		for f in thisFilePathList:
			A = np.fromfile(f,dtype=np.uint16)
			A=A.reshape(1024,1024)
			BGFrames[incr] = A
			incr = incr +1

		self.BackgroundFrame = np.median(BGFrames,axis=0) #return a float64 ndarray
		self.BackgroundFrame = self.BackgroundFrame.astype(np.float32)
		self.MyLog("DefineBackgroundImage:len(thisFilePathList)",str(len(thisFilePathList)))
#----------------------------------------------------------------------------------------------------------------------------
	def CalibrateFrame(self,thisFilePath,thisEnergy,thisGantryAngleDict):
		ROIs = thisGantryAngleDict.keys()
		self.MyLog("CalibrateFrame",thisFilePath + "," + str(thisEnergy) +"," + str(thisGantryAngleDict[ROIs[0]]))
		t1 = time.clock()
		
		index = self.EnergyList.index(thisEnergy)
		A = np.fromfile(thisFilePath,dtype=np.uint16)
		t2 = time.clock()
		A = A.reshape(1024,1024)
		t3 = time.clock()
		self.FrameCalibrated = np.multiply(np.subtract(A,self.BackgroundFrame),self.Slopes[index]) + self.Offsets[index]
		self.FrameCalibrated = scipy.ndimage.filters.median_filter(self.FrameCalibrated,size=(3,3))
		t4 = time.clock()
		
		#self.MyLog("CalibrateFrame:Max1",str(np.max(self.FrameCalibrated)))
		t5 = time.clock()
		
		#Image translation based of the flexmap offsets
		GDiffs = np.abs(self.FlexmapGantryListArray - float(thisGantryAngleDict[ROIs[0]]))
		index = np.argmin(GDiffs)
		shiftX = self.FlexmapOffsetXList[index]
		shiftY = self.FlexmapOffsetYList[index]
		#self.MyLog("CalibrateFrame self.FlexmapGantryList[index]=",str(self.FlexmapGantryList[index]))
		self.MyLog("CalibrateFrame shiftX",str(shiftX))
		self.MyLog("CalibrateFrame shiftY",str(shiftY))
		

		if shiftX>=0 and shiftY>=0:
			#~ self.FrameCalibrated[0:(1024-shiftY),0:(1024-shiftX)] = self.FrameCalibrated[shiftY:,shiftX:]

			shiftX0 = int(shiftX)
			shiftX1 = shiftX0 + 1
			shiftY0 = int(shiftY)
			shiftY1 = shiftY0 + 1
			wx0 = shiftX1-shiftX
			wx1 = 1-wx0
			wy0 = shiftY1-shiftY
			wy1 = 1-wy0
			self.MyLog("wx0="+str(wx0),"wx1="+str(wx1))
			self.MyLog("wy0="+str(wy0),"wy1="+str(wy1))
			self.MyLog("type FrameCalibratedShift = "+str(type(self.FrameCalibratedShift[0,0,0])),"type FrameCalibrated = "+str(type(self.FrameCalibrated[0,0])))

			self.FrameCalibratedShift[0,0:(1024-shiftY0),0:(1024-shiftX0)] = self.FrameCalibrated[shiftY0:,shiftX0:] 
			self.FrameCalibratedShift[1,0:(1024-shiftY0),0:(1024-shiftX1)] = self.FrameCalibrated[shiftY0:,shiftX1:] 
			self.FrameCalibratedShift[2,0:(1024-shiftY1),0:(1024-shiftX0)] = self.FrameCalibrated[shiftY1:,shiftX0:]
			self.FrameCalibratedShift[3,0:(1024-shiftY1),0:(1024-shiftX1)] = self.FrameCalibrated[shiftY1:,shiftX1:]
			self.MyLog('case=','if shiftX>=0 and shiftY>=0:')
			
			self.FrameCalibrated[:,:] = wy0*(wx0*self.FrameCalibratedShift[0,:,:] + wx1*self.FrameCalibratedShift[1,:,:]) + wy1*(wx0*self.FrameCalibratedShift[2,:,:] + wx1*self.FrameCalibratedShift[3,:,:])
			self.MyLog("WeightCompleted","")
		elif shiftX<0 and shiftY<0:
			#~ self.FrameCalibrated[-shiftY:1024,-shiftX:1024] = self.FrameCalibrated[0:(1024+shiftY),0:(1024+shiftX)]

			shiftX1 = int(shiftX)
			shiftX0 = shiftX1 - 1
			shiftY1 = int(shiftY)
			shiftY0 = shiftY1 - 1
			wx0 = shiftX1-shiftX
			wx1 = 1-wx0
			wy0 = shiftY1-shiftY
			wy1 = 1-wy0
			self.MyLog("wx0="+str(wx0),"wx1="+str(wx1))
			self.MyLog("wy0="+str(wy0),"wy1="+str(wy1))
			self.FrameCalibratedShift[0,-shiftY0:1024,-shiftX0:1024] = self.FrameCalibrated[0:(1024+shiftY0),0:(1024+shiftX0)]
			self.FrameCalibratedShift[1,-shiftY0:1024,-shiftX1:1024] = self.FrameCalibrated[0:(1024+shiftY0),0:(1024+shiftX1)]
			self.FrameCalibratedShift[2,-shiftY1:1024,-shiftX0:1024] = self.FrameCalibrated[0:(1024+shiftY1),0:(1024+shiftX0)]
			self.FrameCalibratedShift[3,-shiftY1:1024,-shiftX1:1024] = self.FrameCalibrated[0:(1024+shiftY1),0:(1024+shiftX1)]
			self.MyLog('case=','elif shiftX<0 and shiftY<0:')
			self.FrameCalibrated[:,:] = wy0*(wx0*self.FrameCalibratedShift[0,:,:] + wx1*self.FrameCalibratedShift[1,:,:]) + wy1*(wx0*self.FrameCalibratedShift[2,:,:] + wx1*self.FrameCalibratedShift[3,:,:])
			self.MyLog("WeightCompleted","")
		elif shiftX>=0 and shiftY<0:
			#~ self.FrameCalibrated[-shiftY:1024,0:(1024-shiftX)] = self.FrameCalibrated[0:(1024+shiftY),shiftX:]
			
			shiftX0 = int(shiftX)
			shiftX1 = shiftX0 + 1
			shiftY1 = int(shiftY)
			shiftY0 = shiftY1 - 1
			wx0 = shiftX1-shiftX
			wx1 = 1-wx0
			wy0 = shiftY1-shiftY
			wy1 = 1-wy0
			self.MyLog("wx0="+str(wx0),"wx1="+str(wx1))
			self.MyLog("wy0="+str(wy0),"wy1="+str(wy1))
			self.FrameCalibratedShift[0,-shiftY0:1024,0:(1024-shiftX0)] = self.FrameCalibrated[0:(1024+shiftY0),shiftX0:]
			self.FrameCalibratedShift[1,-shiftY0:1024,0:(1024-shiftX1)] = self.FrameCalibrated[0:(1024+shiftY0),shiftX1:]
			self.FrameCalibratedShift[2,-shiftY1:1024,0:(1024-shiftX0)] = self.FrameCalibrated[0:(1024+shiftY1),shiftX0:]
			self.FrameCalibratedShift[3,-shiftY1:1024,0:(1024-shiftX1)] = self.FrameCalibrated[0:(1024+shiftY1),shiftX1:]
			self.MyLog('case=','elif shiftX>0 and shiftY<0:')
			self.FrameCalibrated[:,:] = wy0*(wx0*self.FrameCalibratedShift[0,:,:] + wx1*self.FrameCalibratedShift[1,:,:]) + wy1*(wx0*self.FrameCalibratedShift[2,:,:] + wx1*self.FrameCalibratedShift[3,:,:])
			self.MyLog("WeightCompleted","")
		elif shiftX<0 and shiftY>=0:
			#~ self.FrameCalibrated[0:(1024-shiftY),-shiftX:1024] = self.FrameCalibrated[shiftY:,0:(1024+shiftX)]
			
			shiftX1 = int(shiftX)
			shiftX0 = shiftX1 - 1
			shiftY0 = int(shiftY)
			shiftY1 = shiftY0 + 1
			wx0 = shiftX1-shiftX
			wx1 = 1-wx0
			wy0 = shiftY1-shiftY
			wy1 = 1-wy0
			self.MyLog("wx0="+str(wx0),"wx1="+str(wx1))
			self.MyLog("wy0="+str(wy0),"wy1="+str(wy1))
			self.FrameCalibratedShift[0,0:(1024-shiftY0),-shiftX0:1024] = self.FrameCalibrated[shiftY0:,0:(1024+shiftX0)]
			self.FrameCalibratedShift[1,0:(1024-shiftY0),-shiftX1:1024] = self.FrameCalibrated[shiftY0:,0:(1024+shiftX1)]
			self.FrameCalibratedShift[2,0:(1024-shiftY1),-shiftX0:1024] = self.FrameCalibrated[shiftY1:,0:(1024+shiftX0)]
			self.FrameCalibratedShift[3,0:(1024-shiftY1),-shiftX1:1024] = self.FrameCalibrated[shiftY1:,0:(1024+shiftX1)]
			self.MyLog('case=','elif shiftX<0 and shiftY>0:')
			self.FrameCalibrated[:,:] = wy0*(wx0*self.FrameCalibratedShift[0,:,:] + wx1*self.FrameCalibratedShift[1,:,:]) + wy1*(wx0*self.FrameCalibratedShift[2,:,:] + wx1*self.FrameCalibratedShift[3,:,:])
			self.MyLog("WeightCompleted","")
		else:
			self.MyLog("CalibrateFrame","else")

		t6 = time.clock()
		#Pixel binning 4x4
		self.BinArray3D[0,:,:] = self.FrameCalibrated[:,:] 
		self.BinArray3D[1,:,0:1023] = self.FrameCalibrated[:,1:1024]		
		self.BinArray3D[2,0:1023,:] = self.FrameCalibrated[1:1024,:]
		self.BinArray3D[3,0:1023,0:1023] = self.FrameCalibrated[1:1024,1:1024]
		
		self.FrameCalibrated = np.average(self.BinArray3D,axis=0)
	#	self.FrameCalibrated = np.average(self.BinArray3D,axis=0)
		#self.BinArray3D.sort(axis=0)
		#self.FrameCalibrated[:,:]=0.5*(self.BinArray3D[1,:,:] + self.BinArray3D[2,:,:]) 
		#self.FrameCalibrated = np.median(self.BinArray3D,axis=0)
		#test = np.mean(self.BinArray3D,axis=0)		
		t7 = time.clock()
		
		self.FrameCalibratedBinned[:,:] = self.FrameCalibrated[0:1024:2,0:1024:2]
		#self.FrameCalibratedBinned = self.FrameCalibratedBinned.astype(np.float32) #512x512 float32
		#self.FrameCalibratedBinned.tofile(os.path.join(self.SettingsObj.ROOTPATH,"BinnedArray.raw"))
		#print time.clock()-t1
		
		#self.MyLog("CalibrateFrame:Max3",str(np.max(self.FrameCalibratedBinned)))	
		
		t8 = time.clock()
		
		self.FrameCalibratedBinned[self.FrameCalibratedBinned < 0] = 0
		#~ self.FrameCalibratedBinned = scipy.signal.medfilt2d(self.FrameCalibratedBinned)
		#Spatial Median filter 3x3
		#~ self.MedianArray3D[0,1:511,1:511] = self.FrameCalibratedBinned[0:510,0:510]
		#~ self.MedianArray3D[1,1:511,1:511] = self.FrameCalibratedBinned[0:510,1:511]
		#~ self.MedianArray3D[2,1:511,1:511] = self.FrameCalibratedBinned[0:510,2:512]

		#~ self.MedianArray3D[3,1:511,1:511] = self.FrameCalibratedBinned[1:511,0:510]
		#~ self.MedianArray3D[4,1:511,1:511] = self.FrameCalibratedBinned[1:511,1:511]
		#~ self.MedianArray3D[5,1:511,1:511] = self.FrameCalibratedBinned[1:511,2:512]

		#~ self.MedianArray3D[6,1:511,1:511] = self.FrameCalibratedBinned[2:512,0:510]
		#~ self.MedianArray3D[7,1:511,1:511] = self.FrameCalibratedBinned[2:512,1:511]
		#~ self.MedianArray3D[8,1:511,1:511] = self.FrameCalibratedBinned[2:512,2:512]
		#~ self.MedianArray3D.sort(axis=0)
		#~ self.FrameCalibratedBinned[:,:] = self.MedianArray3D[4,:,:]

		
		
		#self.FrameCalibratedBinned.tofile(os.path.join(self.SettingsObj.ROOTPATH,"BinnedArray.raw"))
		
		self.FrameCalibratedBinned*=(255.0/np.amax(self.FrameCalibratedBinned))
		#self.FrameCalibratedBinned = np.rot90(self.FrameCalibratedBinned,1)
		self.FrameCalibratedBinned = np.transpose(self.FrameCalibratedBinned)
		
		self.FrameDisplayed[:,:] = self.FrameCalibratedBinned[:,:]
		#self.MyLog("CalibrateFrame:Max4",str(np.max(self.FrameDisplayed)))	
		#self.MyLog("CalibrateFrame:Min4",str(np.min(self.FrameDisplayed)))	
		
		t9 = time.clock()
	
		if self.SettingsObj.SAVERAW==True:
			fname = str(self.ImCount) + "_" + str(thisGantryAngleDict[ROIs[0]]) + ".raw"
			self.FrameDisplayed.tofile(os.path.join(self.SettingsObj.ROOTPATH,"SaveRaw",fname))
			#self.FrameCalibratedBinned.tofile(os.path.join(self.SettingsObj.ROOTPATH,fname))
			
		self.ImGantryAngleDict = thisGantryAngleDict
		self.ImCount = self.ImCount + 1
		self.MyLog("CalibrateFrame Completed in ",str(time.clock()-t1)+" seconds")
		self.MyLog("CalibrateFrame:self.ImCount",str(self.ImCount))
		#print time.clock()-t1
		#~ self.MyLog("CalibrateFrame:t2-t1",str(t2-t1))
		#~ self.MyLog("CalibrateFrame:t3-t1",str(t3-t1))
		#~ self.MyLog("CalibrateFrame:t4-t1",str(t4-t1))
		#~ self.MyLog("CalibrateFrame:t5-t1",str(t5-t1))
		#~ self.MyLog("CalibrateFrame:t6-t1",str(t6-t1))
		#~ self.MyLog("CalibrateFrame:t7-t1",str(t7-t1))
		#~ self.MyLog("CalibrateFrame:t8-t1",str(t8-t1))
		#~ self.MyLog("CalibrateFrame:t9-t1",str(t9-t1))
#============================================================================================================================================================
if __name__ == "__main__":
	S= Settings.Settings()
	A = Calibration(S)
	BGList = list()
	thisFilePath = os.path.join('C:\EPID\\2030-11-26_18-26-21\image','acq00000.bin')
	BGList.append(thisFilePath)
	thisFilePath = os.path.join('C:\EPID\\2030-11-26_18-26-21\image','acq00001.bin')
	BGList.append(thisFilePath)
	thisFilePath = os.path.join('C:\EPID\\2030-11-26_18-26-21\image','acq00002.bin')
	BGList.append(thisFilePath)
	A.DefineBackgroundImage(BGList)#~ thisFilePath = os.path.join('C:\E
	
	thisFilePath = os.path.join('C:\EPID\\2030-11-26_18-26-21\image','acq00101.bin')
	A.CalibrateFrame(thisFilePath,"6MV",10.0)