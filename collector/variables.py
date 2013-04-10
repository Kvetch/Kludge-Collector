import os, datetime
from os import *

# Should I set type on each one?
class KludgeVars:
    def __init__(self):
        global now
        now = datetime.datetime.now()
        global timestmp
        timestmp = now.strftime("%m-%d-%Y_%H%M")
        global memory
        memory = None
        global _varlogs
        varlogs = None
        global log
        log = None
        global level
        level = 1
        global verbose
        verbose = None
        global output
        output = 1
        global mail
        mail = 1
        global hashing
        hashing = 1
        global outputdir
        outputdir = "C:/Windows/Temp/"
        global errorlog
        errorlog = None
        global err_file
        err_file = None
        global encryption
        encryption = None
        global passphrase
        passphrase = None
        global justdate
        justdate = now.strftime("%m-%d-%Y")
        global today
        today = datetime.datetime.today()
        global abitback
        abitback = (today - datetime.timedelta(days=15)).strftime("%m/%d/%Y")
