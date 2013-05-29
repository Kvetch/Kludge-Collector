import subprocess, os, shutil
import variables as var
import logger as log
import sys
from os import getenv

class DirHandler(object):

    def __init__(self):
        self = self
    
    def create_dir(self):
        """ Create collection directory """
        _ofolder = var.outputdir + "/" + os.getenv('COMPUTERNAME') + "-" + var.timestmp
        var.outputdir = _ofolder
        try:
            if not os.path.exists(var.outputdir):
                os.makedirs(var.outputdir)
            else: # If the dir exists, delete it and then create a blank one
                shutil.rmtree(var.outputdir) # Is this slow???
                os.makedirs(var.outputdir)
            self.create_subdirs()
            self.create_errorlog()
        except Exception as e: 
            print(e)
            sys.exit(2)
                
    def create_subdirs(self):
        """ Create collection Sub-directories """
        os.makedirs(var.outputdir + "/Processes")
        os.makedirs(var.outputdir + "/SysInfo")
        os.makedirs(var.outputdir + "/Files")
        os.makedirs(var.outputdir + "/Network")
        os.makedirs(var.outputdir + "/Memory")
        os.makedirs(var.outputdir + "/Logs")
        os.makedirs(var.outputdir + "/Browser")
        os.makedirs(var.outputdir + "/TLN")
        os.makedirs(var.outputdir + "/Software")
        
    def create_errorlog(self):
        """ Create Error Log """
        var.err_file = os.getenv('COMPUTERNAME') + "-" + var.timestmp + "-error.log"
        var.errorlog = open(var.outputdir + "/" + var.err_file, "w")
        var.errorlog.writelines("Kludge Error Log for " + os.getenv('COMPUTERNAME'))
        var.errorlog.writelines("Timestamp is " + var.timestmp)
        var.errorlog.close()
