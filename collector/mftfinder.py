import struct
import os
import sys
import ctypes
import binascii
from StringIO import StringIO

longlongsize=ctypes.sizeof(ctypes.c_longlong)
bytesize = ctypes.sizeof(ctypes.c_byte)

ntfsdrive = open('\\\\.\\\\C:', 'rb')
ntfs = ntfsdrive.read(512)
ntfsfile = StringIO(ntfs)


def decodeATRHeader(s):
	
	d = {}
	d['type'] = struct.unpack("<L",s[:4])[0]
	print("Type is " + str(d['type']))
	if d['type'] == 0xffffffff:
		return d
	d['len'] = struct.unpack("<L",s[4:8])[0]
	print("Len is " + str(d['len']))
	d['res'] = struct.unpack("B",s[8])[0]
	d['nlen'] = struct.unpack("B",s[9])[0]					# This name is the name of the ADS, I think.
	d['name_off'] = struct.unpack("<H",s[10:12])[0]
	d['flags'] = struct.unpack("<H",s[12:14])[0]
	d['id'] = struct.unpack("<H",s[14:16])[0]
	if d['res'] == 0:
		d['ssize'] = struct.unpack("<L",s[16:20])[0]
		d['soff'] = struct.unpack("<H",s[20:22])[0]
		d['idxflag'] = struct.unpack("<H",s[22:24])[0]
	else:
		d['start_vcn'] = struct.unpack("<d",s[16:24])[0]
		d['last_vcn'] = struct.unpack("<d",s[24:32])[0]
		d['run_off'] = struct.unpack("<H",s[32:34])[0]
		d['compusize'] = struct.unpack("<H",s[34:36])[0]
		d['f1'] = struct.unpack("<I",s[36:40])[0]
		d['alen'] = struct.unpack("<d",s[40:48])[0]
		d['ssize'] = struct.unpack("<d",s[48:56])[0]
		d['initsize'] = struct.unpack("<d",s[56:64])[0]

	return d


# Bytes Per Sector Number
ntfsfile.seek(0x0b) # 11 bytes in
bytesPerSector = ntfsfile.read(2)
print("bytespersector")
#print "".join(format(ord(c),"02x") for c in bytesPerSector)
bytesPerSector = struct.unpack('<h', bytesPerSector)
print(bytesPerSector[0])
print(type(bytesPerSector))
print(type(bytesPerSector[0]))
print ("bytesPerSector =", bytesPerSector)

# Sectors Per Cluster Number
ntfsfile.seek(0x0d) # 13 bytes in
sectorsPerCluster = ntfsfile.read(1) # Read a byte
sectorsPerCluster = struct.unpack('<b', sectorsPerCluster)
print ("sectorsPerCluster =", sectorsPerCluster)

# MFT Cluster Number
ntfsfile.seek(0x30) # 48 bytes in
mftClusterNumber = ntfsfile.read(longlongsize) # Read 8 bytes
mftClusterNumber = struct.unpack('<q', mftClusterNumber)
print(mftClusterNumber)
#print ("ClusterNumber in bytearray is =", bytearray(mftClusterNumber))
print ("mftClusterNumber =", mftClusterNumber)

mftloc=(bytesPerSector[0]*sectorsPerCluster[0]*mftClusterNumber[0])
print ("mftloc = ",mftloc)
print (type(mftloc))

ntfsdrive.seek(0,0)
ntfsdrive.seek(mftloc,0)
mftrecord=ntfsdrive.read(1024) # This should be the MFT record for itself.	Each $MFT record is 1024 bytes
#print(mftrecord)
#print ("mftrecord in bytearray is =", bytearray(mftrecord))
ReadPtr=0
mftDict={} # Create MFT Hash Table
#print ("mft-attrib " + bytearray(mftrecord[20:22]))
mftDict['attr_offset'] = struct.unpack('<H', mftrecord[20:22]) # 8 byte unsigned int short.	 Bytes 20-21 of the File Record Segment Header 1st Attrib Offset
print("mftDict", mftDict)
ReadPtr=mftDict['attr_offset'][0]	 
print ("ReadPtr " + str(ReadPtr) + str(type(ReadPtr)))
print type(mftrecord)
print mftrecord[0]
print len(mftrecord)
i = 0
while ReadPtr<len(mftrecord):
	ATRrecord = decodeATRHeader(mftrecord[ReadPtr:])
	if ATRrecord['type'] == 0x80:
		print("true")
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
		break
	if ATRrecord['len'] > 0:
			ReadPtr = ReadPtr + ATRrecord['len']




# Attribute Name				Hex Value		Information
# Unused						0x00			Unused	
# Standard Information			0x10			timestamps, link counts
# File Name						0x30			long and short filenames.  Long can be <=255 unicode chrs, Short is 8.3 names.	Additional names and hard links
# Object ID						0x40			volume file identifier used by link tracking service.  not all files have them
# Security Descriptor			0x50			who owns and can access the file
# Volume Name					0x60			volume label in the $Volume NTFS File
# Volume Information			0x70			volume version in the $Volume NTFS File
# Data							0x80			file data.	can have multiple attribs per file including 1 unnamed data attribute
# Index Root					0x90			used to implement folders and indexes
# Index Allocation				0xa0			used to implement folders and indexes
# Bitmap						0xb0			used to implement folders and indexes
# Reparse Point					0xc0			used for volume mounts and junction points and used to mark certain files special for a driver
# EA Information				0xd0			
# EA							0xe0			
# Property Set					0xf0			
# Logged Utility Stream			0x100			used by EFS, similiar to a data stream.
# First User Defined Attribute	0x1000			
# End of Attributes (records)	0xffffffff		