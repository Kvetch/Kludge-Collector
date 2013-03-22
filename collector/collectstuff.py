import subprocess, os
import variables as var
import logger as log
import cmdlnr as cmdlnr
import dirhandler as dirhandlr

class CollectStuff(object):
    """ Start Collection of Data """
    def __init__(self):
        self = self
        dir = dirhandlr.DirHandler()    # Call Directory creation
        dir.create_dir()
        self.collector()
        
# RE-ORDER CMDS TO COLLECT IN ORDER OF VOLATILITY
# Procs, SysInfo, Network, Memory, Logs, Browser, TLN, Software
    def collector(self):
        command = cmdlnr.CmdLnr()
        command.run_acmd("ps -ef", "Procs/ps.txt")
        command.run_acmd("crontab -l", "Procs/crontab.txt")
        
        for r,d,f in os.walk("/dev"): # Find disks
            for files in f:
                if files.startswith("disk"):
                    _filename = os.path.join(r, files)
                    command.run_acmd("diskutil info " + _filename, "SysInfo/" + files + "-info.txt")
                    command.run_acmd("diskutil list " + _filename, "SysInfo/" + files + "-list.txt")
                    # command.run_acmd("pdisk " + _filename + " -dump", "SysInfo/" + files + "-Partition.txt")
                    command.run_acmd("hdiutil pmap " + _filename, "SysInfo/" + files + "-info2.txt")
                
        if var.level == 2:
            command.run_acmd("ls -liRhT /", "Files/file-listing.txt")
			
			for	r,d,f in os.walk("/Users"):	# Find certain types of	file info -	dmg, plist...
				for	files in f:
					if files.endswith(".dmg"):
						_filename =	os.path.join(r,	files)
						command.run_acmd("hdiutil imageinfo	" +	_filename, "Software/" + files + "-info.txt")
					elif files.endswith(".plist"):
						_filename =	os.path.join(r,	files)
						command.run_acmd("plutil -p	" +	_filename, "Software/" + files + "-info.txt")