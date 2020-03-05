import numpy as np
import time
from multiprocessing import Process
import multiprocessing
from skimage import measure
import os

class intersectCPU:
	def __init__(self,ThisFilePath,isocenter,refPointCT,sens,resolution,Dim,id_Patient,SelectedStructures,thread=4):
		
		thread = int(np.sqrt(thread))
		self.PanelNbPixels_o = 512
		self.PanelNbPixels = self.PanelNbPixels_o/thread
		self.PixDimEPID = 0.252*1024/self.PanelNbPixels_o*1.6
		self.resolution = np.array(resolution)
		self.Pi = np.pi
		NbAngles = 720
		ResultFile = open(os.path.join(ThisFilePath,"StructureProjection","Results.txt"),"w")
		ResultFile.write(str(len(SelectedStructures))+"\t\n")
		ResultFile.write(str(NbAngles)+"\n")		
		CentroidFile = open(os.path.join(ThisFilePath,"StructureProjection","Centroid.txt"),"w")
		for RoiName in SelectedStructures:
			
			ResultFile.write(RoiName+"\n")
			CentroidFile.write(RoiName+"\n")
			
			b = np.fromfile(os.path.join(ThisFilePath,"ROIs",id_Patient+"."+RoiName),dtype=np.uint8)
			self.Label = b.reshape((Dim[2],Dim[0],Dim[1]))
			
			LabelShape = self.Label.shape
			self.NbRows = LabelShape[1]
			self.NbCols = LabelShape[2]
			self.NbSlices =  LabelShape[0]
			
			nZ = np.nonzero(self.Label)
			Zmin = min(nZ[0])
			Zmax = max(nZ[0])
			Ymin = min(nZ[1])
			Ymax = max(nZ[1])
			Xmin = min(nZ[2])
			Xmax = max(nZ[2])
			
			lenz = Zmax-Zmin +1
			leny = Ymax-Ymin +1
			lenx = Xmax-Xmin +1
			z = np.ones((lenz,self.PanelNbPixels,self.PanelNbPixels),dtype = np.int64)
			zpos = np.array(range(Zmin,Zmax+1))
			self.zL = zpos[:,None,None]*z
			y = np.ones((leny,self.PanelNbPixels,self.PanelNbPixels),dtype = np.int64)
			ypos = np.array(range(Ymin,Ymax+1))
			self.yL = ypos[:,None,None]*y
			x = np.ones((lenx,self.PanelNbPixels,self.PanelNbPixels),dtype = np.int64)
			xpos = np.array(range(Xmin,Xmax+1))
			self.xL = xpos[:,None,None]*x
			
			self.offsetX_dicom = (isocenter[0] - refPointCT[0])*sens[0]
			self.offsetY_dicom = (isocenter[1] - refPointCT[1])*sens[1]
			self.offsetZ_dicom = (isocenter[2] - refPointCT[2])*sens[2]+(self.NbSlices-1)*self.resolution[2]
			
			self.x_mm = self.xL.astype(np.float32)*self.resolution[0] - self.offsetX_dicom
			self.y_mm = self.yL.astype(np.float32)*self.resolution[1] - self.offsetY_dicom
			self.z_mm = self.zL.astype(np.float32)*self.resolution[2] - self.offsetZ_dicom			
			
			self.x_target,self.y_target = np.meshgrid(range(self.PanelNbPixels),range(self.PanelNbPixels))

			self.sourcePoint = [0.0,0.0,0.0]

			t1 = time.time()
			
			for A in range(NbAngles):
				t3 = time.time()
				self.BeamAngle = A*0.5
				print "Angle = ",self.BeamAngle
				
				self.sourcePoint[0] = 1000 * np.sin(self.BeamAngle*self.Pi / 180.0)
				self.sourcePoint[1] = -1000 * np.cos(self.BeamAngle*self.Pi / 180.0)
				self.sourcePoint[2] = 0.0
				
				self.im_EPID = np.zeros((self.PanelNbPixels_o,self.PanelNbPixels_o),dtype = np.uint8)
				arr1 = multiprocessing.Array('i',self.PanelNbPixels*self.PanelNbPixels)
				arr2 = multiprocessing.Array('i',self.PanelNbPixels*self.PanelNbPixels)
				arr3 = multiprocessing.Array('i',self.PanelNbPixels*self.PanelNbPixels)
				arr4 = multiprocessing.Array('i',self.PanelNbPixels*self.PanelNbPixels)
				p1 = Process(target=self.intersect, args=(0,0,arr1,))
				p1.start()
				p2 = Process(target=self.intersect, args=(0,1,arr2,))
				p2.start()
				p3 = Process(target=self.intersect, args=(1,0,arr3,))
				p3.start()
				p4 = Process(target=self.intersect, args=(1,1,arr4,))
				p4.start()
				
				p1.join()
				p2.join()
				p3.join()
				p4.join()
				
				self.im_EPID[0:self.PanelNbPixels,0:self.PanelNbPixels] = np.array(arr1).reshape((self.PanelNbPixels,self.PanelNbPixels))
				self.im_EPID[self.PanelNbPixels:2*self.PanelNbPixels,0:self.PanelNbPixels] = np.array(arr2).reshape((self.PanelNbPixels,self.PanelNbPixels))
				self.im_EPID[0:self.PanelNbPixels,self.PanelNbPixels:2*self.PanelNbPixels] = np.array(arr3).reshape((self.PanelNbPixels,self.PanelNbPixels))
				self.im_EPID[self.PanelNbPixels:2*self.PanelNbPixels,self.PanelNbPixels:2*self.PanelNbPixels] = np.array(arr4).reshape((self.PanelNbPixels,self.PanelNbPixels))
				
				nz = self.im_EPID.nonzero()
				CentroidX = np.mean([nz[1]])
				CentroidY = np.mean([nz[0]])
				
				CentroidFile.write(str(self.BeamAngle)+"\t"+str(CentroidX)+"\t"+str(CentroidY)+"\n")
				
				contours = measure.find_contours(self.im_EPID, 0.99)
				
				t4 = time.time()
				print (t4-t3)*720/60.0

				for point in contours[0]:
					ResultFile.write(str(round(point[1])*256.0/self.PanelNbPixels_o)+"\t"+str(round(511-point[0])*256.0/self.PanelNbPixels_o)+"\t")
				
				ResultFile.write("\n")
			
			t2 = time.time()
			print t2-t1
		
		ResultFile.close()
		CentroidFile.close()




	def intersect(self,ii,jj,arr):
		x_target_ii = self.x_target + ii*self.PanelNbPixels
		y_target_jj = self.y_target + jj*self.PanelNbPixels
		
		ai = (x_target_ii-self.PanelNbPixels_o/2+0.5)*self.PixDimEPID
		aj = (y_target_jj-self.PanelNbPixels_o/2+0.5)*self.PixDimEPID

		targetpoint0 = np.cos(self.BeamAngle*self.Pi/180)*ai-np.sin(self.BeamAngle*self.Pi/180)*600
		targetpoint1 = np.sin(self.BeamAngle*self.Pi/180)*ai+np.cos(self.BeamAngle*self.Pi/180)*600
		targetpoint2 = aj
		
		# x=ax*z+bx,  y=ay*z+by
		azx = (targetpoint0-self.sourcePoint[0])/(targetpoint2-self.sourcePoint[2])
		bzx = self.sourcePoint[0]-azx*self.sourcePoint[2]
		azy = (targetpoint1-self.sourcePoint[1])/(targetpoint2-self.sourcePoint[2])
		bzy = self.sourcePoint[1]-azy*self.sourcePoint[2]
		
		x_intersectZ = (np.round(((self.z_mm*azx+bzx)+self.offsetX_dicom)/self.resolution[0])).astype(np.int)
		y_intersectZ = (np.round(((self.z_mm*azy+bzy)+self.offsetY_dicom)/self.resolution[1])).astype(np.int)
		
		ayx = (targetpoint0-self.sourcePoint[0])/(targetpoint1-self.sourcePoint[1])
		byx = self.sourcePoint[0]-ayx*self.sourcePoint[1]
		ayz = (targetpoint2-self.sourcePoint[2])/(targetpoint1-self.sourcePoint[1])
		byz = self.sourcePoint[2]-ayz*self.sourcePoint[1]
		
		x_intersectY = (np.round(((self.y_mm*ayx+byx)+self.offsetX_dicom)/self.resolution[0])).astype(np.int)
		z_intersectY = (np.round(((self.y_mm*ayz+byz)+self.offsetZ_dicom)/self.resolution[2])).astype(np.int)
		
		axy = (targetpoint1-self.sourcePoint[1])/(targetpoint0-self.sourcePoint[0])
		bxy = self.sourcePoint[1]-axy*self.sourcePoint[0]
		axz = (targetpoint2-self.sourcePoint[2])/(targetpoint0-self.sourcePoint[0])
		bxz = self.sourcePoint[2]-axz*self.sourcePoint[0]
		
		y_intersectX = (np.round(((self.x_mm*axy+bxy)+self.offsetY_dicom)/self.resolution[1])).astype(np.int)
		z_intersectX = (np.round(((self.x_mm*axz+bxz)+self.offsetZ_dicom)/self.resolution[2])).astype(np.int)

		TF = (self.xL >= 0)*(self.xL < self.NbRows)*(y_intersectX >= 0)*(y_intersectX < self.NbCols)*(z_intersectX >= 0)*(z_intersectX < self.NbSlices)
		y_intersectX *=TF
		self.xL *=TF
		z_intersectX *=TF
		
		Res = self.Label[z_intersectX,y_intersectX,self.xL].max(axis=0)
		
		TF = (x_intersectY >= 0)*(x_intersectY < self.NbRows)*(self.yL >= 0)*(self.yL < self.NbCols)*(z_intersectY >= 0)*(z_intersectY < self.NbSlices)
		x_intersectY *=TF
		self.yL *=TF
		z_intersectY *=TF
		
		Res += self.Label[z_intersectY,self.yL,x_intersectY].max(axis=0)

				

		TF = (x_intersectZ >= 0)*(x_intersectZ < self.NbRows)*(y_intersectZ >= 0)*(y_intersectZ < self.NbCols)*(self.zL >= 0)*(self.zL < self.NbSlices)
		
		x_intersectZ *=TF
		self.zL *=TF
		y_intersectZ *=TF
		
		
		Res += self.Label[self.zL,y_intersectZ,x_intersectZ].max(axis=0)

		Res = (Res>0).reshape((self.PanelNbPixels*self.PanelNbPixels))
		arr[:] = Res[:]
		