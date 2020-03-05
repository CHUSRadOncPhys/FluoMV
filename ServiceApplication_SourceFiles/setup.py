from distutils.core import setup
import py2exe
import numpy
import numpy.core.multiarray
import matplotlib
import os, os.path
setup(windows=[{"script":"ServiceApplication.py","dest_base":"ServiceApplication"}],

data_files=matplotlib.get_py2exe_datafiles(),

 options = {
 'py2exe': {'optimize': 2,'dist_dir':'ServiceApplication','includes': [ 'ctypes','logging','numpy.*',],'excludes': ['OpenGL',],"dll_excludes": ["MSVCP90.dll","OLEACC.dll","API-MS-Win-Security-Base-L1-1-0.dll","API-MS-Win-Core-ProcessThreads-L1-1-0.dll","API-MS-Win-Core-LocalRegistry-L1-1-0.dll", "libopenblas.UWVN3XTD2LSS7SFIFK6TIQ5GONFDBJKU.gfortran-win32.dll",],

		}
	},

)


if os.path.isdir("dist")==True:
    os.rename("dist","ServiceApplication")