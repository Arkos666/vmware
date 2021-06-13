import subprocess
import os
from winregistry import WinRegistry as Reg
from ping3 import ping, verbose_ping
import time
import sys
import glob

dirMachine = r'C:\Users\arkos\Documents\Virtual Machines\Debian 10.x 64-bit'
sMachine ="Debian 10.x 64-bit.vmx"
ip_vmware = "192.168.1.138"

def getPuttyDir():
    #CASE GET FROM PROGRAM FILES
    putty_file = "putty.exe"
    path = os.environ["ProgramFiles"] + os.path.sep
    # Extract the list of filenames
    files = glob.glob(path + '*[Pp][Uu][Tt][Tt][Yy]', recursive=False)
     
    # Loop to print the filenames
    for filename in files:
        print(filename)
        return filename + os.path.sep + putty_file
    
    return None

def getVmwareDir():
    vmrun_file = "vmrun.exe"
    VMWare = "vmplayer"
    #CASE GET FROM HKLM\SOFTWARE\Microsoft\Windows\Windows\Installer\Folders
    regVmware = r"HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths" + os.path.sep #\Windows\Installer\Folders"  + os.path.sep
    
    reg = Reg()
    reg_key = reg.read_key(regVmware)
    #print(reg_key)
    
    for key in reg_key['keys']:
        #print(key.lower())
        if VMWare.lower() in str(key).lower():
            regVmware = regVmware + os.path.sep + key + os.path.sep
            reg_key_vm = reg.read_key(regVmware)

            for key_value in reg_key_vm['values']:
                if (key_value['value'] == 'Path'):
                    path_vmrun = key_value['data'] + vmrun_file
                    if os.path.isfile(path_vmrun ):
                        return path_vmrun
    return None
    
    
#FIRST WE FIND THE VMWARE PATH
vmware_path = getVmwareDir()

if vmware_path == None:
    print ('vmware dir not found')
    exit()

#HERE WE LAUNCH THE WMWARE
vmPathQuotes="\"" + vmware_path + "\""
vmMachine = "\"" + dirMachine + os.path.sep + sMachine + "\""
vmCommand = "start"
vmParameters = "-T wp"

s = vmPathQuotes + " " + vmParameters + " " + vmCommand + " " + vmMachine
print(s)
#return_code = subprocess.call([vmPath, vmParameters, vmCommand, vmMachine])
return_code = subprocess.call(s)

#WE'RE GOING TO VIEW IF IP IS RESPONDING DURING 120 SEC

t_end = time.time() + 60 * 2
sec = 110
print ("pinging during: " + str(sec) + " seconds")

toolbar_width = sec

# setup toolbar
sys.stdout.write("[%s]" % (" " * toolbar_width))

sys.stdout.flush()
sys.stdout.write("\b" * (toolbar_width+1)) # return to start of line, after '['

while time.time() < t_end:
    #sys.stdout.write("-")
    if not int(t_end - time.time()) == sec:
        sec = int(t_end - time.time())
        sys.stdout.write("-")
        sys.stdout.flush()
        response = ping(ip_vmware)  # Returns delay in seconds.
        if isinstance(response, float):
            response = True
            break
        
if not response:
    print("Timeout to " + ip_vmware)
    exit()
sys.stdout.write("]\n")

putty = getPuttyDir() + " -load \"debian\""
return_code = subprocess.call(putty)

exit()

