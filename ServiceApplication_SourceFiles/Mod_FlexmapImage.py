# -*- coding: utf-8 -*-
#================================================================================================================
#Liste des choses faire:
#================================================================================================================

#matplotlib.use('gtk')
#from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

#from matplotlib.backends.backend_agg import pyplot as plt

#from matplotlib.pyplot import hist
import numpy as np

import time
#import scipy
#from scipy import ndimage
import sys
import os
from os import path
import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure, show, rc
#from matplotlib.backends.backend_agg import Figure
import Settings
#===============================================================================================================
class FlexmapImage:
	
	def __init__(self, thisSettingsObj):
		
		self.Status = True
		self.SettingsObj = thisSettingsObj# Settings.Settings()

#--------------------------------------------------------------------------------------------------------------------------------------------
	def Execute(self,thisImArray):
		t1 = time.clock()
		#self.GantryAngle = str(thisGantryAngle)
		
		#~ self.GetGantryAngle()
	
		#~ self.ImArray = np.fromfile(self.FilePath,dtype=np.float32)
		#~ self.ImArray = self.ImArray.reshape((1024,1024))

		#self.ImArrayFiltered=ndimage.filters.median_filter(self.ImArray,footprint=np.ones((3,3)))
		#~ self.ImArrayFiltered=self.ImArray
		
		self.ImArrayFiltered = thisImArray
		#Zone de l'image ou doit se trouver le ballbearing
		self.ImArrayBallBearing = self.ImArrayFiltered[462:562,462:562]#[y][x]
		
		#~ plt.imshow(self.ImArrayFiltered,interpolation='none',cmap='gray')
		#~ plt.show()
		#~ sys.exit()
		
		self.Normalisation = 0 #Intensite du 100% du champ de radiation.
		self.LowThreshold = 0  #Intensite de l'image self.ImArrayBallBearing. Toutes les pixels avec des niveaux de gris inférieurs à self.LowThreshold appartienne au Ballbearing.
		
		self.BBXPosi = 0
		self.BBYPosi = 0
		
		#Appel des fonctions
		self.GetThresholds() 	#Fonction pour déterminer self.Normalisation, self.LowThreshold
		self.GetBallBearing()
		
		return np.around(self.BBXPosi,1), np.around(self.BBYPosi,1)
#------------------------------------------------------------------------------------------
	def GetThresholds(self):
		#self.LogFile.write("1")
		PixList = list()
		for i in range(0,self.ImArrayBallBearing.shape[0]):
			for j in range(0,self.ImArrayBallBearing.shape[1]):
				PixList.append(self.ImArrayBallBearing[i][j])
		
		#self.LogFile.write("2")
		#Histogramme des intensit? de niveaux de gris.
		#Figure()
		#plt.figure()
		
		
		#n,bin,patches = plt.hist(PixList,bins=10,normed = 1, facecolor='green')
		#n,bin,patches = hist(PixList,bins=10,normed = 1, facecolor='green')
		#self.LogFile.write("4")
		#print bin
		#plt.show()
		#plt.close()
		#self.LogFile.write("5")
		
		n,bin = np.histogram(PixList,10)
		#self.LogFile.write("3")
		self.LowThreshold = bin[2] #seuil d'intensit? la position du ballbearing : valeur = 1
		self.Normalisation =  (bin[-2] + bin[-1])*0.5 # seuil d'intensit?u champ ouvert.
		
		
		#print "Max Histogramme",bin[-1]
		#print "Normalisation: ",self.Normalisation
		#print "LowThreshold:", self.LowThreshold
#------------------------------------------------------------------------------------------------------------------------------------
	def GetBallBearing(self):
		Xlist = list()
		Ylist = list()

		for y in range(462,562):
			for x in range(462,562):
				if(self.ImArrayFiltered[y][x] <= self.LowThreshold):
					Ylist.append(y)
					Xlist.append(x)

		self.BBXPosiMedian = np.median(Xlist)
		self.BBYPosiMedian = np.median(Ylist)
		self.BBXPosiMoyen = np.mean(Xlist)
		self.BBYPosiMoyen = np.mean(Ylist)
		
		if abs(self.BBXPosiMedian - self.BBXPosiMoyen)<=1:
			self.BBXPosi = self.BBXPosiMoyen
		else:
			self.BBXPosi = self.BBXPosiMedian

		if abs(self.BBYPosiMedian - self.BBYPosiMoyen)<=1:
			self.BBYPosi = self.BBYPosiMoyen
		else:
			self.BBYPosi = self.BBYPosiMedian			
		
		
		#self.BBXPosi = np.rint(self.BBXPosi) #+ 462
		#self.BBYPosi = np.rint(self.BBYPosi) #+ 462
		
		#print 'Ball bearing position X (pixels):',self.BBXPosi
	#	print 'Ball bearing position Y (pixels):',self.BBYPosi

	
		#Show the center of the ballbearing:
		#self.ImArrayBallBearing[np.rint(self.BBYPosi-462)][np.rint(self.BBXPosi-462)]=0
		#self.ImArrayFiltered[np.rint(self.BBYPosi)][np.rint(self.BBXPosi)]=0
		#plt.imshow(self.ImArrayFiltered,interpolation = 'none')
		#plt.imshow(self.ImArrayBallBearing,interpolation = 'none')
		#plt.show()
		
		#May generate a binary image based on threshold if neccessary
				#~ xlist = list()
		#~ ylist = list()
		
		#~ for i in range(0,self.ImArrayBallBearing.shape[0]):
			#~ for j in range(0,self.ImArrayBallBearing.shape[1]):
				#~ if self.ImArrayBallBearing[i,j]<=self.LowThreshold:
					#~ self.BinaryImBallBearing[i,j] = self.BinaryImBallBearing[i,j] 
					#~ xlist.append(j)
					#~ ylist.append(i)
				#~ else:
					#~ self.BinaryImBallBearing[i,j] = 0
					
		#~ xmedian = np.median(xlist)
		#~ ymedian = np.median(ylist)
		#~ xmean = np.mean(xlist)
		#~ ymean = np.mean(ylist)
		#~ print xmedian,ymedian
		#~ print xmean,ymean
		#~ self.BinaryImBallBearing[ymedian,xmedian] = 0
		#~ self.BinaryImBallBearing[ymean,xmean] = 0
		#~ #plt.imshow(self.BinaryImBallBearing)
		#~ plt.imshow(self.ImArrayBallBearing)
		#~ plt.show()
		
		#~ xprofile = list()
		#~ yprofile = list()
		#~ for i in range(0,self.ImArrayBallBearing.shape[1]):
			#~ xprofile.append(np.median(self.ImArrayBallBearingFiltered[ymedian-2:ymedian+2,i]))
			#~ yprofile.append(np.median(self.ImArrayBallBearingFiltered[i,xmedian-2:xmedian+2]))
		
		
		#~ pix = np.arange(0,100)
		#~ print pix
		#~ print xprofile
		#~ print len(xprofile)
		#~ print len(pix)
		#~ plt.plot(pix,xprofile)
		#~ plt.plot(pix,yprofile)
		#~ plt.show()
		
		#plt.imshow(self.ImArrayBallBearing,interpolation = 'none')
		#plt.colorbar()
		#plt.show()		
		
#-----------------------------------------------------------------------------------------------------
#==============================================================================================================================================
if __name__ == "__main__":
	
	#FilePath = os.path.join(os.getcwd(),"118_-37.0.bin")
	#Image(FilePath)
	Image(sys.argv[1],sys.argv[2])
