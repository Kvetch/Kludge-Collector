import struct
import os
import sys
import ctypes
import binascii
from StringIO import StringIO

longlongsize=ctypes.sizeof(ctypes.c_longlong)
bytesize = ctypes.sizeof(ctypes.c_byte)

#F = open('\\\\.\\PhysicalDrive0', 'rb')
F = open('\\\\.\\\\C:', 'rb')
d = F.read(512)
drive = StringIO(d)

# Bytes Per Sector Number
drive.seek(0x0b) # 11 bytes in
bytesPerSector = drive.read(2)
print("bytespersector")
#print "".join(format(ord(c),"02x") for c in bytesPerSector)
bytesPerSector = struct.unpack('<h', bytesPerSector)
bytesPerSector = reduce(lambda clust, d: clust * 10 + d, bytesPerSector)
print ("bytesPerSector =", bytesPerSector)

# Sectors Per Cluster Number
drive.seek(0x0d) # 13 bytes in
sectorsPerCluster = drive.read(1) # Read a byte
sectorsPerCluster = struct.unpack('<b', sectorsPerCluster)
sectorsPerCluster = reduce(lambda clust, d: clust * 10 + d, sectorsPerCluster)
print ("sectorsPerCluster =", sectorsPerCluster)

# MFT Cluster Number
drive.seek(0x30) # 48 bytes in
mftClusterNumber = drive.read(longlongsize) # Read 8 bytes
mftClusterNumber = struct.unpack('<q', mftClusterNumber)
#print ("ClusterNumber in bytearray is =", bytearray(clusterNumber))
print ("mftClusterNumber =", mftClusterNumber)
mftClusterNumber = reduce(lambda clust, d: clust * 10 + d, mftClusterNumber)

mftloc=(bytesPerSector*sectorsPerCluster*mftClusterNumber)
print ("mftloc",mftloc)
drive.seek(0)
drive.seek(mftloc)
mftrecord=drive.read(1024) # This should be the MFT record for itself

ReadPtr=0
mftDict={}
print mftrecord[20:22]
mftDict['attr_offset'] = struct.unpack("<H", mftrecord[20:22]) # 2 byte unsigned int short
print("mftDict", mftDict)
# ReadPtr=mftDict['attr_offset']    
# while ReadPtr<len(mftrecord):    
	# ATRrecord = decodeATRHeader(mftrecord[ReadPtr:])
	# if ATRrecord['type'] == 0x80:
		# dataruns=mftrecord[ReadPtr+ATRrecord['run_offset']:ReadPtr+ATRrecord['len']]
		# prevCluster=None
		# prevSeek=0
		# mftfile = open('C:\\dev\\test.dat', "wb")
		# for length,cluster in decodeDataRuns(dataruns):
		
			# if prevCluster==None:    
				# ntfsdrive.seek(cluster*bytesPerSector*sectorsPerCluster)
				# prevSeek=ntfsdrive.tell()
				# mftfile.writelines(ntfsdrive.read(length*bytesPerSector*sectorsPerCluster))
				# prevCluster=cluster
			# else:
				# ntfsdrive.seek(prevSeek)
				# newpos=prevSeek + (cluster*bytesPerSector*sectorsPerCluster)
				# ntfsdrive.seek(newpos)
				# prevSeek=ntfsdrive.tell()                    
				# mftfile.writelines(ntfsdrive.read(length*bytesPerSector*sectorsPerCluster))
				# prevCluster=cluster           
		# break





