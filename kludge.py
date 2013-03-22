#!/usr/bin/python

import sys
import getopt
import time
import os
sys.path.append('collector')
import constants as	constants
import variables as	var
import collectstuff	as collect
# collect memory = -m
# collect logs = -l
# preliminary fast collection =	-L1
# deep collection =	-L2
# output directory = -o:directory
# verbose =	-v
# encryption = -e:passphrase
# help = -h

if sys.version_info	< (2, 6, 0)	and	sys.version_info > (3, 0, 0):
	sys.stderr.write("A	minimium of	Python 2.6.0 is	required.  Python 3.0.0	has	not	been fully tested.")
	sys.exit(1)

class KludgeCollector:
	def	__init__(self):
		self = self
		var.KludgeVars()
		self.main(sys.argv[1:])

	def	printit(self):
		opts, args = getopt.getopt(sys.argv[1:], "migqfvlho:e:", ["help", "memory",	"inline", "logs", "quick", "full", "verbose", "errorlog", "output",	"encrypt", "outputdir=", "encryption="])
		print ("Running	Kludge with	" +	str(sys.argv) +	" on " + os.uname()[1])
		print "Press CTRL/C	to cancel in ",
		for	i in range(5):
			print str(5	- i) + " ",
			sys.stdout.flush()
			time.sleep(1)
#		for	opt	in sys.argv[1:]:
#			print opt
#			print var.level
			
	def	running(self):
		print("running")
		collect.CollectStuff()

	def	usage(self):
		#print __doc__
		#print "Help"
		print "Usage: kludge.py	[Options]"
		print "Ex: python kludge.py	-m -f -o /tmp --verbose"
		print "	 -m/--memory: Collect Memory"
		print "	 -i/--inline: Perform inline Memory	Data Collection"
		print "	 -g/--logs:	Collect	Log	Files"
		print "	 -q/--quick: Preliminary Quick Data	Collection"
		print "	 -f/--full:	Full Data Collection"
		print "	 -v/--verbose: Verbose Output"
		print "	 -l/--errorlog:	Log	Kludge"
		print "	 -o/--outputdir	<output	dir>: Output Directory"
		print "	 -e/--encrypt <passphrase>:	Encryption Passphrase"
		print "	 -h/--help:	Help"
	
	def	main(self,argv):
		sys.stderr.write("Kludge {0}".format(constants.VERSION)	+ "\t(https://github.com/Kvetch/)\n")
		sys.stderr.flush()
		try:
			opts, args = getopt.getopt(argv, "migqfvlho:e:", ["help", "memory",	"logs",	"quick", "full", "verbose",	"errorlog",	"encrypt", "outputdir=", "encrypt="])
		except getopt.GetoptError as err:
			print(err)
			self.usage()
			sys.exit(2)
		
		# If there are no arguments	print the help
		if len(sys.argv) ==	1:
			self.usage()
			sys.exit()
			
		for	opt, arg in	opts:
			# If opt is	help print the help
			if opt in ("-h", "--help"):
				self.usage()
				sys.exit()
			elif opt in	('-m', "--memory"):
				var.memory = 1
			elif opt in	('-i', "--inline"):
				var.memory = 1
			elif opt in	('-g', "--logs"):
				var.varlogs	= 1
			elif opt in	('-l', "--errorlog"):
				var.log	= 1
			elif opt in	('-q', "--quick"):
				var.level =	1
			elif opt in	('-f', "--full"):
				var.level =	2
			elif opt in	('-v', "--verbose"):
				var.verbose	= 1
			elif opt in	("-o", "--outputdir"):
				var.output = 1
				var.outputdir =	str(arg)
			elif opt in	("-e", "--encrypt"):
				var.encryption = 1
				var.passphrase = str(arg)
				
				#options = "".join(args)

#		if __name__	== "__main__":
#			main(sys.argv[1:])

x =	KludgeCollector()
x.printit()
x.running()	
			
