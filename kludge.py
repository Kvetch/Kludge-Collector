#!/usr/bin/python
import sys
import getopt
import time
import os
sys.path.append('collector')
import constants as constants
import variables as var
import collectstuff as collect

if sys.version_info < (2, 6, 0) and sys.version_info > (3, 0, 0): # This probably isn't needed if we py2exe
    sys.stderr.write("A minimium of Python 2.6.0 is required.  Python 3.0.0 has not been fully tested.")
    sys.exit(1)

class KludgeCollector:
    def __init__(self):
        self = self
        var.KludgeVars()
        self.main(sys.argv[1:])

    def printit(self):
        opts, args = getopt.getopt(sys.argv[1:], "milqfeavrho:e:", ["help", "memory", "inline", "logs", "quick", "full", "email", "hashing", "verbose", "errorlog", "outputdir",    "encrypt"])
        print ("Running Kludge with " + str(sys.argv) + " on " + os.getenv('COMPUTERNAME'))
        print "\tPress CTRL/C to cancel in ",
        for i in range(5):
            print str(5 - i) + " ",
            sys.stdout.flush()
            time.sleep(1)
#       for opt in sys.argv[1:]:
#           print opt
#           print var.level
            
    def running(self):
        print("running")
        collect.CollectStuff()

    def usage(self):
        print "Usage: kludge.py [Options]"
        print "Ex: python kludge.py -m -f -o /tmp --verbose"
        print "\t  -m/--memory: Collect Memory"
        print "\t  -i/--inline: Perform inline Memory Data Collection"
        print "\t  -l/--logs: Collect Log Files"
        print "\t  -q/--quick: Preliminary Quick Data Collection"
        print "\t  -f/--full: Full Data Collection"
        print "\t  -e/--email:    Collect email files"
        print "\t  -a/--hashing:  MD5/SHA1 hashing"
        print "\t  -v/--verbose: Verbose Output"
        print "\t  -r/--errorlog: Log Kludge"
        print "\t  -o/--outputdir <output dir>: Output Directory"
        print "\t  -c/--encrypt <passphrase>: Encryption Passphrase"
        print "\t  -h/--help: Help"
        
    def manpage(self):
        #print __doc__
        #print "Extended Help"
        print "Usage: kludge.py [Options]"
        print "\t  -m/--memory: Collect Memory"
        print "\t         This option will perform a win32/64dd dump of memory"
        print "\t  -i/--inline: Perform inline Memory Data Collection"
        print "\t         This option is currently not implemented"
        print "\t  -l/--logs: Collect Log Files"
        print "\t         This option will collect Event Logs"
        print "\t  -q/--quick: Preliminary Quick Data Collection"
        print "\t         This option will perform a shorter cursory collection of data"
        print "\t  -f/--full: Full Data Collection"
        print "\t         This option will collect as much data as possible"
        print "\t  -e/--email:    Collect email files"
        print "\t         This option will collect .pst, .ost, .nsf and .oab files"
        print "\t  -a/--hashing:  MD5/SHA1 hashing"
        print "\t         This option will perform md5 and sha1 hashing of the Windows directory along with the user home directories"
        print "\t  -v/--verbose: Verbose Output"
        print "\t         Verbose Screen Output"
        print "\t  -r/--errorlog: Log Kludge"
        print "\t         This option will log Kludge's activities and errors"
        print "\t  -o/--outputdir <output dir>: Output Directory"
        print "\t         To override the standard output directory of C:\\Windows\\temp"
        print "\t  -c/--encrypt <passphrase>: Encryption Passphrase"
        print "\t         This option is currently not implemented"
        print "\t  -h/--help: The standard smart alec response of \"You're Looking at it\""
        print "Example: python kludge.py -m -f -o /tmp --verbose"
    
    def main(self,argv):
        sys.stderr.write("Kludge {0}".format(constants.VERSION) + "\t(https://github.com/Kvetch/)\n")
        sys.stderr.flush()
        try:
            opts, args = getopt.getopt(argv, "milqfeavrho:e:", ["help", "memory", "inline", "logs", "quick", "full", "email", "hashing", "verbose", "errorlog", "outputdir",    "encrypt"])
        except getopt.GetoptError as err:
            print(err)
            self.usage()
            sys.exit(2)
        
        # If there are no arguments print the help
        if len(sys.argv) == 1:
            self.usage()
            sys.exit()
            
        for opt, arg in opts:
            # If opt is help print the help
            if opt in ("-h", "--help"):
                self.manpage()
                sys.exit()
            elif opt in ('-m', "--memory"):
                var.memory = 1
            elif opt in ('-i', "--inline"):
                var.memory = 1
            elif opt in ('-l', "--logs"):
                var.varlogs = 1
            elif opt in ('-r', "--errorlog"):
                var.log = 1
            elif opt in ('-q', "--quick"):
                var.level = 1
            elif opt in ('-f', "--full"):
                var.level = 2
            elif opt in ('-e', "--email"):
                var.mail =  1
            elif opt in ('-a', "--hashing"):
                var.hashing =   1
            elif opt in ('-v', "--verbose"):
                var.verbose = 1
            elif opt in ("-o", "--outputdir"):
                var.output = 1
                var.outputdir = str(arg)
            elif opt in ("-c", "--encrypt"):
                var.encryption = 1
                var.passphrase = str(arg)
                
                #options = "".join(args)

#       if __name__ == "__main__":
#           main(sys.argv[1:])

x = KludgeCollector()
x.printit()
x.running() 
            
