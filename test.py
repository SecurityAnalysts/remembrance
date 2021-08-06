from remembrance.process import Process, ProcessAccessRights

notepad = Process.by_name("notepad.exe")
notepad.open(ProcessAccessRights.PROCESS_ALL_ACCESS)

notepad.close()
