from distutils.core import setup
import py2exe

import numpy
import scipy

#========================================================================================================================
setup(windows=[{"script":"ClinicalApplication.py","dest_base":"ClinicalApplication"}],


 options = {
	'py2exe': {

		'optimize': 2,
		'dist_dir' : 'ClinicalApplication',
		#~ "packages":["wx","PIL","OpenGL","scipy"],
		"packages":["PIL","OpenGL","scipy"],
		'includes': ['logging'],
		#~ 'excludes': ['scipy',],
		"dll_excludes": ["MSVCP90.dll","OLEACC.dll"],

		}
	},

)
#==========================================================================================================================
#excludes OLEACC.dll is necessary for wxpython. Another method is to delete this dll in the compiled folder.
#Need to excludes MSVCP90.dll. py2exe says: error: [Errno 2] No such file or directory: 'MSVCP90.dll' during compilation