# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import Settings
import os,os.path,sys
import numpy as np
import pyautogui
import threading
import time
from datetime import datetime
import shutil
import subprocess
from multiprocessing import Pool
import matplotlib
matplotlib.use('WXAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure

import Mod_AcquisitionManager
import Mod_Calibration
import Mod_IcomManager
import Mod_FlexmapImage
import Mod_ViewManager

#==========================================================================================================================================================================================================
class MyFrame1 ( wx.Frame ):
	
	def __init__( self, parent,settingsObj ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = "CINE-MV SERVICE APPLICATION", pos = wx.DefaultPosition, size = wx.Size( 810,800 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.settingsObj = settingsObj
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		MyPanel1(parent = self,settingsObj = self.settingsObj)
		self.Bind(wx.EVT_CLOSE,self.OnFrameClose)
		
		self.Centre( wx.BOTH )
		self.Show(True)
	
	def __del__( self ):
		pyautogui.press('f18')
		pass
	
	def OnFrameClose(self,e):
		pyautogui.press('f18')
		time.sleep(1)
		pyautogui.press('f18')
		
	
		if self.settingsObj.debugLvl < 2 :
			folder = os.path.join(self.settingsObj.ROOTPATH,"EPID_Listening")
			for the_file in os.listdir(folder):
				file_path = os.path.join(folder, the_file)
				try:
					if os.path.isfile(file_path):
						os.unlink(file_path)
					elif os.path.isdir(file_path): shutil.rmtree(file_path)
				except Exception as e:
					print(e)
				
		self.Destroy()

###########################################################################
## Class MyPanel1
###########################################################################

class MyPanel1 ( wx.Panel ):
	
	def __init__( self, parent,settingsObj ):
		
		self.settingsObj = settingsObj
		self.ClearLogs()

		self.AcquisitionManagerObj = Mod_AcquisitionManager.AcquisitionManager(self.settingsObj) #Define t=0 for new image files. Fetch active calibration
		
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 810,800 ), style = wx.TAB_TRAVERSAL )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		
		bSizer1.AddSpacer(0)
		
		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )
		
		
		bSizer2.AddSpacer(0)
		
		bSizer5 = wx.BoxSizer( wx.VERTICAL )
		
		
		bSizer5.AddSpacer(0)
		
		self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"GAIN CALIBRATION", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )
		self.m_staticText1.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, True, wx.EmptyString ) )
		
		bSizer5.Add( self.m_staticText1, 0, wx.ALL, 5 )
		
		
		bSizer5.AddSpacer(0)
		
		self.GainCalibListCtrl = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,style = wx.LC_REPORT )
		self.GainCalibListCtrl.InsertColumn(0, 'Energy', width = 60) 
		self.GainCalibListCtrl.InsertColumn(1, 'Last saved date', wx.LIST_FORMAT_LEFT, 150) 
		
		for i in self.AcquisitionManagerObj.ActiveCalibrationDTList: #ActiveCalibrationDTList is a list of tuple
			index = self.GainCalibListCtrl.InsertItem(sys.maxint, i[0]) 
			self.GainCalibListCtrl.SetItem(index, 1, i[1]) 

		bSizer5.Add( self.GainCalibListCtrl, 0, wx.ALL, 5 )
		
		bSizer5.AddSpacer(0)
		
		bSizer6 = wx.BoxSizer( wx.HORIZONTAL )
		
		
		bSizer6.AddSpacer(0)
		
		self.BackgroundButton1 = wx.Button( self, 1, u"BACKGROUND", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer6.Add( self.BackgroundButton1, 0, wx.ALL, 5 )
		
		
		bSizer6.AddSpacer(0)
		
		self.StartButton1 = wx.Button( self, wx.ID_ANY, u"START", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.StartButton1.Disable()
		bSizer6.Add( self.StartButton1, 0, wx.ALL, 5 )
		
		
		bSizer6.AddSpacer(0)
		
		self.StopButton1 = wx.Button( self, wx.ID_ANY, u"STOP", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.StopButton1.Disable()
		bSizer6.Add( self.StopButton1, 0, wx.ALL, 5 )
		
		
		bSizer5.Add( bSizer6, 1, wx.EXPAND, 5 )
		
		
		bSizer2.Add( bSizer5, 1, wx.EXPAND, 5 )
		
		
		bSizer2.AddSpacer(0)
		
		
		bSizer1.Add( bSizer2, 1, wx.EXPAND, 5 )
		
		
		bSizer1.AddSpacer(0)
		
		self.m_staticline1 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		self.m_staticline1.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		
		bSizer1.Add( self.m_staticline1, 0, wx.EXPAND |wx.ALL, 5 )
		
		
		bSizer1.AddSpacer(0)
		
		bSizer9 = wx.BoxSizer( wx.HORIZONTAL )
		
		
		bSizer9.AddSpacer(0)
		
		bSizer10 = wx.BoxSizer( wx.VERTICAL )
		
		
		bSizer10.AddSpacer(0)
		
		self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"PANEL SAG CALIBRATION", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )
		self.m_staticText2.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, True, wx.EmptyString ) )
		
		bSizer10.Add( self.m_staticText2, 0, wx.ALL, 5 )
		
		
		bSizer10.AddSpacer(0)
		
		self.SagCalibListCtrl = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,style = wx.LC_REPORT )
		self.SagCalibListCtrl.InsertColumn(0, 'Last saved date', wx.LIST_FORMAT_LEFT, 150) 	
		if self.AcquisitionManagerObj.FlexmapDT is not None:
			self.SagCalibListCtrl.InsertItem(sys.maxint,self.AcquisitionManagerObj.FlexmapDT)

		self.SagCalibListCtrl.SetMinSize((150,100))
		self.SagCalibListCtrl.SetMaxSize((150,100))
		bSizer10.Add(self.SagCalibListCtrl, 0, wx.ALL, 5 )
		
		
		bSizer10.AddSpacer(0)
		
		self.BackgroundButton2 = wx.Button( self, 2, u"BACKGROUND", wx.DefaultPosition, wx.DefaultSize, 0 )
		#self.BackgroundButton2.Disable()
		bSizer10.Add( self.BackgroundButton2, 0, wx.ALL, 5 )
		
		
		bSizer10.AddSpacer(0)
		
		self.StartButton2 = wx.Button( self, wx.ID_ANY, u"START", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.StartButton2.Disable()
		bSizer10.Add( self.StartButton2, 0, wx.ALL, 5 )
		
		
		bSizer10.AddSpacer(0)
		
		self.StopButton2 = wx.Button( self, wx.ID_ANY, u"STOP", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.StopButton2.Disable()
		bSizer10.Add( self.StopButton2, 0, wx.ALL, 5 )
		
		
		bSizer10.AddSpacer(0)
		
		
		bSizer9.Add( bSizer10, 1, wx.EXPAND, 5 )
		
		
		bSizer9.AddSpacer(0)
		
		sbSizer1 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, wx.EmptyString ), wx.VERTICAL )
		sbSizer1.SetMinSize( wx.Size( 300,300 ) ) 
		
		sbSizer1.AddSpacer(0)
		
		self.m_bitmap2 = wx.StaticBitmap( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_bitmap2.SetMinSize( wx.Size( 300,300 ) )
		
		self.Figure_CNN = Figure(figsize=(5,4))
		self.FigureAxes_CNN = self.Figure_CNN.add_subplot(111)
		self.FigureAxes_CNN.plot(self.AcquisitionManagerObj.GantryList,self.AcquisitionManagerObj.YIsoList,'k',label='Crossline')
		self.FigureAxes_CNN.plot(self.AcquisitionManagerObj.GantryList,self.AcquisitionManagerObj.XIsoList,'r',label='Inline')
		self.FigureAxes_CNN.set_xlabel("GANTRY ANGLE")
		self.FigureAxes_CNN.set_ylabel("BB POSITION (Pixels)")
		self.FigureAxes_CNN.legend()
		self.FigureAxes_CNN.grid(True,which='both',axis='both',linestyle='--',color='lightgrey')
		
		self.FigureCanvas_CNN = FigureCanvas(sbSizer1.GetStaticBox(), -1, self.Figure_CNN)
		sbSizer1.Add(self.FigureCanvas_CNN, 0, wx.ALL, 5 )

		self.FigureToolbar_CNN = NavigationToolbar2Wx(self.FigureCanvas_CNN)
		self.FigureToolbar_CNN.Realize()
		sbSizer1.Add(self.FigureToolbar_CNN, 0, wx.LEFT | wx.EXPAND)
		self.FigureToolbar_CNN.update()
		
		sbSizer1.Add( self.m_bitmap2, 0, wx.ALL, 5 )
		
		
		sbSizer1.AddSpacer(0)
		
		
		bSizer9.Add( sbSizer1, 1, wx.EXPAND, 5 )
		
		
		bSizer9.AddSpacer(0)
		
		
		bSizer1.Add( bSizer9, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		
		# Connect Events
		self.BackgroundButton1.Bind( wx.EVT_BUTTON, self.OnRefreshBackground )
		self.StartButton1.Bind( wx.EVT_BUTTON, self.OnStartGainCalibration )
		self.StopButton1.Bind( wx.EVT_BUTTON, self.OnStopGainCalibration )
		self.BackgroundButton2.Bind( wx.EVT_BUTTON, self.OnRefreshBackground )
		self.StartButton2.Bind( wx.EVT_BUTTON, self.OnStartSagCalibration )
		self.StopButton2.Bind( wx.EVT_BUTTON, self.OnStopSagCalibration )

		#self.SagCalibListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED,self.OnSagListSelection)


		if self.settingsObj.debugLvl!=2079:
			self.StartPyComView()

	def __del__( self ):
		pass
#--------------------------------------------------------------------------------------------------------------------------------------------------
	#~ def OnSagListSelection(self,evt):
		#~ print(evt.GetIndex())
		#~ for k in range(0,3):
			#~ print(self.SagCalibListCtrl.IsSelected(k))
#---------------------------------------------------------------------------------------------------------------------------------------------------
	def UpdateFlexmapPlot(self):
		
		if len(self.CalibObj.GantryAngleList)>5:
			try:
				self.FigureAxes_CNN.clear()
				self.FigureAxes_CNN.plot(self.CalibObj.GantryAngleList,self.CalibObj.YIsoList,'k',label='Crossline')
				self.FigureAxes_CNN.plot(self.CalibObj.GantryAngleList,self.CalibObj.XIsoList,'r',label='Inline')
				self.FigureAxes_CNN.set_xlabel("GANTRY ANGLE")
				self.FigureAxes_CNN.set_ylabel("BB POSITION (Pixels)")
				self.FigureAxes_CNN.legend(loc='best')
				self.FigureAxes_CNN.grid(True,which='both',axis='both',linestyle='--',color='lightgrey')
				self.FigureCanvas_CNN.draw()
			except:
				pass
#---------------------------------------------------------------------------------------------------------------------------------------------------
	def LaunchProgressDialog(self,NbSec,mess="Background acquisition in Progress ..."): #Progress bar
		dialog = wx.ProgressDialog("Service", mess, NbSec, style=wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME | wx.PD_AUTO_HIDE ) 
		count=0
		for k in range(0,NbSec):
			count+=1
			dialog.Update(count)
			time.sleep(1)
		dialog.Destroy()
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	def OnRefreshBackground(self,evt): #DONE

		widget = evt.GetEventObject()
		#print widget.GetId()
		self.BackgroundButton1.Disable()
		self.BackgroundButton2.Disable()
			
		if widget.GetId() == 1:
			#self.BackgroundButton1.Disable()
			self.StartButton1.Disable()
			self.StopButton1.Disable()
			#self.BackgroundButton2.Disable()
		else:
			#self.BackgroundButton2.Disable()
			self.StartButton2.Disable()
			self.StopButton2.Disable()
			#self.BackgroundButton1.Disable()
			
		
		self.AcquisitionManagerObj.ResetLists()
		self.AcquisitionManagerObj.FindMostRecentMeasurementFolder()
		if self.AcquisitionManagerObj.MeasurementFolderPath is not None:
			thisViewObj = Mod_ViewManager.ViewManager(self.AcquisitionManagerObj.MeasurementFolderPath,self.settingsObj)
			self.AcquisitionManagerObj.ImageFilePathListBefore = list(thisViewObj.FrameFilePathList) #list() mean thisList.copy()
		
		pyautogui.press('f16') #Start acquisition trigger
		self.LaunchProgressDialog(5)
		pyautogui.press('f17') #Pause acquisition
		
		self.AcquisitionManagerObj.FindMostRecentMeasurementFolder()
		if self.AcquisitionManagerObj.MeasurementFolderPath is not None:
			thisViewObj = Mod_ViewManager.ViewManager(self.AcquisitionManagerObj.MeasurementFolderPath,self.settingsObj)
			self.AcquisitionManagerObj.ImageFilePathListAfter = list(thisViewObj.FrameFilePathList) #list() mean thisList.copy()
			rtn = self.AcquisitionManagerObj.FindNewImages(list(thisViewObj.TimeStampList),NbMin=3)
			if rtn == True:
				self.AcquisitionManagerObj.DefineBackgroundFiles()
				if widget.GetId() == 1:
					self.StartButton1.Enable()
				else:
					self.StartButton2.Enable()
			else:
				self.MyLog("OnRefreshSagBackground","self.AcquisitionManagerObj.FindNewImages return False",level=0)
				wx.MessageBox('Background Failed. PLEASE RETRY', 'INFORMATION BACKGROUND',wx.OK | wx.ICON_INFORMATION)
		else:
			self.MyLog("OnRefreshSagBackground","self.AcquisitionManagerObj.FindMostRecentMeasurementFolder() return None",level=0)
		
		self.BackgroundButton1.Enable()
		self.BackgroundButton2.Enable()

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	def OnStartGainCalibration(self,evt):
		self.BackgroundButton1.Disable()
		self.StartButton1.Disable()
		self.StopButton1.Enable()
		
		self.AcquisitionManagerObj.ResetLists()
		self.AcquisitionManagerObj.FindMostRecentMeasurementFolder()
		if self.AcquisitionManagerObj.MeasurementFolderPath is not None:			
			thisViewObj = Mod_ViewManager.ViewManager(self.AcquisitionManagerObj.MeasurementFolderPath,self.settingsObj)
			self.AcquisitionManagerObj.ImageFilePathListBefore = list(thisViewObj.FrameFilePathList) #list() mean thisList.copy()
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	def OnStopGainCalibration(self,evt):
		self.StopButton1.Disable()
		
		self.AcquisitionManagerObj.FindMostRecentMeasurementFolder()
		if self.AcquisitionManagerObj.MeasurementFolderPath is not None:
			
			thisViewObj = Mod_ViewManager.ViewManager(self.AcquisitionManagerObj.MeasurementFolderPath,self.settingsObj)
			self.AcquisitionManagerObj.ImageFilePathListAfter = list(thisViewObj.FrameFilePathList) #list() mean thisList.copy()
			rtn = self.AcquisitionManagerObj.FindNewImages(list(thisViewObj.TimeStampList),NbMin=5)
			
			if rtn == True:
			
				self.IcomObj = Mod_IcomManager.IcomManager(self.AcquisitionManagerObj.MeasurementFolderPath, self.settingsObj)
				self.IcomObj.FetchInfo(np.min(self.AcquisitionManagerObj.NewImageTSList),np.max(self.AcquisitionManagerObj.NewImageTSList))

				self.CalibObj = Mod_Calibration.Calibration(self.settingsObj)
				self.CalibObj.DefineBackground(self.AcquisitionManagerObj.BackgroundFilePathList)
				
				thisEnergy = None
				thisDRList = list()
				DRFilePathDict = dict()
				for beamseg in self.IcomObj.BeamNameSegIDSet: #beamseg is a tuple(BeamName,SegID)
						rtn = self.IcomObj.GetSegmentTimeLimits(beamseg[0],beamseg[1]) #return True, np.min(thisTimeStampList), np.max(thisTimeStampList),np.median(thisDRList),thisEnergy
						if rtn[0]==True:
							rtn2 = thisViewObj.GetFrameFilePathList(rtn[1],rtn[2])
							DRFilePathDict[rtn[3]] = rtn2
							thisDRList.append(rtn[3])
							thisEnergy = rtn[4]
				thisDRList.sort()

				#Create a temporary folder in the ROOTPATH
				if os.path.isdir(os.path.join(self.settingsObj.ROOTPATH,thisEnergy)) == True:
					try:
						shutil.rmtree(os.path.join(self.SettingsObj.ROOTPATH,thisEnergy))
					except:
						pass
				os.mkdir(os.path.join(self.settingsObj.ROOTPATH,thisEnergy))
				
				self.CalibObj.MLG = np.zeros((len(thisDRList),1024,1024),np.float32)
				for dr in thisDRList:
					self.CalibObj.GetLevelTemporalMedian(DRFilePathDict[dr],dr,thisEnergy) #background substraction is also performed
				self.CalibObj.LMSRegression(thisEnergy)
				f=open(os.path.join(self.settingsObj.ROOTPATH,thisEnergy,"Files.Calib"),"w")
				for dr in thisDRList:
					f.write("DR"+str(int(dr))+".raw\n")
				f.close()
				self.CalibObj.CommitGainCalibration(thisEnergy)
				
				#Refresh the available Gain calibration
				self.AcquisitionManagerObj.GetActiveCalibrations() 
				self.GainCalibListCtrl.DeleteAllItems()
				for i in self.AcquisitionManagerObj.ActiveCalibrationDTList: #ActiveCalibrationDTList is a list of tuple
					index = self.GainCalibListCtrl.InsertItem(sys.maxint, i[0]) 
					self.GainCalibListCtrl.SetItem(index, 1, i[1]) 
					
		self.BackgroundButton1.Enable()
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	def OnStartSagCalibration(self,evt):
		self.BackgroundButton2.Disable()
		self.StartButton2.Disable()
		self.StopButton2.Enable()
		
		self.AcquisitionManagerObj.ResetLists()
		self.AcquisitionManagerObj.FindMostRecentMeasurementFolder()
		if self.AcquisitionManagerObj.MeasurementFolderPath is not None:
			thisViewObj = Mod_ViewManager.ViewManager(self.AcquisitionManagerObj.MeasurementFolderPath,self.settingsObj)
			self.AcquisitionManagerObj.ImageFilePathListBefore = list(thisViewObj.FrameFilePathList) #list() mean thisList.copy()
		self.MyLog("OnStartSagCalibration:self.AcquisitionManagerObj.ImageFilePathListBefore[-1]",self.AcquisitionManagerObj.ImageFilePathListBefore[-1],level=2)
		self.MyLog("OnStartSagCalibration:len(self.AcquisitionManagerObj.ImageFilePathListBefore)",str(len(self.AcquisitionManagerObj.ImageFilePathListBefore)),level=2)
		self.AcquisitionManagerObj.State = "Acquisition"
		self.StartSagMonitoring()

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	def OnStopSagCalibration(self,evt):
		self.AcquisitionManagerObj.State = None
		self.BackgroundButton2.Enable()
		self.StartButton2.Enable()
		self.StopButton2.Disable()
		#~ self.AcquisitionManagerObj.CalibState = False
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	def StartSagMonitoring(self):
		
		def SagMonitoring():
			self.AcquisitionManagerObj.FindMostRecentMeasurementFolder()
			thisViewObj = Mod_ViewManager.ViewManager(self.AcquisitionManagerObj.MeasurementFolderPath,self.settingsObj)
			self.AcquisitionManagerObj.ImageFilePathListAfter = list(thisViewObj.FrameFilePathList)
			rtn = self.AcquisitionManagerObj.FindNewImages(list(thisViewObj.TimeStampList))

			if rtn == True:

				if self.IcomObj==None:
					self.ti =time.clock()
					self.IcomObj = Mod_IcomManager.IcomManager(self.AcquisitionManagerObj.MeasurementFolderPath,self.settingsObj)	
					
				if np.max(self.AcquisitionManagerObj.NewImageTSList)>self.IcomObj.TimeStampMax:
					time.sleep(2)
					self.IcomObj.Update()
					
				incr =0
				for im in self.AcquisitionManagerObj.NewImageFilePathList:
					rtn2 = self.IcomObj.GetFrameInfo(self.AcquisitionManagerObj.NewImageTSList[incr]) #rtn2[0] = boolean, rtn2[1] = index des listes Icom.
					if rtn2[0]==True:						
						if self.LastEnergy==None:
							self.CalibObj.LoadFiles(os.path.join(self.settingsObj.ROOTPATH,'CalibrationFiles',self.IcomObj.EnergyList[rtn2[1]]))
							self.CalibObj.DefineBackground(self.AcquisitionManagerObj.BackgroundFilePathList)
							self.LastEnergy = self.IcomObj.EnergyList[rtn2[1]]

						if self.IcomObj.DoseRateList[rtn2[1]]>350 and abs(self.IcomObj.GantryAngleList[rtn2[1]])<180.0:
							OverRotation = False
							if len(self.CalibObj.GantryAngleList)>0 and abs(self.IcomObj.GantryAngleList[rtn2[1]]-self.CalibObj.GantryAngleList[-1])>50:
								OverRotation = True
							if OverRotation == False:
								self.CalibObj.CalibrateFrame(im)
								bbx,bby = self.FlexmapObj.Execute(self.CalibObj.FrameCalibrated)
								self.CalibObj.GantryAngleList.append(self.IcomObj.GantryAngleList[rtn2[1]])
								self.CalibObj.YIsoList.append(bby)
								self.CalibObj.XIsoList.append(bbx)

						if incr % 10==0:
							self.UpdateFlexmapPlot()
					incr = incr +1

				self.AcquisitionManagerObj.ImageFilePathListBefore = self.AcquisitionManagerObj.ImageFilePathListBefore + self.AcquisitionManagerObj.NewImageFilePathList
				self.AcquisitionManagerObj.NewImageFilePathList = list()
				self.AcquisitionManagerObj.NewImageTSList = list()
		
		def launchMonitoring():
			self.IcomObj = None
			self.LastEnergy = None
			self.CalibObj = Mod_Calibration.Calibration(self.settingsObj)
			self.CalibObj.InitNewFlexmap() #Reset GantryList, YIsoList,XIsoList
			self.FlexmapObj = Mod_FlexmapImage.FlexmapImage(self.settingsObj)
			self.ti = None
			self.tf = None

			while self.AcquisitionManagerObj.State == "Acquisition":
				time.sleep(0.5)
				#print "Sag Monitoring ..."
				SagMonitoring()
				self.UpdateFlexmapPlot()

			SagMonitoring()
			rnt = self.CalibObj.CommitFlexmap()
			self.AcquisitionManagerObj.GetActiveCalibrations()
			self.SagCalibListCtrl.DeleteAllItems()
			if self.AcquisitionManagerObj.FlexmapDT is not None:
				self.SagCalibListCtrl.InsertItem(sys.maxint,self.AcquisitionManagerObj.FlexmapDT)
			self.SagCalibListCtrl.SetMaxSize((150,50))
			self.tf=time.clock()
			#print "End of Sag Acquisition"
			#print self.tf-self.ti

		#self.MyLog('StartSagMonitoring','Just before:tl = threading.Thread(target = launchMonitoring)')
		tl = threading.Thread(target = launchMonitoring)
		tl.start()

#---------------------------------------------------------------------------------------------------------------------------------------------------
	def StartPyComView(self):

		def launch():
			try:
				os.chdir(os.path.join(self.settingsObj.ROOTPATH,"PyComView","dist"))
				if (self.settingsObj.debugLvl>0):
					subprocess.call("main.exe")
				else:
					CREATE_NO_WINDOW = 0x08000000
					subprocess.call("main.exe",creationflags=CREATE_NO_WINDOW)
				
				#os.chdir(os.path.join(self.settingsObj.ROOTPATH,"EPID_Fluoroscopie","dist"))
				
			except:
				pass

				
		tl = threading.Thread(target = launch)
		tl.start()
		
		self.LaunchProgressDialog(5,mess="Starting PyComView ....")
		self.BackgroundButton1.Enable()
#--------------------------------------------------------------------------------------------------------------
	def MyLog(self,mess="none",value="none",level=0):
		if level<=self.settingsObj.debugLvl:
			f = open(os.path.join(self.settingsObj.ROOTPATH,"Logs","Service.log"),"a")
			f.write(str(mess)+"\t"+str(value)+"\t"+str(datetime.now())+"\n")
			f.close()
#---------------------------------------------------------------------------------------------------------------------------------------------------
	def ClearLogs(self):
		try:
			os.remove(os.path.join(self.settingsObj.ROOTPATH,"Logs","Service.log"))
		except:
			pass
		try:
			os.remove(os.path.join(self.settingsObj.ROOTPATH,"Logs","Mod_IcomManager.log"))
		except:
			pass
		try:
			os.remove(os.path.join(self.settingsObj.ROOTPATH,"Logs","Mod_Calibration.log"))
		except:
			pass

#===============================================================================================================================================        
class RunApp(wx.App):
	def __init__(self):
		wx.App.__init__(self, redirect=False)
		

	def OnInit(self):
		S = Settings.Settings()
		self.frame = MyFrame1(parent = None,settingsObj = S)
		self.SetTopWindow(self.frame)
		return True

#===================================================================================================================
if __name__ == "__main__":
	app = RunApp()
	app.MainLoop()

	

