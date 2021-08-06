import os

from remembrance.injection.dll import DLLLoadLibraryMethod
from remembrance.process import Process, ProcessAccessRights

notepad = Process.by_name("notepad.exe")
notepad.open(ProcessAccessRights.PROCESS_ALL_ACCESS)

notepad.inject_dll(DLLLoadLibraryMethod, os.path.join(os.getcwd(), "examples/assets/MessageBox64.dll"))

notepad.close()
