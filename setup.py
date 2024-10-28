import cx_Freeze
import sys
import os 
base = None

if sys.platform == 'win32':
    base = "Win32GUI"

os.environ['TCL_LIBRARY'] = r"C:\Users\user\AppData\Local\Programs\Python\Python311\tcl\tcl8.6"
os.environ['TK_LIBRARY'] = r"C:\Users\user\AppData\Local\Programs\Python\Python311\tcl\tk8.6"

executables = [cx_Freeze.Executable("gui.py", base=base, icon="icon.ico")]


cx_Freeze.setup(
    name = "Activity Monitor",
    options = {"build_exe": {"packages":["os","time","shutil","watchdog","socket","psutil","tkinter","plyer"], "include_files":["icon.ico",'tcl86t.dll','tk86t.dll']}},
    version = "0.02",
    description = "Activity Monitor for monitor system files",
    executables = executables
    )