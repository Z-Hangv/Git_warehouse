set ws=wscript.createobject("wscript.shell") 
Set objArgs = WScript.Arguments
ws.run "python.exe task_script.py "+ objArgs(0)+" "+ objArgs(1) +" "+ objArgs(2) + " /start",0
