# -*- coding: utf-8 -*- 

import sys
sys.path += ['.'] #For OpenGL

import wx
from wx import glcanvas
import os,os.path
import numpy as np
import pyautogui
import threading
import time
from datetime import datetime
import pickle

#~ from matplotlib import pyplot as plt
import shutil
import subprocess
#~ import PIL
#~ import PIL.Image
from PIL import Image


from ctypes import util
import OpenGL.GL


import Module_Controller
import Settings
import Mod_AcquisitionManager
###########################################################################
## Class MyFrame1
###########################################################################
class MyFrame1 ( wx.Frame ):
	
	def __init__( self, parent,DebugLvl,settingsObj ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = "FLUO-MV CLINICAL APPLICATION", pos = wx.DefaultPosition, size = wx.Size( 900,800 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		self.DebugLvl = DebugLvl
		self.ClearLogs()
		self.SettingsObj = settingsObj
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		self.PanelObj = MyPanel1(parent = self,DebugLvl=self.DebugLvl,settingsObj = self.SettingsObj)
		
		self.Bind(wx.EVT_CLOSE,self.OnFrameClose)
		
		self.Centre( wx.BOTH )
		self.Show(True)
	
	def __del__( self ):
		pyautogui.press('f18')
		self.MyLog("__del__","called")
		pass
	
	
	def OnFrameClose(self,e):
		self.PanelObj.CopyImages()
		self.MyLog("OnFrameClose","called")
		pyautogui.press('f18')
		time.sleep(1)
		pyautogui.press('f18')
		
		if self.DebugLvl != 2079:
			folder = os.path.join(self.SettingsObj.ROOTPATH,"EPID_Listening")
			for the_file in os.listdir(folder):
				file_path = os.path.join(folder, the_file)
				try:
					os.removedirs(file_path)
				except:
					pass
				try:
					if os.path.isfile(file_path):
						os.unlink(file_path)
					elif os.path.isdir(file_path): shutil.rmtree(file_path)
				except Exception as e:
					print(e)
				
		self.Destroy()
#--------------------------------------------------------------------------------------------------------------------------------------------
	def ClearLogs(self):
		try:
			os.remove(os.path.join(self.SettingsObj.ROOTPATH,"Logs","Frame.log"))
		except:
			pass
#--------------------------------------------------------------------------------------------------------------------------------------------
	def MyLog(self,mess="none",value="none",level=0):
		if level<=self.SettingsObj.debugLvl:
			f = open(os.path.join(self.SettingsObj.ROOTPATH,"Logs","Frame.log"),"a")
			f.write(str(mess)+"\t"+str(value)+"\t"+str(datetime.now())+"\n")
			f.close()
#----------------------------------------------------------------------------------------------------------------------------------------------------		

###########################################################################
## Class MyPanel1
###########################################################################
class MyPanel1 ( wx.Panel ):
	
	def __init__( self, parent, DebugLvl, settingsObj ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 900,800 ), style = wx.TAB_TRAVERSAL )
		self.SettingsObj = settingsObj		
		self.ClearImages()
		self.ClearLogs()

		self.DebugLvl = DebugLvl

		self.CurrentPatientID = 'none'
		self.PrescriptionList = list()
		self.Threshold = 175
		self.DisplayedImCount = 0
		self.TimeTravelActivated = False
		self.PNGFileList = list()
		self.PNGIndex = None

	
		self.Controller = Module_Controller.Controller(self.SettingsObj)
		self.AcquisitionManagerObj = Mod_AcquisitionManager.AcquisitionManager(self.SettingsObj)
		
		bSizer1 = wx.BoxSizer( wx.HORIZONTAL )

		bSizer1.AddSpacer(15)
		
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		
		
		bSizer2.AddSpacer(15)
		
		bSizer3 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_textCtrl1 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		#~ self.m_textCtrl1.write("Deliver Stored Beam")
		self.m_textCtrl1.write("ID")
		bSizer3.Add( self.m_textCtrl1, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		#~ self.m_button1 = wx.Button( self, wx.ID_ANY, u"SEARCH", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_button1 = wx.Button( self, wx.ID_ANY, u"SEARCH", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_button1.Bind(wx.EVT_BUTTON,self.SearchPatient)
		bSizer3.Add( self.m_button1, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		
		bSizer2.Add( bSizer3, 1, wx.EXPAND, 5 )
		
		
		bSizer2.AddSpacer(15)
		
		#~ self.PrescriptionList = []
		self.m_choice1 = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, self.PrescriptionList, 0 )
		self.m_choice1.SetSelection( 0 )
		self.m_choice1.SetMinSize( wx.Size( 225,-1 ) )
		self.m_choice1.Bind(wx.EVT_CHOICE,self.PrescriptionChoice)
		
		bSizer2.Add( self.m_choice1, 0, wx.ALIGN_LEFT, 5 )
		
		
		bSizer2.AddSpacer(15)
		
		self.m_button2 = wx.Button( self, wx.ID_ANY, u"BACKGROUND", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_button2.Disable()
		bSizer2.Add( self.m_button2, 0, wx.ALIGN_LEFT, 5 )
		self.m_button2.Bind(wx.EVT_BUTTON,self.OnRefreshBackground)
		
		
		bSizer2.AddSpacer(15)
		
		
		bSizer2.AddSpacer(15)
		
		m_checkList1Choices = []
		self.m_checkList1 = wx.CheckListBox( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_checkList1Choices, 0 )
		bSizer2.Add( self.m_checkList1, 0, wx.ALL, 5 )
		
		
		bSizer1.Add( bSizer2, 1, wx.ALIGN_TOP, 5 )
		
		
		bSizer1.AddSpacer(15)
		
		bSizer5 = wx.BoxSizer( wx.VERTICAL )
		
		self.MyOpenGL = MyCanvasBase(self,self.SettingsObj)
		self.MyOpenGL.SetMinSize((512,512))

		self.timer = wx.Timer(self,id=-1)
		self.Bind(wx.EVT_TIMER,self.display)

		self.timer.Start(250)
		
		bSizer5.Add( self.MyOpenGL, 0, wx.ALL, 5 )
		
		bSizer5.AddSpacer(15)
		
		#~ bSizer5hZoom = wx.BoxSizer( wx.HORIZONTAL )
		#~ s = wx.Size(300,30)
		#~ self.m_sliderZoom = wx.Slider( self, wx.ID_ANY, 1,1, 5, wx.DefaultPosition, s, wx.SL_HORIZONTAL|wx.SL_AUTOTICKS ) #Level
		#~ self.m_sliderZoom.Bind(wx.EVT_SLIDER,self.OnMouseWheelV2)
		#~ bSizer5hZoom.Add( self.m_sliderZoom, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		#~ bSizer5.Add(bSizer5hZoom, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 2 )
		
		
		bSizer5h = wx.BoxSizer( wx.HORIZONTAL )

		s = wx.Size(300,30)
		self.m_slider1 = wx.Slider( self, wx.ID_ANY, self.Threshold,1, 255, wx.DefaultPosition, s, wx.SL_HORIZONTAL|wx.SL_AUTOTICKS ) #Level
		self.m_slider1.Bind(wx.EVT_SLIDER,self.OnSliderScroll)
		bSizer5h.Add( self.m_slider1, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		self.cb1 = wx.CheckBox(self,wx.ID_ANY,label="Invert")
		bSizer5h.Add( self.cb1, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.m_textCtrl2 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY|wx.TE_CENTRE)
		self.m_textCtrl2.SetMinSize( wx.Size( 100,25 ) )
		self.m_textCtrl2.SetValue(str(self.DisplayedImCount))

		bSizer5h.Add( self.m_textCtrl2, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )

		bSizer5.Add(bSizer5h, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 2 )
		
		#bSizer5.Add( self.m_slider1, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 2 )
		
		bSizer5.AddSpacer(5)
		
		bSizer4 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_button3 = wx.Button( self, wx.ID_ANY, u"START", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_button3.Disable()
		self.m_button3.Bind(wx.EVT_BUTTON,self.OnStart)
		bSizer4.Add( self.m_button3, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.m_button4 = wx.Button( self, wx.ID_ANY, u"STOP", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_button4.Disable()
		self.m_button4.Bind(wx.EVT_BUTTON,self.OnStop)
		bSizer4.Add( self.m_button4, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		
		bSizer5.Add( bSizer4, 1, wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		
		bSizer1.Add( bSizer5, 1, wx.EXPAND, 5 )
		
		
		bSizer1.AddSpacer(15)

		self.m_choice1.Disable()
		
		self.Bind(wx.EVT_MOUSEWHEEL,self.OnMouseWheel)
		
		self.SetSizer( bSizer1 )
		self.Layout()
	
#-----------------------------------------------------------------------------------------------------------------
	def OnMouseWheel(self, event=None):
		NbPNG=  len(self.PNGFileList)
		
		if self.TimeTravelActivated==True and NbPNG>5 and self.PNGIndex!=None:
			
			if event.GetWheelRotation()<0 and self.PNGIndex>0:
				self.PNGIndex += -1

			if event.GetWheelRotation()>0 and self.PNGIndex<(NbPNG-1):
				self.PNGIndex += 1

			self.m_textCtrl2.SetValue(str(self.PNGIndex+1) + "/" + str(NbPNG))
			try:
				thisIm = Image.open(self.PNGFileList[self.PNGIndex])
				self.MyOpenGL.CurrentGLIm = np.flipud(np.array(thisIm))
				self.MyOpenGL.OnIDLE()
			except:
				pass

#------------------------------------------------------------------------------------------------------------------------------------------		
	def __del__( self ):
		pyautogui.press('f18')
		pass
#--------------------------------------------------------------------------------------------------------------------------------------------
	def ClearLogs(self):
		try:
			os.remove(os.path.join(self.SettingsObj.ROOTPATH,"Logs","MyPanel.log"))
		except:
			pass
#--------------------------------------------------------------------------------------------------------------------------------------------
	def MyLog(self,mess="none",value="none",level=0):
		if level<=self.SettingsObj.debugLvl:
			f = open(os.path.join(self.SettingsObj.ROOTPATH,"Logs","MyPanel.log"),"a")
			f.write(str(mess)+"\t"+str(value)+"\t"+str(datetime.now())+"\n")
			f.close()
#-----------------------------------------------------------------------------------------------------------------------------------------------------
	def ClearImages(self):
		try:
			for r, d, f in os.walk(os.path.join(self.SettingsObj.ROOTPATH,"SavePNG")):
				for file in f:
					os.remove(os.path.join(self.SettingsObj.ROOTPATH,"SavePNG",file))
		except:
			self.MyLog("Except in ClearImages")
			pass
			
		try:
			for r, d, f in os.walk(os.path.join(self.SettingsObj.ROOTPATH,"SaveRaw")):
				for file in f:
					os.remove(os.path.join(self.SettingsObj.ROOTPATH,"SaveRaw",file))
		except:
			pass
#-----------------------------------------------------------------------------------------------------------------------------------------------------
	def CopyImages(self):
		self.MyLog("Calling CopyImages",str(self.CurrentPatientID))
		AllPNGFiles = os.listdir(os.path.join(self.SettingsObj.ROOTPATH,"SavePNG"))
		AllRAWFiles = os.listdir(os.path.join(self.SettingsObj.ROOTPATH,"SaveRaw"))

		mess = "Transfering images ..."
		Nb = len(AllPNGFiles) + len(AllRAWFiles)

		if len(AllPNGFiles)>2 or len(AllRAWFiles)>2 and self.CurrentPatientID!='none' and self.CurrentPatientID!='ID':
			
			dialog = wx.ProgressDialog("Clinical", mess, Nb, style=wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME | wx.PD_AUTO_HIDE ) 
			count = 0
			
			if os.path.isdir(os.path.join(self.SettingsObj.ROIPATH,"SavedImages"))==False:
				os.mkdir(os.path.join(self.SettingsObj.ROIPATH,"SavedImages"))
				
			if os.path.isdir(os.path.join(self.SettingsObj.ROIPATH,"SavedImages",self.CurrentPatientID))==False:
				os.mkdir(os.path.join(self.SettingsObj.ROIPATH,"SavedImages",self.CurrentPatientID))

			DT = datetime.now()
			DTTag = str(DT.year)+"-"+str(DT.month)+"-"+str(DT.day)+"_"+str(DT.hour)+"h"+str(DT.minute)+"m"+str(DT.second)+"s"

			if not os.path.isdir(os.path.join(self.SettingsObj.ROIPATH,"SavedImages",self.CurrentPatientID,DTTag)):
				os.mkdir(os.path.join(self.SettingsObj.ROIPATH,"SavedImages",self.CurrentPatientID,DTTag))

			self.MyLog("CopyImages",str(os.path.join(self.SettingsObj.ROIPATH,"SavedImages",self.CurrentPatientID,DTTag)))

			if self.SettingsObj.SAVEPNG:
				if not os.path.isdir(os.path.join(self.SettingsObj.ROIPATH,"SavedImages",self.CurrentPatientID,DTTag,"SavePNG")):
					os.mkdir(os.path.join(self.SettingsObj.ROIPATH,"SavedImages",self.CurrentPatientID,DTTag,"SavePNG"))
				try:
					for r, d, f in os.walk(os.path.join(self.SettingsObj.ROOTPATH,"SavePNG")):
						for file in f:
							shutil.copy(os.path.join(self.SettingsObj.ROOTPATH,"SavePNG",file),os.path.join(self.SettingsObj.ROIPATH,"SavedImages",self.CurrentPatientID,DTTag,"SavePNG", file))
							if os.path.isfile(os.path.join(self.SettingsObj.ROIPATH,"SavedImages",self.CurrentPatientID,DTTag,"SavePNG", file)):
								os.remove(os.path.join(self.SettingsObj.ROOTPATH,"SavePNG",file))
							count+=1
							dialog.Update(count)
				except:
					pass

			if self.SettingsObj.SAVERAW:
				if not os.path.isdir(os.path.join(self.SettingsObj.ROIPATH,"SavedImages",self.CurrentPatientID,DTTag,"SaveRaw")):
					os.mkdir(os.path.join(self.SettingsObj.ROIPATH,"SavedImages",self.CurrentPatientID,DTTag,"SaveRaw"))
				try:
					for r, d, f in os.walk(os.path.join(self.SettingsObj.ROOTPATH,"SaveRaw")):
						for file in f:
							shutil.copy(os.path.join(self.SettingsObj.ROOTPATH,"SaveRaw",file),os.path.join(self.SettingsObj.ROIPATH,"SavedImages",self.CurrentPatientID,DTTag,"SaveRaw", file))
							if os.path.isfile(os.path.join(self.SettingsObj.ROIPATH,"SavedImages",self.CurrentPatientID,DTTag,"SaveRaw", file)):
								os.remove(os.path.join(self.SettingsObj.ROOTPATH,"SaveRaw",file))
							count +=1
							dialog.Update(count)
				except:
					pass
					
			dialog.Destroy()
#-----------------------------------------------------------------------------------------------------------------------------------------------------
	def SearchPatient(self,evt):
		if self.CurrentPatientID!="none":
			self.CopyImages()
		pyautogui.press('f18') #Stop  PyComView
		time.sleep(1)
		pyautogui.press('f18')

		self.m_button1.Disable()
		self.m_choice1.Disable()
		self.m_button2.Disable()
		self.m_button3.Disable()
		self.m_button4.Disable()
		self.m_choice1.Clear()
		self.m_checkList1.Clear()
		self.STRUCTFOLDER = self.SettingsObj.ROIPATH
		self.CurrentPatientID = self.m_textCtrl1.GetValue()
		

		try:
			AllFiles = os.listdir(os.path.join(self.STRUCTFOLDER,self.CurrentPatientID))
			self.PrescriptionList = list()#AllFiles
			self.m_choice1.Clear()
			if len(AllFiles)!=0:
				for p in AllFiles:
					#~ if p.endswith(".dcm"):
						#~ self.m_choice1.Append(p.split(".dcm")[0])
						#~ self.PrescriptionList.append(p)
					if p.endswith(".pickle"):
						self.m_choice1.Append(p.split(".pickle")[0])
						self.PrescriptionList.append(p)

				self.Controller.PatientID = self.CurrentPatientID
				#if self.SettingsObj.debugLvl!=2079:
				self.StartPyComView()				
				
		except:
			self.MyLog("SearchPatient","Exception")
			self.m_button1.Enable()
			pass

		self.SetFocusIgnoringChildren() #Necessary for OnMouseWheel() function
#-------------------------------------------------------------------------------------------------------------------------------------------------------
	def PrescriptionChoice(self,evt):
		ID = self.m_choice1.GetCurrentSelection()
		self.m_button2.Enable()
		#presc = self.PrescriptionList[ID]
		#self.CurrentSTRUCT = 
		#~ self.NbOfROI = len(self.RT.StructureSetROISequence)
		#~ self.Contours = []
		#~ self.m_checkList1.Disable()
		#~ for i in range(self.NbOfROI):
			#~ self.Contours.append(self.RT.StructureSetROISequence[i].ROIName)
			#~ self.m_checkList1.Append(self.Contours[i])
		f = open(os.path.join(self.STRUCTFOLDER,self.CurrentPatientID,self.PrescriptionList[ID]),"rb")
		self.picklefile = pickle.load(f)
		f.close()
		
		self.NbOfROI = len(self.picklefile)
		self.Contours = []
		self.m_checkList1.Disable()
		for i in range(self.NbOfROI):
			self.Contours.append(self.picklefile[i][0])
			self.m_checkList1.Append(self.Contours[i])
		
		self.m_checkList1.SetCheckedItems(range(self.NbOfROI))
		size = (-1,self.NbOfROI*32)
		self.m_checkList1.SetSize(size)
		self.m_checkList1.SetMinSize(size)

		self.LoadTimeOffsetFit(ID)
#----------------------------------------------------------------------------------------------------------------------------------------------------
	def LoadTimeOffsetFit(self,ID): #Time offset pour prendre en compte sequence de lecture des colonnes du panneau
		self.Controller.GantryForTimeOffsetList = list()
		self.Controller.TimeOffsetList = list()
		
		f = open(os.path.join(self.STRUCTFOLDER,self.CurrentPatientID,self.PrescriptionList[ID].replace(".pickle",".txt")))
		Lines = f.readlines()
		f.close()
		
		Lines = list(filter(None,Lines))
		for k in range(self.NbOfROI):
			ROIName = str(Lines[k*721].replace("\n",""))
			GantryForTimeOffsetList = []
			TimeOffsetList = []
			for i in range(720):
				info = Lines[k*721+i+1].split("\t")
				GantryForTimeOffsetList.append(float(info[0]))
				TimeOffsetList.append(float(info[1]))
				
			self.Controller.GantryForTimeOffsetDict[ROIName] = GantryForTimeOffsetList
			self.Controller.TimeOffsetDict[ROIName] = TimeOffsetList
			
		self.MyLog("LoadTimeOffsetFit",str(len(self.Controller.TimeOffsetList)))
#-----------------------------------------------------------------------------------------------------------------------------------------------------
	def OnRefreshBackground(self,evt):
		self.m_textCtrl1.Disable()
		self.m_button1.Disable()
		self.m_choice1.Disable()
		self.m_button2.Disable()

		self.AcquisitionManagerObj.ResetLists()
		self.AcquisitionManagerObj.FindMostRecentMeasurementFolder()
		if self.AcquisitionManagerObj.MeasurementFolderPath is not None:
			self.AcquisitionManagerObj.ImageFilePathListBefore = self.AcquisitionManagerObj.GetList()

		pyautogui.press('f16') #Start
		self.LaunchProgressDialog(4)
		pyautogui.press('f17') #Pause
		
		self.AcquisitionManagerObj.FindMostRecentMeasurementFolder()
		if self.AcquisitionManagerObj.MeasurementFolderPath is not None:
			self.AcquisitionManagerObj.ImageFilePathListAfter = self.AcquisitionManagerObj.GetList()
			rtn = self.AcquisitionManagerObj.FindNewImages(NbMin=3)
			if rtn == True:
				self.AcquisitionManagerObj.DefineBackgroundFiles()
				self.Controller.CalibObj.DefineBackgroundImage(self.AcquisitionManagerObj.BackgroundFilePathList)
				self.m_checkList1.Enable()
				self.m_button3.Enable()
			else:
				wx.MessageBox('Background Failed. Please retry.', 'BACKGROUND FAILED',wx.OK | wx.ICON_INFORMATION)

		
		self.m_textCtrl1.Enable()
		self.m_button1.Enable()
		self.m_choice1.Enable()
		self.m_button2.Enable()
		#self.m_checkList1.Enable()
		#self.m_button3.Enable()



#------------------------------------------------------------------------------------------------------------------------------------------------
	def OnStart(self,evt):
		self.MyLog("OnStart","Called")
		self.m_button3.Disable()
		self.m_button4.Enable()
		self.m_button1.Disable()
		self.m_button2.Disable()
		self.m_choice1.Disable()
		self.m_textCtrl1.Disable()
		self.TimeTravelActivated = False
		self.Controller.CallStartAcquisition()
#----------------------------------------------------------------------------------------------------------------------------------------------------
	def OnStop(self,evt):
		self.MyLog("OnStop","Called")
		self.m_button4.Disable()
		self.m_button3.Enable()
		self.m_button1.Enable()
		self.m_button2.Enable()
		self.m_choice1.Enable()		
		self.m_textCtrl1.Enable()

		self.TimeTravelActivated = True
		if len(self.PNGFileList)>5:
			self.SetFocusIgnoringChildren()
			self.PNGIndex = len(self.PNGFileList)-1
		self.MyLog("OnStop: len(self.PNGFileList)",str(len(self.PNGFileList)))

		self.Controller.CallStopAcquisition()
				
		self.MyOpenGL.CurrentGLIm = np.zeros((512,512,4),dtype=np.uint8)
		self.MyOpenGL.OnIDLE()
#---------------------------------------------------------------------------------------------------------------------------------------------------
	#def ScanPNGs(self):
	  #  AllFiles = os.listdir(os.path.join(self.SettingsObj.ROOTPATH,"SavePNG"))
#---------------------------------------------------------------------------------------------------------------------------------------------------
	def LaunchProgressDialog(self,NbSec,mess="Background acquisition in Progress ..."):
		dialog = wx.ProgressDialog("Acquiring ...", mess, NbSec, style=wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME | wx.PD_AUTO_HIDE ) 
		count=0
		for k in range(0,NbSec):
			count+=1
			dialog.Update(count)
			time.sleep(1)
		dialog.Destroy()
#---------------------------------------------------------------------------------------------------------------------------------------------------
	def StartPyComView(self):

		def launch():
			try:
				os.chdir(os.path.join(self.SettingsObj.ROOTPATH,"PyComView","dist"))

				if (self.DebugLvl>0):
					subprocess.call("main.exe")
				else:
					CREATE_NO_WINDOW = 0x08000000
					subprocess.call("main.exe",creationflags=CREATE_NO_WINDOW)
				
			except:
				self.MyLog("StartPyComView","Exception")
				pass

				
		tl = threading.Thread(target = launch)
		tl.start()

		self.LaunchProgressDialog(5,mess="Starting PyComView ....")
		self.m_button1.Enable()
		self.m_choice1.Enable()	
#----------------------------------------------------------------------------------------------------------------------------------------------------		
	def OnSliderScroll(self,e):
		self.Threshold = int(self.m_slider1.GetValue()) 
#--------------------------------------------------------------------------------------------------------------
	def image_histogram_equalization(self,image, number_bins=256):

		image_histogram, bins = np.histogram(image.flatten(), number_bins, normed=True)
		image_histogram[0] = 0.0
		cdf = image_histogram.cumsum() # cumulative distribution function
		cdf = 255 * cdf / cdf[-1] # normalize
		
		# use linear interpolation of cdf to find new pixel values
		image_equalized = np.interp(image.flatten(), bins[:-1], cdf)

		return image_equalized.reshape(image.shape), cdf
#---------------------------------------------------------------------------------------------------------------------------------------------------
	def display(self,event):

		ROIs_id = self.m_checkList1.GetCheckedItems()
		LastROIAngle = 0.0
		
		if self.DebugLvl==2079:

			self.MyOpenGL.CurrentGLIm = np.random.randint(0,255,size=(512,512,4),dtype=np.uint8)

		if self.DebugLvl!=2079 and self.Controller.CalibObj.ImCount>self.DisplayedImCount:

			try:
					
				A=np.array(self.Controller.CalibObj.FrameDisplayed,dtype=np.float32)

				low_values_flags = A < self.Threshold  # Where values are low
				A[low_values_flags] = 0 
				
				if self.SettingsObj.EQUALIZE==True:
					A = self.image_histogram_equalization(A)[0]
				
				#self.MyLog("display A.mean",str(np.mean(A)))
				
				if self.cb1.GetValue()==True:
					A = 255 - A
				self.MyOpenGL.CurrentGLIm[::-1,:,0] = A
				self.MyOpenGL.CurrentGLIm[::-1,:,1] = A
				self.MyOpenGL.CurrentGLIm[::-1,:,2] = A
				self.MyOpenGL.CurrentGLIm[:,:,3] = 255

				
				Transparency = 0.65

				for z in range(len(self.picklefile)):
					if z in ROIs_id:
						self.MyLog("ROI_Name = ",str(self.picklefile[z][0]),level=1)
						self.MyLog("Dict keys = ",self.Controller.CalibObj.ImGantryAngleDict.keys(),level=2)
						q = float(self.Controller.CalibObj.ImGantryAngleDict[str(self.picklefile[z][0])])
						self.MyLog("Gantry angle",q)
						if (q<0):
							q+=360.0

						AnglePos = int(round(q*2))
						if AnglePos == 720:
							AnglePos = 0
							
						LastROIAngle = np.round(q,1)
						
						Res = 512/256 #Rescale
						v_color = self.picklefile[z][1]

						PosX = self.picklefile[z][2][AnglePos]
						PosY = self.picklefile[z][3][AnglePos]
						for j in range(len(PosX)):
							x = int(float(PosX[j])*Res)
							y = int(float(PosY[j])*Res)
							
							self.MyOpenGL.CurrentGLIm[511-y,511-x,0] = int(self.MyOpenGL.CurrentGLIm[511-y,511-x,0]*Transparency + int(v_color[0])*(1-Transparency))
							self.MyOpenGL.CurrentGLIm[511-y,511-x,1] = int(self.MyOpenGL.CurrentGLIm[511-y,511-x,1]*Transparency + int(v_color[1])*(1-Transparency))
							self.MyOpenGL.CurrentGLIm[511-y,511-x,2] = int(self.MyOpenGL.CurrentGLIm[511-y,511-x,2]*Transparency + int(v_color[2])*(1-Transparency))
				self.MyOpenGL.CurrentGLIm = np.fliplr(self.MyOpenGL.CurrentGLIm)
				self.DisplayedImCount = self.Controller.CalibObj.ImCount
				self.m_textCtrl2.SetValue(str(self.DisplayedImCount))
				
			except:
				self.MyOpenGL.CurrentGLIm[:,:,0] = 0
				self.MyOpenGL.CurrentGLIm[:,:,1] = 0
				self.MyOpenGL.CurrentGLIm[:,:,2] = 0
				self.MyOpenGL.CurrentGLIm[:,:,3] = 0
				self.MyLog("display","Exception")
		

			if self.SettingsObj.SAVEPNG==True:
				ImTemp = np.zeros((512,512,4),np.uint8)
				ImTemp[:,:,0] = self.MyOpenGL.CurrentGLIm[::-1,:,0]
				ImTemp[:,:,1] = self.MyOpenGL.CurrentGLIm[::-1,:,1]
				ImTemp[:,:,2] = self.MyOpenGL.CurrentGLIm[::-1,:,2]
				ImTemp[:,:,3] = self.MyOpenGL.CurrentGLIm[::-1,:,3]
				im = Image.fromarray(ImTemp,"RGBA")
				fname = str(self.CurrentPatientID)+"_"+str(self.Controller.CalibObj.ImCount) + "_" + str(LastROIAngle) + ".png"
				im.save(os.path.join(self.SettingsObj.ROOTPATH,"SavePNG",fname))
				self.PNGFileList.append(os.path.join(self.SettingsObj.ROOTPATH,"SavePNG",fname))

		self.MyOpenGL.OnIDLE()
#---------------------------------------------------------------------------------------------------------------------------------------------------
	#~ def OnMouseWheel(self,evt):
	#~ #	print "self.zoom:",self.MyOpenGL.zoom
		#~ #print evt.GetWheelRotation
		#~ if evt.GetWheelRotation()>0 and self.MyOpenGL.zoom<4:
				#~ self.MyOpenGL.zoom = self.MyOpenGL.zoom + 0.5


		#~ if evt.GetWheelRotation()<0 and self.MyOpenGL.zoom>1:
				#~ self.MyOpenGL.zoom = self.MyOpenGL.zoom - 0.5

		#~ self.MyLog("OnMouseWheel",str(self.MyOpenGL.zoom))
#~ #-------------------------------------------------------------------------------
	#~ def OnMouseWheelV2(self,evt):
				#~ self.MyOpenGL.zoom = float(self.m_sliderZoom.GetValue()) 
#=============================================================================================================================
class MyCanvasBase(glcanvas.GLCanvas):
	
	def __init__(self, parent,thisSettingsObj):
		glcanvas.GLCanvas.__init__(self, parent, -1)
		self.context = glcanvas.GLContext(self)

		self.CurrentGLIm = np.zeros((512,512,4),dtype=np.uint8)
		self.DisplayIm = np.zeros((512,512,4),dtype=np.uint8)
		
		self.SettingsObj = thisSettingsObj
		self.size = None
		self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
		self.Bind(wx.EVT_SIZE, self.OnSize)
		
		self.Bind(wx.EVT_RIGHT_DOWN,self.OnRightMouse)
		
		self.Bind(wx.EVT_LEFT_DOWN,self.OnMouseLeftDown)
		self.Bind(wx.EVT_LEFT_UP,self.OnMouseLeftUp)
		self.Bind(wx.EVT_MOTION,self.OnMouseMotion)
		self.ClearLogs()

		#Zoom and Pan
		self.CursorType = 'none'

		self.zoom = 1.0
		self.Zooming=False
		self.MouseDrag=False
		
		self.offsetx=0
		self.xstart=0
		self.xstop = 512
		self.istart=0
		self.istop=512

		self.offsety=0
		self.ystart=0
		self.ystop = 512
		self.jstart=0
		self.jstop=512

		self.xdragStart=0
		self.ydragStart=0
		self.xzoomStart=0
		self.yzoomStart=0	
#--------------------------------------------------------------------------------------------------------------------------------------------
	def ClearLogs(self):
		try:
			os.remove(os.path.join(self.SettingsObj.ROOTPATH,"Logs","MyCanvasBase.log"))
		except:
			pass
#--------------------------------------------------------------------------------------------------------------------------------------------
	def MyLog(self,mess="none",value="none",level=0):
		if level<=self.SettingsObj.debugLvl:
			f = open(os.path.join(self.SettingsObj.ROOTPATH,"Logs","MyCanvasBase.log"),"a")
			f.write(str(mess)+"\t"+str(value)+"\t"+str(datetime.now())+"\n")
			f.close()
#--------------------------------------------------------------------------------------------------------------------
	def OnIDLE(self):
		self.MyLog("OnIDLE",str(np.mean(self.CurrentGLIm[0])))
		self.MyLog("OnIDLE",str(self.zoom))
		
		self.DisplayIm[:,:,:]=0
		self.DisplayIm[self.jstart:self.jstop,self.istart:self.istop,:]=self.CurrentGLIm[self.ystart:self.ystop,self.xstart:self.xstop,:]

		xmag = int(512/self.zoom)
		xhalfwidth = int(xmag*0.5)
		xmag = 2*xhalfwidth
		self.DisplayIm[0:xmag,0:xmag,:] = self.DisplayIm[256-xhalfwidth:256+xhalfwidth,256-xhalfwidth:256+xhalfwidth,:]
		
		OpenGL.GL.glPixelZoom(self.zoom,self.zoom)
		OpenGL.GL.glDrawPixels(512,512,OpenGL.GL.GL_RGBA,OpenGL.GL.GL_UNSIGNED_BYTE,self.DisplayIm.tobytes())
		self.SwapBuffers()
#-------------------------------------------------------------------------------------------
	def OnRightMouse(self,evt):
		
		if self.CursorType == 'none':
			myCursor= wx.Cursor(wx.CURSOR_HAND)
			self.CursorType = 'Pan'
			
		elif self.CursorType == 'Pan':
			myCursor= wx.Cursor(wx.CURSOR_MAGNIFIER)
			self.CursorType = 'Magnifier'
		else:
			myCursor= wx.Cursor(wx.CURSOR_ARROW)
			self.CursorType = 'none'

		self.SetCursor(myCursor)
#-----------------------------------------------------------------------------------------------------------------
	def OnMouseLeftDown(self,event):
		x,y = event.GetPosition()
		#print x,y
		if self.CursorType=='Pan':
			self.MouseDrag = True
			self.xdragStart=x
			self.ydragStart=y
		
		if self.CursorType=='Magnifier':
			self.Zooming = True
			self.xzoomStart=x
			self.yzoomStart=y
#-----------------------------------------------------------------------------------------------------------------
	def OnMouseLeftUp(self,event):
		self.MouseDrag=False
		self.Zooming = False
#-----------------------------------------------------------------------------------------------------------------
	def OnMouseMotion(self,event):
		if self.CursorType=="Magnifier" and self.Zooming==True:
			x,y = event.GetPosition()
			
			deltay = self.yzoomStart-y
			self.yzoomStart = y
			
			#print "zoom deltay",deltay
			
			if deltay>0 and self.zoom<10:
				self.zoom = self.zoom + 0.1

			if deltay<0 and self.zoom>1:
				self.zoom = self.zoom - 0.1		
			
		
		if self.CursorType=="Pan" and self.MouseDrag==True:
			x,y = event.GetPosition()

			self.deltax=x-self.xdragStart
			self.deltay=self.ydragStart-y			
			self.xdragStart=x
			self.ydragStart=y			
			
			if self.deltax>0:
				self.offsetx = self.offsetx + 1				
			if self.deltax<0:
				self.offsetx = self.offsetx - 1

			if self.deltay>0:
				self.offsety = self.offsety + 1
			if self.deltay<0:
				self.offsety = self.offsety - 1

			
			if self.offsetx>=0:
				self.istart=self.offsetx
				self.istop=512
				self.xstart=0
				self.xstop=512-self.offsetx
			
			if self.offsetx<0:
				self.istart=0
				self.istop=512+self.offsetx
				self.xstart=-self.offsetx
				self.xstop=512				


			if self.offsety>=0:
				self.jstart=self.offsety
				self.jstop=512
				self.ystart=0
				self.ystop=512-self.offsety
			
			if self.offsety<0:
				self.jstart=0
				self.jstop=512+self.offsety
				self.ystart=-self.offsety
				self.ystop=512
				
				#~ print "self.istart",self.istart
				#~ print "self.istop",self.istop				
				#~ print "self.xstart",self.xstart
				#~ print "self.xstop",self.xstop
#------------------------------------------------------------------------------------------------------------------
	def OnEraseBackground(self, event):
		#print "OnEraseBackground"
		pass # Do nothing, to avoid flashing on MSW.
#-----------------------------------------------------------------------------------------------------------------
	def OnSize(self, event):
		#print "OnSize"
		wx.CallAfter(self.DoSetViewport)
		event.Skip()
#----------------------------------------------------------------------------------------------------------------
	def DoSetViewport(self):
		#print "OnDoSetViewPort"
		size = self.size = self.GetClientSize()
		#print "size.width",self.size
		
		self.SetCurrent(self.context) #Makes the OpenGL state that is represented by the OpenGL rendering context context current
		OpenGL.GL.glViewport(0, 0, size.width, size.height)
#===================================================================================================================
class RunApp(wx.App):
	def __init__(self):
		wx.App.__init__(self, redirect=False)
		
	def OnInit(self):
		S = Settings.Settings()
		self.frame = MyFrame1(parent = None,DebugLvl=S.debugLvl,settingsObj = S)
		self.SetTopWindow(self.frame)
		return True

#===================================================================================================================
if __name__ == "__main__":
	app = RunApp()
	app.MainLoop()
