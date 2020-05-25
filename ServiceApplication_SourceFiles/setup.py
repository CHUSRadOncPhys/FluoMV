from distutils.core import setup
import py2exe

import matplotlib

#========================================================================================================================
setup(

windows=[{"script":"ServiceApplication.py","dest_base":"ServiceApplication"}],

data_files=matplotlib.get_py2exe_datafiles(),

options = {
	'py2exe': {        

		'optimize': 2,
		'dist_dir':'ServiceApplication',
		'includes': ['logging'],
		#~ 'excludes': ['OpenGL',],
		"dll_excludes": ["MSVCP90.dll","OLEACC.dll",]
		}
	},

)#End of setup
#==========================================================================================================================
#excludes OLEACC.dll is necessary for wxpython. Another method is to delete this dll in the compiled folder.
#Need to excludes MSVCP90.dll. py2exe says: error: [Errno 2] No such file or directory: 'MSVCP90.dll' during compilation