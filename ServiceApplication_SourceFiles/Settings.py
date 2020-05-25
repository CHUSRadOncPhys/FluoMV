import os
from datetime import datetime

class Settings:
	def __init__(self):

		self.ClearLogs()
		self.LoadSettings() #Load the parameter in "C:\EPID","settings.txt"
		self.CreateFolders()
		self.MyLog("__init__",str(os.getcwd()),level=2)
#--------------------------------------------------------------------------------------------------------------------------------------------
	def ClearLogs(self):
		fpath = os.path.join("C:\EPID","Logs","Settings.log")
		if os.path.isfile(fpath)==True:        
			try:
				os.remove(fpath)
			except:
				pass
#--------------------------------------------------------------------------------------------------------------------------------------------
	def MyLog(self,mess="none",value="none",level=0):
			
		if level<=self.debugLvl:
			f = open(os.path.join("C:\EPID","Logs","Settings.log"),"a")
			f.write(str(mess)+"\t"+str(value)+"\t"+str(datetime.now())+"\n")
			f.close()
#-----------------------------------------------------------------------------------------------------------------------------------------------
	def CreateFolders(self):
		if os.path.isdir(os.path.join(self.ROOTPATH,"CalibrationFiles"))==False:
			os.mkdir(os.path.join(self.ROOTPATH,"CalibrationFiles"))

		if os.path.isdir(os.path.join(self.ROOTPATH,"EPID_Listening"))==False:
			os.mkdir(os.path.join(self.ROOTPATH,"EPID_Listening"))

		if os.path.isdir(os.path.join(self.ROOTPATH,"SavePNG"))==False:
			os.mkdir(os.path.join(self.ROOTPATH,"SavePNG"))

		if os.path.isdir(os.path.join(self.ROOTPATH,"SaveRAW"))==False:
			os.mkdir(os.path.join(self.ROOTPATH,"SaveRAW"))

		if os.path.isdir(os.path.join(self.ROOTPATH,"Logs"))==False:
			os.mkdir(os.path.join(self.ROOTPATH,"Logs"))
			
#---------------------------------------------------------------------------------------------------------------------------------------------
	def LoadSettings(self):
		
		f = open(os.path.join("C:\EPID","settings.txt"),"r")
		lines = f.readlines()
		f.close()
		lines = filter(None,lines)
		dict = {}
		for l  in lines:
			if l.find("#")!=-1:
				l = l.split("#")
				l=l[0]
			l=l.replace(" ","")
			l=l.replace("\t","")
			l=l.replace("\n","")
			vars = l.split("=")
			#print vars
			dict[vars[0]] = vars[1]
		
		self.ROOTPATH = dict["root_path"] 
		self.debugLvl = int(dict["DebugLevel"])
		
		if dict["SavePNG"]=="True":
			self.SAVEPNG = True
		else:
			self.SAVEPNG = False

		if dict["SaveRAW"]=="True":
			self.SAVERAW = True
		else:
			self.SAVERAW = False

