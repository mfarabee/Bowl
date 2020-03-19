from distutils.core import setup
import py2exe

setup(
    # The first three parameters are not required, if at least a
    # 'version' is given, then a versioninfo resource is built from
    # them and added to the executables.
    version = "1.0.0",
    options= {"py2exe": { 
        'dll_excludes': ['libgdk-win32-2.0-0.dll', 'libgobject-2.0-0.dll',"msvcp90.dll"],
        },
    },

    # targets to build
    #console = ["bowl_tk.py"],
    windows = ["bowl_tk.py"],
    )
