import sys
import variables as var
import logger as log
import variables as var
import hashlib
import os

class KludgeHasher():
    """ Hashing Mechanism """
    def __init__(self):
        self = self
    
    def dirhasher(self, directory):
        self = self
        for r,d,f in os.walk(directory):
            for files in f:
                _filename = os.path.join(r, files)
                print _filename
                print 'The Hash of ' + _filename + ' is ', self.hashfile(_filename, hashlib.md5())
            
    def hashfile(self, filename, hasher, blocksize=65536):
        afile = open(str(filename), 'rb')
        buf = afile.read(blocksize)
        while True:
            hasher.update(buf)
            buf = afile.read(blocksize)
            if not buf:
                break
        return hasher.hexdigest()
