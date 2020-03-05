import os
import numpy as np
#=================================================================================
class ImageSeries:

	def __init__(self,thisImageSerie):

		self.SeriesInstanceUID = "none"
		self.thisImageSerie = thisImageSerie
		#*******************************
		self.Modality = 'none'
		self.SeriesNumber = 'none'
		self.NbIm = len(self.thisImageSerie)
		self.NbRows = 'none'
		self.NbColumns = 'none'
		self.PixelSpacing = 'none'
		self.Label = 'none'
		self.GetMetaData()
		
		self.Im3DDisplay = np.zeros((self.NbIm,self.NbRows,self.NbColumns,4),np.uint8)
		self.Im3DDisplayOriginal =  np.zeros((self.NbIm,self.NbRows,self.NbColumns,4),np.uint8)
		self.Im3DTissue = np.zeros((self.NbIm,self.NbRows,self.NbColumns),np.uint8)

#----------------------------------------------------------------------------------------------------------------------------
	def AddROI(self,ArrayCoordList):
		invert = self.NbRows-1
		for p in ArrayCoordList:
			i=p[0]
			j=p[1]
			k=p[2]
			self.Im3DDisplay[k,invert-j,i,0]=250
			self.Im3DDisplay[k,invert-j,i,1]=0
			self.Im3DDisplay[k,invert-j,i,2]=0
			self.Im3DTissue[k,j,i] = 1
#--------------------------------------------------------------------------------------------------
	def AddContour(self,CoordList):
		invert = self.NbRows-1
		for p in CoordList:
			i,j,k = self.ConvertCoordinates_DicomToGrid(p[0],p[1],p[2])
			self.Im3DDisplay[k,invert-j,i,0]=0
			self.Im3DDisplay[k,invert-j,i,1]=250
			self.Im3DDisplay[k,invert-j,i,2]=0

#--------------------------------------------------------------------------------------------------
	def ResetPixelData(self):
		self.Im3DDisplay[:,:,:,:] = self.Im3DDisplayOriginal[:,:,:,:]
		self.Im3DTissue = np.zeros((self.NbIm,self.NbRows,self.NbColumns),np.uint8)
#----------------------------------------------------------------------------------------------
	def LoadPixelData(self):
		
		for k,thisDCM in enumerate(self.thisImageSerie):

			max= np.amax(thisDCM.pixel_array)

			A =thisDCM.pixel_array*(255/float(max))
			
			self.Im3DDisplay[k,:,:,0] = np.flipud(A.astype(np.uint8))
			self.Im3DDisplay[k,:,:,1] = np.flipud(A.astype(np.uint8))
			self.Im3DDisplay[k,:,:,2] = np.flipud(A.astype(np.uint8))
			self.Im3DDisplay[k,:,:,3] = 0.0#Fully opaque
		
	
		self.Im3DDisplayOriginal[:,:,:,:] = self.Im3DDisplay[:,:,:,:] 
#----------------------------------------------------------------------------------------------
	def GetMetaData(self):

		self.SeriesInstanceUID = self.thisImageSerie[0].SeriesInstanceUID
		
		self.PixelSpacing = self.thisImageSerie[0].PixelSpacing
		self.NbRows = self.thisImageSerie[0].Rows
		self.NbColumns = self.thisImageSerie[0].Columns

		self.ImagePosition = self.thisImageSerie[0].ImagePositionPatient
		self.ImageOrientation = list(self.thisImageSerie[0].ImageOrientationPatient)      
		
		
		self.X0 = self.ImagePosition[0]
		self.DirectionX = int(self.ImageOrientation[0])
		self.Y0 = self.ImagePosition[1]
		self.DirectionY = int(self.ImageOrientation[4])
		self.Z0 = self.ImagePosition[2]
		self.DirectionZ = self.DirectionX*self.DirectionY
		
		
		self.SliceSpacing = abs(float(self.thisImageSerie[0].SliceLocation)-float(self.thisImageSerie[1].SliceLocation)) #Raystation
		#~ self.SliceSpacing = abs(float(self.thisImageSerie[0].SpacingBetweenSlices))
		
		self.CoordinateMatrix = np.zeros((4,4),np.float)
		self.CoordinateMatrix[0,0] = self.ImageOrientation[0]*self.PixelSpacing[0]
		self.CoordinateMatrix[1,0] = self.ImageOrientation[1]*self.PixelSpacing[0]
		self.CoordinateMatrix[2,0] = self.ImageOrientation[2]*self.PixelSpacing[0]
		self.CoordinateMatrix[3,0] = 0.0
		
		self.CoordinateMatrix[0,1] = self.ImageOrientation[3]*self.PixelSpacing[1]
		self.CoordinateMatrix[1,1] = self.ImageOrientation[4]*self.PixelSpacing[1]
		self.CoordinateMatrix[2,1] = self.ImageOrientation[5]*self.PixelSpacing[1]
		self.CoordinateMatrix[3,1] = 0.0
		
		self.CoordinateMatrix[0,3] = self.ImagePosition[0]
		self.CoordinateMatrix[1,3] = self.ImagePosition[1]
		self.CoordinateMatrix[2,3] = self.ImagePosition[2]
		self.CoordinateMatrix[3,3] = 1.0
		
#-----------------------------------------------------------------------------------------------------------------------------
	def ConvertCoordinates_GridToDicom(self,i,j,k):
		
		PlaneCoords = self.CoordinateMatrix.dot([i,j,0,1]) #[i,j,0,1]		
		return PlaneCoords[0],PlaneCoords[1]#,z
#------------------------------------------------------------------------------------------------------------------------------
	def ConvertCoordinates_DicomToGrid(self,x,y,z):
		
		i = np.int(np.rint(((x-self.ImagePosition[0])/(self.DirectionX*self.PixelSpacing[0])))) #Index coordinates
		j = np.int(np.rint(((y-self.ImagePosition[1])/(self.DirectionY*self.PixelSpacing[1]))))
		k = np.int(np.rint(((z-self.ImagePosition[2])/(self.DirectionZ*self.SliceSpacing))))

		return i,j,k
#-----------------------------------------------------------------------------------------------------------------------------
