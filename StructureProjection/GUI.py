# -*- coding: utf-8 -*- 

import wx
import os
import sys
import numpy as np
import glob
import dicom
import pickle
import Module_DicomImageSeries
import Module_RTStructFile
from ModSPReadResults import Results
import Intersect_multiprocessing
import ModEligibility

DEBUG = 0

from wx import glcanvas

# The Python OpenGL package can be found at
# http://PyOpenGL.sourceforge.net/
from OpenGL.GL import *
from OpenGL.GLUT import *

###########################################################################
## Class MyFrame1
###########################################################################

class MyFrame1 ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = "STRUCTURE PROJECTION", pos = wx.DefaultPosition, size = wx.Size( 860,750 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.Centre( wx.BOTH )
		self.Show(True)
	
	def __del__( self ):
		pass
	

###########################################################################
## Class MyPanel1
###########################################################################

class MyPanel1 ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 860,750 ), style = wx.TAB_TRAVERSAL )
		
		self.MyOpenGL = 'none'
		self.DCMFolderObj = 'none'
		self.ImSerieObj = 'none'
		
		bSizer1 = wx.BoxSizer( wx.HORIZONTAL )
		bSizer1.AddSpacer(15)
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		bSizer2.AddSpacer(15)
		bSizer3 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.dirDialog = wx.DirDialog (self, "Choose input directory", "",wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)		
		
		self.m_button1 = wx.Button( self, wx.ID_ANY, u"Scan Folder", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_button1.Bind(wx.EVT_BUTTON,self.OnScanFolder)
		bSizer3.Add( self.m_button1, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		bSizer2.Add( bSizer3, 1, wx.EXPAND, 5 )
		bSizer2.AddSpacer(15)
		
		self.PrescriptionList = list()
		self.m_choice1 = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, self.PrescriptionList, 0 ,wx.DefaultValidator)
		self.m_choice1.SetMinSize( wx.Size( 225,-1 ) )
		bSizer2.Add(self.m_choice1, 0, wx.ALIGN_LEFT|wx.ALL|wx.EXPAND, 5 )
		self.m_choice1.Bind(wx.EVT_CHOICE,self.OnSelectPrescription)
	
		bSizer2.AddSpacer(15)
		
		m_checkList1Choices = []
		self.m_checkList1 = wx.CheckListBox( self, wx.ID_ANY, wx.DefaultPosition, (250,200), m_checkList1Choices, 0 )
		self.m_checkList1.Bind(wx.EVT_CHECKLISTBOX,self.OnContourSelection)
		bSizer2.Add( self.m_checkList1, 0, wx.ALL, 5 )
		
		bSizer2.AddSpacer(10)
		
		self.m_textCtrl1 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textCtrl1.SetMinSize( wx.Size( 225,25 ) )
		self.m_textCtrl1.WriteText("")
		bSizer2.Add( self.m_textCtrl1,0, wx.ALIGN_LEFT,  5 )
		bSizer2.AddSpacer(10)
		
		self.m_button2 = wx.Button( self, wx.ID_ANY, u"Project Structures", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_button2.Disable()
		self.m_button2.Bind(wx.EVT_BUTTON,self.OnProjectStructures)
		bSizer2.Add( self.m_button2, 0, wx.ALL, 5 )
		bSizer2.AddSpacer(5)		

		bSizer1.Add( bSizer2, 1, wx.ALIGN_TOP, 5 )
		bSizer1.AddSpacer(15)
		bSizer5 = wx.BoxSizer( wx.VERTICAL )
		bSizer5.AddSpacer(15)
		
		self.MyOpenGL = MyCanvasBase(self)
		self.MyOpenGL.SetMinSize((512,512))
		bSizer5.Add( self.MyOpenGL, 0, wx.ALL, 5 )
		
		bSizer5.AddSpacer(15)
		
		self.m_slider1 = wx.Slider( self, wx.ID_ANY, 50, 0, 100, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL )
		self.m_slider1.Bind(wx.EVT_SCROLL,self.OnSliderScroll)
		bSizer5.Add( self.m_slider1, 0, wx.ALIGN_TOP|wx.ALL|wx.EXPAND, 5 )
		
		bSizer5.AddSpacer(15)
		
		self.m_textCtrl2 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY )
		self.m_textCtrl2.SetMinSize( wx.Size( 250,25 ) )
		bSizer5.Add( self.m_textCtrl2, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )
		bSizer5.AddSpacer(5)

		
		bSizer1.Add( bSizer5, 1, wx.EXPAND, 5 )
		
		bSizer1.AddSpacer(15)
		
		self.SetSizer( bSizer1 )
		self.Layout()
		self.LoadSettings()
	
	def __del__( self ):
		pass
		
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
	def OnScanFolder(self,e): #When the button Scan Folder is pressed. The Folder chosen must contains the dicom RTPLAN, RTStruct, and CT images. The function create the list of all the prescriptions present in the folder.
		
		self.dirDialog.SetPath(self.DefaultPATHScanFolder)
		self.dirDialog.ShowModal()
		PATH = self.dirDialog.GetPath()
		files = glob.glob(PATH+"/*.dcm")	
		
		self.CTs = []
		self.rtstructs = []
		self.rtplans = []
		
		for f in files:
			dcm = dicom.read_file(f)
			if dcm.Modality == "CT":
				self.CTs.append(dcm)
			if dcm.Modality == "RTSTRUCT":
				self.rtstructs.append(dcm)
			if dcm.Modality == "RTPLAN":
				self.rtplans.append(dcm)				
		
		if len(self.rtplans)>0:
			self.PrescriptionList = list()
			self.PrescList = list()
			for plan in self.rtplans:
				#~ try:
				for prescription in plan.FractionGroupSequence:
					beamInPresc = []
					MUInPresc = []
					for B in prescription.ReferencedBeamSequence:
						try:
							beamInPresc.append(B.ReferencedBeamNumber)
							MUInPresc.append(int(B.BeamMeterset))
						except:
							pass
							
					for BS in plan.BeamSequence:
						for i in range(len(beamInPresc)):
							try:
								if BS.BeamNumber == beamInPresc[i] and MUInPresc[i]>1:
									Isocenter = BS.ControlPointSequence[0].IsocenterPosition
							except:
								pass
						
					self.PrescriptionList.append(str(plan.RTPlanName) + "   Prescription "+str(prescription.FractionGroupNumber) + " ("+str(prescription.NumberOfFractionsPlanned) +" fractions, "+str(prescription.NumberOfBeams)+" beams), Iso="+str(Isocenter))
					
					self.PrescList.append((plan,Isocenter,prescription.FractionGroupNumber))
					
				#~ except:
					#~ pass
		
		self.m_choice1.Clear()
		for p in self.PrescriptionList:
			self.m_choice1.Append(p)
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------				
	def OnSelectPrescription(self,e): # When the prescription is selected. The structures associated to this prescription are loaded and listed. The CT images and RTPLAN are also loaded. The name of the prescription is set as the name that will be used for the pickle file generated at the end but can be edited in the GUI
		
		
		c = self.m_choice1.GetSelection()
		self.Selectedplan = self.PrescList[c][0]
		self.Selectedpresc = self.PrescList[c][2]
		
		self.m_textCtrl1.Clear()
		self.SavingFileName = str(self.Selectedplan.RTPlanName)+"_"+str(self.Selectedpresc)#+".dcm"
		self.SavingFileName = self.SavingFileName.replace(' ','')
		self.m_textCtrl1.WriteText(self.SavingFileName)
		
		RefRTSTRUCT = self.Selectedplan.ReferencedStructureSetSequence[0].ReferencedSOPInstanceUID
		
		Iso = str(self.PrescList[c][1]).split("'")
		
		self.SelectedIsocenter = [float(Iso[1]),float(Iso[3]),float(Iso[5])]
		
		self.SelectedRTSTRUCT = 'None'
		for r in self.rtstructs:
			if RefRTSTRUCT == r.SOPInstanceUID:
				self.SelectedRTSTRUCT = r
				
				self.RTStructObj = Module_RTStructFile.RTStructFile(self.SelectedRTSTRUCT)
		
				self.m_checkList1.Clear()
				for k in range(len(self.RTStructObj.ROINameList)):
					self.m_checkList1.Append(self.RTStructObj.ROINameList[k])
		
		if self.SelectedRTSTRUCT == 'None':
			NoRTSTRUCT= wx.MessageDialog (self, "No RTSTRUCT corresponding to the selected plan",style=wx.OK)
			NoRTSTRUCT.ShowModal()
		
		self.SelectedCT = list()
		for f in self.CTs:
			if self.SelectedRTSTRUCT.ReferencedFrameOfReferenceSequence[0].RTReferencedStudySequence[0].RTReferencedSeriesSequence[0].SeriesInstanceUID == f.SeriesInstanceUID:
				self.SelectedCT.append(f)
				
		self.SelectedCT.sort(key=lambda x: x.SliceLocation)
		
		self.ImSerieObj = Module_DicomImageSeries.ImageSeries(self.SelectedCT)
		self.OnLoadImage()
						
			
		
		
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
	def OnContourSelection(self,e):  # When ROIs are selected.
		
		self.ImSerieObj.ResetPixelData()

		u = self.m_checkList1.GetCheckedStrings()
		
		if len(u) != 0:
			
			for roiname in u:
				idx = self.RTStructObj.ROINameList.index(str(roiname))
				ROIID = self.RTStructObj.ROIIDList[idx]

				self.RTStructObj.DefineROI(ROIID,self.ImSerieObj.X0,self.ImSerieObj.DirectionX,self.ImSerieObj.Y0,self.ImSerieObj.DirectionY,self.ImSerieObj.Z0,self.ImSerieObj.DirectionZ,self.ImSerieObj.PixelSpacing[0],self.ImSerieObj.SliceSpacing)
				self.ImSerieObj.AddContour(self.RTStructObj.ROIContourDicomCoords)

		self.m_button2.Enable()
		
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
	def OnSliderScroll(self,e):
		obj = e.GetEventObject()
		val = obj.GetValue() 

		
		self.MyOpenGL.CurrentGLIm[:,:,:] = self.ImSerieObj.Im3DDisplay[val,:,:,:]

		self.MyOpenGL.DisplayIm(self.ImSerieObj.Im3DDisplay[val])
		self.MyOpenGL.CurrentImageNumber = val

		self.m_textCtrl2.SetValue("Index_k: "+str(val) + "  Dicom_Z: " + str(np.round(self.ImSerieObj.thisImageSerie[val].SliceLocation,2)))

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
	def OnLoadImage(self):

		self.ImSerieObj.LoadPixelData()			

		self.MyOpenGL.CurrentGLIm = self.ImSerieObj.Im3DDisplay[5].copy()
		self.MyOpenGL.DisplayIm(self.ImSerieObj.Im3DDisplay[5])
		self.m_slider1.SetRange(0,(self.ImSerieObj.NbIm-1))	

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
	def OnProjectStructures(self,e):
		
		Eligibility = ModEligibility.CheckEligibility(self.Selectedplan, self.Selectedpresc)
		
		if Eligibility == False:
			NOTELIGIBILE= wx.MessageDialog (self, "This plan has one or more segments that irradiate beyond the limits of the detector! This plan is not eligible for MV fluoroscopy.",style=wx.OK)
			NOTELIGIBILE.ShowModal()
		
		else:
			print "Plan eligible"
			self.m_button2.Disable()
			self.SavingFileName = self.m_textCtrl1.GetLineText(0)
			
			PatientID = self.SelectedRTSTRUCT.PatientID

			RoiNames = self.m_checkList1.GetCheckedStrings()
			
			CT=self.SelectedCT
			if(int(CT[0].ImageOrientationPatient[0])*int(CT[0].ImageOrientationPatient[4])>0):
				sensZ = 1
			else:
				sensZ = -1
				
			sensCT = [CT[0].ImageOrientationPatient[0],CT[0].ImageOrientationPatient[4],sensZ]

			f = open(os.path.join(self.ThisFilePath,"listROI.txt"),"w")
			
			for i in range(len(RoiNames)):
				self.ImSerieObj.ResetPixelData()
				idx = self.RTStructObj.ROINameList.index(str(RoiNames[i]))
				ROIID = self.RTStructObj.ROIIDList[idx]
				self.RTStructObj.DefineFinalROI(ROIID,self.ImSerieObj.X0,self.ImSerieObj.DirectionX,self.ImSerieObj.Y0,self.ImSerieObj.DirectionY,self.ImSerieObj.Z0,self.ImSerieObj.DirectionZ,self.ImSerieObj.PixelSpacing[0],self.ImSerieObj.SliceSpacing)
				self.ImSerieObj.AddROI(self.RTStructObj.ROIVoxelsIndexCoords)
				b = self.ImSerieObj.Im3DTissue.astype(np.uint8)
				b.tofile(os.path.join("ROIs",PatientID+"."+str(RoiNames[i])))
				
				nZ = np.nonzero(b)
				Zmin = min(nZ[0])
				Zmax = max(nZ[0])
				Ymin = min(nZ[1])
				Ymax = max(nZ[1])
				Xmin = min(nZ[2])
				Xmax = max(nZ[2])
				
				#~ print Xmin,Xmax,Ymin,Ymax,Zmin,Zmax
				f.write(str(RoiNames[i])+"\t"+str(Xmin)+"\t"+str(Xmax)+"\t"+str(Ymin)+"\t"+str(Ymax)+"\t"+str(Zmin)+"\t"+str(Zmax)+"\n")
			
			f.close()

			resolution = CT[0].PixelSpacing
			resolution.append(CT[0].SliceThickness)
			refPointCT = CT[0].ImagePositionPatient
			for im in CT:
				if float(im.ImagePositionPatient[2]) > float(refPointCT[2]):
					refPointCT[2] = im.ImagePositionPatient[2]
			
			Dim = (int(CT[0].Rows),int(CT[0].Columns),int(len(CT)))
			
			
			args = str(self.SelectedIsocenter[0])+" "+str(self.SelectedIsocenter[1])+" "+str(self.SelectedIsocenter[2])+" "+str(sensCT[0])+" "+str(sensCT[1])+" "+str(sensCT[2])+" "+str(PatientID)+" "+str(resolution[0])+" "+str(resolution[1])+" "+str(resolution[2])+" "+str(refPointCT[0])+" "+str(refPointCT[1])+" "+str(refPointCT[2])+" "+str(len(RoiNames))+" "+str(Dim[0])+" "+str(Dim[1])+" "+str(Dim[2])
			
			if self.GPU == "True":
				os.system(os.path.join(self.ThisFilePath,"StructureProjection","main")+" "+os.getcwd()+" "+args)
			else:
				Intersect_multiprocessing.intersectCPU(self.ThisFilePath,self.SelectedIsocenter,refPointCT,sensCT,resolution,Dim,PatientID,RoiNames,4)
			
			self.SavePickleFile(PatientID)
			
			if DEBUG == 0:
				folder = os.path.join(self.ThisFilePath,"ROIs")
				for file in os.listdir(folder):
					file = os.path.join(folder, file)
					try:
						if os.path.isfile(file):
							os.remove(file)
					except: 
						pass
				file = os.path.join(self.ThisFilePath,"StructureProjection","Results")
				if os.path.isfile(file):
					os.remove(file)
				
				file=os.path.join(self.ThisFilePath,"listROI.txt")
				if os.path.isfile(file):
					os.remove(file)

			self.ModifyDisplayPickle()

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
	def OnSliderScroll2(self,e):
		
		self.Angle = int(self.m_slider1.GetValue())
		self.DisplayPickle(wx.EVT_CHECKLISTBOX)
		self.m_textCtrl2.Clear()
		self.m_textCtrl2.WriteText('Grantry Angle = '+str(float(self.Angle)/2.0))
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------	
	def LoadSettings(self):
		try:
			f = open(os.path.join(os.getcwd(),"settings.txt"),"r")
			lines = f.readlines()
			f.close()
		except:
			print "No file settings.txt in current working directory"
			sys.exit()
		lines = filter(None,lines)
		dict = {}
		for l  in lines:
			if l.find("#")!=-1:
				l = l.split("#")
				l=l[0]
			l=l.replace(" ","")
			l=l.replace("\t","")
			l=l.replace("\n","")
			l=l.replace("\r","")
			vars = l.split("=")
			dict[vars[0]] = str(vars[1])
		
		self.DefaultPATHScanFolder = dict["DefaultPATHScanFolder"] #Default path where all the folders containing dicom files are.
		#~ self.ThisFilePath = dict["GUIPath"] #Path of the folder StructureProjection containing GUI.py 
		self.SavingPath = dict["SavingPath"] #root path where the generated folders are saved
		self.GPU = dict["GPU"] #Using GPU or not
		
		self.ThisFilePath = os.getcwd()
		
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
	def SavePickleFile(self,id_Patient):
		R = Results(self.ThisFilePath)
		ROIsNames = R.Names
		ROIsNbContours = R.NbOfContours
		Data = R.ROIsData
		TPSStruct = self.SelectedRTSTRUCT
		
		ListToSave = []
		for i in range(len(ROIsNames)):
			color = 'None'
			for c in range(len(TPSStruct.StructureSetROISequence)):
					if TPSStruct.StructureSetROISequence[c].ROIName == ROIsNames[i]:
						color = TPSStruct.ROIContourSequence[c].ROIDisplayColor
			
			PosX = []
			PosY = []
			for j in range(ROIsNbContours):
				CX = []
				CY = []
				for x in range(len(Data[i][j])/2):
					CX.append(Data[i][j][2*x])
					CY.append(Data[i][j][2*x+1])
				PosX.append(np.array(CX))
				PosY.append(np.array(CY))
			
			t = (ROIsNames[i],[int(color[0]),int(color[1]),int(color[2])],PosX,PosY)
			ListToSave.append(t)
		
		
		f = open(os.path.join(self.ThisFilePath,"StructureProjection","ProjectionStruct.pickle"),"wb")
		pickle.dump(ListToSave,f)
		f.close()
		
		path_tmp = self.SavingPath+id_Patient
		if not os.path.isdir(path_tmp):
			os.mkdir(path_tmp)
		
		f = open(os.path.join(path_tmp,self.SavingFileName+".pickle"),"wb")
		pickle.dump(ListToSave,f)
		f.close()
		
		self.writeTimeOffset(id_Patient)
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
	def writeTimeOffset(self,id_Patient):
		# Depending on the position of the Structures on the EPID in the lateral direction, a different EPID readout time offset will be applied.
		f = open(os.path.join("StructureProjection","Centroid.txt"),"r")
		Lines = f.readlines()

		GantryAngles = []
		TimeOffset = []
		x = [0,255,256,511]
		t = [0,0.433e07,0.433e07,0]
		
		path_tmp = self.SavingPath+id_Patient
		filename = os.path.join(path_tmp,self.SavingFileName+".txt")
		
		g = open(filename,"w")
		
		
		for l in Lines:
			l = l.split("\t")
			if  len(l)==3:
				xi = 511.0-float(l[1])
				g.write(str(float(l[0]))+"\t"+str(int(np.interp(xi,x,t)))+"\n")
			else:
				g.write(str(l[0]))
				
		f.close()
		g.close()

		
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
	def ModifyDisplayPickle(self):
		self.Angle = 0 
		self.m_slider1.SetRange(0,720)
		self.m_slider1.Unbind(wx.EVT_SCROLL)
		self.m_slider1.Bind(wx.EVT_SCROLL,self.OnSliderScroll2)
		
		self.m_checkList1.Unbind(wx.EVT_CHECKLISTBOX)
		self.m_checkList1.Bind(wx.EVT_CHECKLISTBOX,self.DisplayPickle)
		g = open(os.path.join(self.ThisFilePath,"StructureProjection","ProjectionStruct.pickle"),"rb")
		self.ProjectedRT = pickle.load(g)
		g.close()
		
		self.m_checkList1.Clear()
		for tup in self.ProjectedRT:
			self.m_checkList1.Append(tup[0])
		
		for i in range(len(self.ProjectedRT)):
			self.m_checkList1.Check(i)
		self.DisplayPickle(wx.EVT_CHECKLISTBOX)	

		self.m_textCtrl2.Clear()
		self.m_textCtrl2.WriteText('Grantry Angle = '+str(self.Angle))
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------	
	def DisplayPickle(self,e):
		
		self.MyOpenGL.CurrentGLIm = np.zeros((512,512,4),dtype=np.uint8)
		ROINames = self.m_checkList1.GetCheckedStrings()
		
		
		for roi in ROINames:
			try:
				for t,tup in enumerate(self.ProjectedRT):
					#~ print tup
					if roi == tup[0]:
						#~ print roi
						Res = 512/256 #Rescale
						v_color =tup[1]
						for j in range(len(tup[2][self.Angle])):
							x = int(float(tup[2][self.Angle][j])*Res)
							y = int(float(tup[3][self.Angle][j])*Res)
							self.MyOpenGL.CurrentGLIm[-y,x,0] = int(v_color[0])
							self.MyOpenGL.CurrentGLIm[-y,x,1] = int(v_color[1])
							self.MyOpenGL.CurrentGLIm[-y,x,2] = int(v_color[2])
							
			except:
				pass
				
		
		self.MyOpenGL.DisplayIm(self.MyOpenGL.CurrentGLIm)
		
		
#===================================================================================================================
class MyCanvasBase(glcanvas.GLCanvas):
	
	def __init__(self, parent):
		glcanvas.GLCanvas.__init__(self, parent, -1)
		self.context = glcanvas.GLContext(self)

		self.ZoomValue = 1.0 #'none'#2.0

		self.CurrentGLIm = 'none'
		
		self.size = None
		self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
		self.Bind(wx.EVT_SIZE, self.OnSize)

#--------------------------------------------------------------------------------------------------------------------
	def DisplayIm(self,thisIm):
		
		if self.ZoomValue == 1.0:
			
			glPixelZoom(self.ZoomValue,self.ZoomValue)
			glDrawPixels(thisIm.shape[0],thisIm.shape[1],GL_RGBA,GL_UNSIGNED_BYTE,thisIm.tobytes())
			self.SwapBuffers()
			
#------------------------------------------------------------------------------------------------------------------
	def OnEraseBackground(self, event):
		pass # Do nothing, to avoid flashing on MSW.
#-----------------------------------------------------------------------------------------------------------------
	def OnSize(self, event):
		wx.CallAfter(self.DoSetViewport)
		event.Skip()
#----------------------------------------------------------------------------------------------------------------
	def DoSetViewport(self):
		size = self.size = self.GetClientSize()
		self.SetCurrent(self.context) #Makes the OpenGL state that is represented by the OpenGL rendering context context current
		glViewport(0, 0, size.width, size.height)
		
#===================================================================================================================
class RunApp(wx.App):
	def __init__(self):
		wx.App.__init__(self, redirect=False)

	def OnInit(self):
	
		self.frame = MyFrame1(parent = None)
		
		self.panel = MyPanel1(parent = self.frame)
		self.SetTopWindow(self.frame)

		return True
		

#===================================================================================================================
if __name__ == "__main__":
	app = RunApp()
	app.MainLoop()