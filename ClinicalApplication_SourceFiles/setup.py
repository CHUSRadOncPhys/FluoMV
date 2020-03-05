
from distutils.core import setup
import py2exe
import numpy
import numpy.core.multiarray
import scipy
import os, os.path

setup(windows=[{"script":"ClinicalApplication.py","dest_base":"ClinicalApplication"}],


 options = {
	'py2exe': {

		'optimize': 2,
		'dist_dir' : 'ClinicalApplication',
		"packages":["wx","PIL","OpenGL","scipy"],
		'includes': ['ctypes','logging','numpy.*',],
		#~ 'excludes': ['scipy',],
		"dll_excludes": ["MSVCP90.dll","OLEACC.dll","API-MS-Win-Security-Base-L1-1-0.dll","API-MS-Win-Core-ProcessThreads-L1-1-0.dll","API-MS-Win-Core-LocalRegistry-L1-1-0.dll", "libopenblas.UWVN3XTD2LSS7SFIFK6TIQ5GONFDBJKU.gfortran-win32.dll",],

		}
	},




)


if os.path.isdir("dist")==True:
	os.rename("dist","ClinicalApplication")
	
