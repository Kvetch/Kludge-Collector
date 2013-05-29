import wmi
class kludgeWMI():
    def __init__(self, wmiAttribs, wmiClass, outputFile, grabHeader):
        file = open(outputFile, 'w')
        c = wmi.WMI()
        wql = "SELECT " + wmiAttribs + " FROM " + wmiClass
        for wmiRecord in c.query(wql):
            header = ''
            wmiRecordValues=''
            if (grabHeader=="True"):
                for thing in wmiRecord.Properties_:
                    header += thing.Name + ","
                    wmiRecordValues += str(thing.Value).replace(","," ") + ","
                grabHeader = "False"
                file.write(header[:-1] + '\n')
                file.write(wmiRecordValues[:-1] + '\n')
            else:
                for thing in wmiRecord.Properties_:
                    wmiRecordValues += str(thing.Value).replace(","," ") + ","
                file.write(wmiRecordValues[:-1] + '\n')
        file.close()
#Get List of Running Processes
wmiGrab = kludgeWMI("*","Win32_Process","ProcessList.csv","True")
#Get Network Adaptor Configuration 
wmiGrab = kludgeWMI("*","Win32_NetworkAdapterConfiguration","NetworkConnections.csv","True")
#Get cached NetLogon Info for User 
wmiGrab = kludgeWMI("*","Win32_NetworkLoginProfile","NetworkLoginProfiles.csv","True")
#Get Computer System Info
wmiGrab = kludgeWMI("*","Win32_ComputerSystem","SystemInfo.csv","True")
#Get Physical Disk Information
wmiGrab = kludgeWMI("*","Win32_DiskPartition","DiskPartition.csv","True")
#Get information on the network adaptors
wmiGrab = kludgeWMI("*","Win32_NetworkAdapter","NetworkAdapter.csv","True")
#Get Operating System Info such as BootDevice, BuildNumber, Service Pack...
wmiGrab = kludgeWMI("*","Win32_OperatingSystem","OperatingSystem.csv","True")
#Get information on installed operating system patches
wmiGrab = kludgeWMI("*","Win32_QuickFixEngineering","Patches.csv","True")
#get information on the state of running services
wmiGrab = kludgeWMI("*","Win32_Service","Services.csv","True")
#enumerate network shares
wmiGrab = kludgeWMI("*","Win32_Share","Shares.csv","True")
#enumerate processes that are scheduled to run at start up
wmiGrab = kludgeWMI("*","Win32_StartupCommand","StartupCommands.csv","True")
#gets list of process IDs for running processes
wmiGrab = kludgeWMI("Handle","Win32_Process","ProcessIDs.txt","False")
#enumerate information on local users
wmiGrab = kludgeWMI("*","Win32_UserAccount WHERE Disabled = 0 AND LocalAccount = 1","LocalUsers.csv","True")
#get logical device information
wmiGrab = kludgeWMI("DeviceID","Win32_logicaldisk","LocalDriveList.txt","True")
#lists the environmental variables for each local user
wmiGrab = kludgeWMI("*","Win32_Environment","EnvironmentVars.csv","True")
