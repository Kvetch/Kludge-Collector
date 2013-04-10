import subprocess, os
import variables as var
import logger as log

# Still needs work.  No clue on the best method to handle the buffer and stdout
class CmdLnr(object):

    def __init__(self):
        self = self
    
    def run_acmd(self,cmdargs,ofile):
        self = self
        cmdargs = str(cmdargs)
        _ofile = ofile
        if os.path.exists(var.outputdir + "/" + _ofile):
            self.outputfile = open(var.outputdir + "/" + _ofile, "a")
        else:
            self.outputfile = open(var.outputdir + "/" + _ofile, "w")
        
        try:
            proc = subprocess.Popen(str(cmdargs), bufsize=-1, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        except:
            if var.log:
                log.logger.debug
            pass
        
        try:
            # Read from pipes
            # for line in proc.stdout:
            if var.verbose:
                print("Running the command " + cmdargs + " outputting to " + _ofile)            
            self.outputfile.writelines(proc.communicate()) # Should we comma delim output?
#            if proc.returncode != 0:
#                var.errorlog = open(var.outputdir + "/" + var.err_file, "a")
#                var.errorlog.writelines(proc.communicate())
#                print(proc.communicate())

        except:
            if var.log:
                log.logger.debug
            pass
