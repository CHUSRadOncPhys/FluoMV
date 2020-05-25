# -*- coding: utf-8 -*-
import numpy as np
import sys
import os
#===============================================================================================================
class FlexmapImage:
	
	def __init__(self, thisSettingsObj):
		
		self.Status = True
		self.SettingsObj = thisSettingsObj

#--------------------------------------------------------------------------------------------------------------------------------------------
	def Execute(self,thisImArray):
		
		self.ImArrayFiltered = thisImArray
		#Zone de l'image ou doit se trouver le ballbearing
		self.ImArrayBallBearing = self.ImArrayFiltered[462:562,462:562]#[y][x]
			
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

		PixList = list()
		for i in range(0,self.ImArrayBallBearing.shape[0]):
			for j in range(0,self.ImArrayBallBearing.shape[1]):
				PixList.append(self.ImArrayBallBearing[i][j])
				
		n,bin = np.histogram(PixList,10)
		self.LowThreshold = bin[2] #Approximation for the gray level of the BB
		self.Normalisation =  (bin[-2] + bin[-1])*0.5 # Approximation for the gray level at the center of the field

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
		
		
		#print 'Ball bearing position X (pixels):',self.BBXPosi
		#print 'Ball bearing position Y (pixels):',self.BBYPosi
#==============================================================================================================================================
