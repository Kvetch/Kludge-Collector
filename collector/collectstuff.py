import subprocess, os
import variables as var
import logger as log
import cmdlnr as cmdlnr
import dirhandler as dirhandlr
import hasher as hasher

class CollectStuff(object):
    """ Start Collection of Data """
    def __init__(self):
        self = self
        dir = dirhandlr.DirHandler()    # Call Directory creation
        dir.create_dir()
        self.collector()
        
# RE-ORDER CMDS TO COLLECT IN ORDER OF VOLATILITY
# Processes, SysInfo, Files, Network, Memory, Logs, Browser, TLN, Software
    def collector(self):
        command = cmdlnr.CmdLnr()
        command.run_acmd("set", "SysInfo\\env.txt")
        command.run_acmd("schtasks.exe \/query", "Processes\\schtasks.txt")
        command.run_acmd("at", "Processes\\at.txt")
        command.run_acmd("tasklist", "Processes\\tasklist.txt")
        command.run_acmd("doskey \/history", "SysInfo\\doskey.txt")
        command.run_acmd("netstat -bona", "Network\\netstat.txt")
        command.run_acmd("ipconfig \/displaydns | findstr \"Name Live Host\"", "Network\\dns.txt")
        command.run_acmd("ipconfig \/all", "Network\\ipconfig.txt")
        command.run_acmd("arp -a", "Network\\arp.txt")
        command.run_acmd("route print", "Network\\routes.txt")
        command.run_acmd("netsh.exe firewall show state", "Network\\firewall.txt")
        command.run_acmd("netsh firewall show service", "Network\\firewall-state.txt")
        command.run_acmd("net use", "Network\\netbios.txt")
        command.run_acmd("nbtstat -nrSsc", "Network\\NBTStat.txt")
        command.run_acmd("net sessions", "Network\\netbios-sessions.txt")

# Hashing test
        hashit = hasher.KludgeHasher()
        hashit.dirhasher("C:\\Users\\")
        
#        for r,d,f in os.walk("/dev"): # Find disks
#            for files in f:
#                if files.startswith("disk"):
#                    _filename = os.path.join(r, files)
#                    command.run_acmd("diskutil info " + _filename, "SysInfo/" + files + "-info.txt")
#                    command.run_acmd("diskutil list " + _filename, "SysInfo/" + files + "-list.txt")
#                    # command.run_acmd("pdisk " + _filename + " -dump", "SysInfo/" + files + "-Partition.txt")
#                    command.run_acmd("hdiutil pmap " + _filename, "SysInfo/" + files + "-info2.txt")
#                
#        if var.level == 2:
#            command.run_acmd("ls -liRhT /", "Files/file-listing.txt")
#            
#            for r,d,f in os.walk("/Users"): # Find certain types of file info - dmg, plist...
#                for files in f:
#                    if files.endswith(".dmg"):
#                        _filename = os.path.join(r, files)
#                        command.run_acmd("hdiutil imageinfo " + _filename, "Software/" + files + "-info.txt")
#                    elif files.endswith(".plist"):
#                        _filename = os.path.join(r, files)
#                        command.run_acmd("plutil -p " + _filename, "Software/" + files + "-info.txt")
