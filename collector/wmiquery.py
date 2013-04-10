import subprocess, os
import sys
import variables as var
import logger as log
import variables as var
import wmi

# Not sure if we should create a class that accepts class, namespace and properties as args
class KludgeWmi():
	"""	WMI	Queries"""
	def	__init__(self):
		self = self
		w =	wmi.WMI(find_classes=False) # Disable lookups for all the classes in the namespace
		
	def	os_info(self):
		"""	Collect	OS and Machine Information """
		for	os in w.Win32_OperatingSystem():
			print os.Caption
		
	def	process_info(self):
		"""	Collect	Process	Information.  Read up on important properties to call"""
		for	process	in w.Win32_Process ():
			print process.Name,	process.ProcessId, process.ParentProcessId,	process.ExecutablePath,	process.CreationDate, process.Handle, process.HandleCount, process.Priority, process.SessionId,	process.TerminationDate, process.ThreadCount, process.UserModeTime,	process.VirtualSize, process.KernelModeTime, process.WindowsVersion, process.WorkingSetSize, process.WriteOperationCount, process.WriteTransferCount


## Show	all	automatic services which are not running			
#stopped_services =	c.Win32_Service	(StartMode="Auto", State="Stopped")
#if	stopped_services:
#  for s in	stopped_services:
#	 print s.Caption, "service is not running"
#else:
#  print "No auto services stopped"			

## Show	the	percentage free	space for each fixed disk
#for disk in c.Win32_LogicalDisk (DriveType=3):
#  print disk.Caption, "%0.2f%%	free" %	(100.0 * long (disk.FreeSpace) / long (disk.Size))
#
## Show	the	IP and MAC addresses for IP-enabled	network	interfaces
#for interface in c.Win32_NetworkAdapterConfiguration (IPEnabled=1):
#  print interface.Description,	interface.MACAddress
#  for ip_address in interface.IPAddress:
#	 print ip_address
#  print
#
## Startup
#for s in c.Win32_StartupCommand ():
#  print "[%s] %s <%s>"	% (s.Location, s.Caption, s.Command)
#
## List	Registry Keys
#import	_winreg
#import	wmi
#r = wmi.Registry ()
#result, names = r.EnumKey (
#  hDefKey=_winreg.HKEY_LOCAL_MACHINE,
#  sSubKeyName="Software"
#)
#for key in	names:
#  print key
#
## Show	Shares
#for share in c.Win32_Share	():
#  print share.Name, share.Path
#
## Show	Partitions
#for physical_disk in c.Win32_DiskDrive	():
#  for partition in	physical_disk.associators ("Win32_DiskDriveToDiskPartition"):
#	 for logical_disk in partition.associators ("Win32_LogicalDiskToPartition"):
#	   print physical_disk.Caption,	partition.Caption, logical_disk.Caption
#
## Schedule	a Job
#one_minutes_time =	datetime.datetime.now () + datetime.timedelta (minutes=1)
#job_id, result	= c.Win32_ScheduledJob.Create (
#  Command=r"cmd.exe /c	dir	/b c:\ > c:\\temp.txt",
#  StartTime=wmi.from_time (one_minutes_time)
#)
#print job_id
#for line in os.popen ("at"):
#  print line
#  
## Find	Drive Types
#for drive in c.Win32_LogicalDisk ():
#  print drive.Caption,	DRIVE_TYPES[drive.DriveType]
#
## List	NameSpaces
#def enumerate_namespaces (namespace=u"root", level=0):
#  print level * "	", namespace.split ("/")[-1]
#  c = wmi.WMI (namespace=namespace)
#  for subnamespace	in c.__NAMESPACE ():
#	 enumerate_namespaces (namespace + "/" + subnamespace.Name,	level +	1)
#enumerate_namespaces ()

#	
#	def	get_uptime(computer, user, password):
#	 c = wmi.WMI(find_classes=False, computer=computer,	user=user, password=password)
#	 secs_up = int([uptime.SystemUpTime	for	uptime in c.Win32_PerfFormattedData_PerfOS_System()][0])
#	 hours_up =	secs_up	/ 3600
#	 return	hours_up
		
#		def	get_cpu(computer, user,	password):
#	 c = wmi.WMI(find_classes=False, computer=computer,	user=user, password=password)
#	 utilizations =	[cpu.LoadPercentage	for	cpu	in c.Win32_Processor()]
#	 utilization = int(sum(utilizations) / len(utilizations))  # avg all cores/processors
#	 return	utilization
# 
#	 
#def get_mem_mbytes(computer, user,	password):
#	 c = wmi.WMI(find_classes=False, computer=computer,	user=user, password=password)
#	 available_mbytes =	int([mem.AvailableMBytes for mem in	c.Win32_PerfFormattedData_PerfOS_Memory()][0])
#	 return	available_mbytes
# 
# 
#def get_mem_pct(computer, user, password):
#	 c = wmi.WMI(find_classes=False, computer=computer,	user=user, password=password)
#	 pct_in_use	= int([mem.PercentCommittedBytesInUse for mem in c.Win32_PerfFormattedData_PerfOS_Memory()][0])
#	 return	pct_in_use

#import	win32com.client
#strComputer = "."
#objWMIService = win32com.client.Dispatch("WbemScripting.SWbemLocator")
#objSWbemServices =	objWMIService.ConnectServer(strComputer,"root\cimv2")
#colItems =	objSWbemServices.ExecQuery("Select * from Win32_ProgIDSpecification")
#for objItem in	colItems:
#	 print "Caption: ",	objItem.Caption
#	 print "Check ID: ", objItem.CheckID
#	 print "Check Mode:	", objItem.CheckMode
#	 print "Description: ",	objItem.Description
#	 print "Name: ", objItem.Name
#	 print "Parent:	", objItem.Parent
#	 print "ProgID:	", objItem.ProgID
#	 print "Software Element ID: ",	objItem.SoftwareElementID
#	 print "Software Element State:	", objItem.SoftwareElementState
#	 print "Target Operating System: ",	objItem.TargetOperatingSystem
#	 print "Version: ",	objItem.Version
#	 print "-------------------------------------------------------------------\n"

import win32com.client
strComputer	= "."
objWMIService =	win32com.client.Dispatch("WbemScripting.SWbemLocator")
objSWbemServices = objWMIService.ConnectServer(strComputer,"root\cimv2")
colItems = objSWbemServices.ExecQuery("Select *	from Win32_Environment")
for	objItem	in colItems:
	print "Caption:	", objItem.Caption
	print "Description:	", objItem.Description
	print "Install Date: ",	objItem.InstallDate
	print "Name: ",	objItem.Name
	print "Status: ", objItem.Status
	print "System Variable:	", objItem.SystemVariable
	print "User	Name: ", objItem.UserName
	print "Variable	Value: ", objItem.VariableValue

