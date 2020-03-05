import sys
from matplotlib import path
import numpy as np


#=======================================================================================================
class RTStructFile:

	def __init__(self,RTS):

		self.Status = True
		self.DCM = RTS

		
		self.ROINameList = list()
		self.ROIIDList = list()

		for ROI in self.DCM.StructureSetROISequence:
			self.ROINameList.append(ROI.ROIName)
			self.ROIIDList.append(ROI.ROINumber)

#--------------------------------------------------------------------------------------------------------------------------
	def DefineROI(self,thisROIID,X0,DirectionX,Y0,DirectionY,Z0,DirectionZ,PixelSpacing,SliceSpacing):
		
		self.Margin = 10
		self.i_Start = 'none'
		self.j_Start = 'none'
		self.k_Start = 'none'
		self.Nb_i = 'none'
		self.Nb_j = 'none'
		self.Nb_k = 'none'
		self.GetROIProperties(thisROIID,X0,DirectionX,Y0,DirectionY,Z0,DirectionZ,PixelSpacing,SliceSpacing)
		
		self.ROIVoxelsIndexCoords = list() #liste des index de toutes les voxels de la ROI ([i,j,k],[i,j,k], ... )
		self.ROIContourDicomCoords = list() #liste des coord dicom du contour de la ROI ([x1,y1,z1],[x2,y2,z2],......)
		self.GetROIVoxelsIndexCoords(thisROIID,X0,DirectionX,Y0,DirectionY,Z0,DirectionZ,PixelSpacing,SliceSpacing,final=0)

#--------------------------------------------------------------------------------------------------------------------------
	def DefineFinalROI(self,thisROIID,X0,DirectionX,Y0,DirectionY,Z0,DirectionZ,PixelSpacing,SliceSpacing):
		
		self.Margin = 10
		self.i_Start = 'none'
		self.j_Start = 'none'
		self.k_Start = 'none'
		self.Nb_i = 'none'
		self.Nb_j = 'none'
		self.Nb_k = 'none'
		self.GetROIProperties(thisROIID,X0,DirectionX,Y0,DirectionY,Z0,DirectionZ,PixelSpacing,SliceSpacing)
		
		self.ROIVoxelsIndexCoords = list() #liste des index de toutes les voxels de la ROI ([i,j,k],[i,j,k], ... )
		self.ROIContourDicomCoords = list() #liste des coord dicom du contour de la ROI ([x1,y1,z1],[x2,y2,z2],......)
		self.GetROIVoxelsIndexCoords(thisROIID,X0,DirectionX,Y0,DirectionY,Z0,DirectionZ,PixelSpacing,SliceSpacing,final=1)


#-----------------------------------------------------------------------------------------------------------------------------------
	def GetROIProperties(self,thisROIID,X0,DirectionX,Y0,DirectionY,Z0,DirectionZ,PixelSpacing,SliceSpacing): #the main goal of this function is to determine the limits of the coordinates of the ROIs.
		
		self.i_list = list() #Index Coords grille Image dataset
		self.j_list = list()
		self.k_list = list()
		
		for ROI in self.DCM.ROIContourSequence:
			if int(ROI.ReferencedROINumber) == int(thisROIID):
				for contour in ROI.ContourSequence:

					for p in range(0,contour.NumberofContourPoints):
						x=contour.ContourData[3*p] #Dicom coordinates
						y=contour.ContourData[3*p+1]
						z=contour.ContourData[3*p+2]

					
						i = np.int(np.rint(((x-X0)/(DirectionX*PixelSpacing)))) #Index coordinates
						j = np.int(np.rint(((y-Y0)/(DirectionY*PixelSpacing))))
						k = np.int(np.rint(((z-Z0)/(DirectionZ*SliceSpacing))))

						self.i_list.append(i)
						self.j_list.append(j)
						self.k_list.append(k)

	
		imin = np.min(self.i_list)
		jmin = np.min(self.j_list)
		kmin = np.min(self.k_list)
		
		imax = np.max(self.i_list)
		jmax = np.max(self.j_list)
		kmax = np.max(self.k_list)
		
		
		self.k_Start = kmin - self.Margin
		self.k_Stop = kmax + self.Margin
		self.Nb_k = (self.k_Stop-self.k_Start)+1
		
		self.j_Start = jmin - self.Margin
		self.j_Stop = jmax + self.Margin
		self.Nb_j = (self.j_Stop-self.j_Start)+1
		

		self.i_Start = imin - self.Margin
		self.i_Stop = imax + self.Margin
		self.Nb_i = (self.i_Stop-self.i_Start)+1
		
#---------------------------------------------------------------------------------------------------------------------------------------
	def GetROIVoxelsIndexCoords(self,thisROIID,X0,DirectionX,Y0,DirectionY,Z0,DirectionZ,PixelSpacing,SliceSpacing,final):
		
		for ROI in self.DCM.ROIContourSequence:
			
			if int(ROI.ReferencedROINumber) == int(thisROIID):
				for contour in ROI.ContourSequence:
					
					#Find k indice
					thisz = contour.ContourData[2]
					k = np.int(np.rint(((thisz-Z0)/(DirectionZ*SliceSpacing))))
					
					thisPath = list()
					for p in range(0,contour.NumberofContourPoints):
						x=contour.ContourData[3*p]
						y=contour.ContourData[3*p+1]
						z=contour.ContourData[3*p+2]
						
						i = np.int(np.rint(((x-X0)/(DirectionX*PixelSpacing))))
						j = np.int(np.rint(((y-Y0)/(DirectionY*PixelSpacing))))
						
						thisPath.append([i,j])
						self.ROIContourDicomCoords.append([x,y,z])
					
					if final==1:
						thisPath = path.Path(thisPath)

						for j in range(self.j_Start,self.j_Stop):
							for i in range(self.i_Start,self.i_Stop):
								if thisPath.contains_point([i,j],radius=0.01)== 1:
									self.ROIVoxelsIndexCoords.append([i,j,k])

