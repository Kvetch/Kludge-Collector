#!/usr/bin/python2
import subprocess,os,sys
import ctypes
import struct
import binascii
from StringIO import StringIO


class MFT:
	def __init__(self):
		#constant size values
		global longlongsize
		longlongsize=ctypes.sizeof(ctypes.c_longlong)
		global bytesize
		bytesize=ctypes.sizeof(ctypes.c_byte)
		global wordsize
		wordsize=2
		global dwordsize
		dwordsize=4
		self.open_drive()
		
	def open_drive(self):
		#print("Hello")
		global ntfsdrive
		ntfsdrive = open('\\\\.\\\\C:', 'rb') # Change to a variable
		ntfs = ntfsdrive.read(512)
		ntfsfile = StringIO(ntfs)
		
		#parse the MBR for this drive to get the bytes per sector,sectors per cluster and MFT location. 
		#bytes per sector
		ntfsfile.seek(0x0b) # 11 bytes in
		global bytesPerSector
		bytesPerSector=ntfsfile.read(wordsize)
		bytesPerSector=struct.unpack('<h', binascii.unhexlify(binascii.hexlify(bytesPerSector)))[0]

		#sectors per cluster

		ntfsfile.seek(0x0d) # 13 bytes in
		global sectorsPerCluster
		sectorsPerCluster=ntfsfile.read(bytesize)
		sectorsPerCluster=struct.unpack('<b', binascii.unhexlify(binascii.hexlify(sectorsPerCluster)))[0]


		#get mftlogical cluster number
		ntfsfile.seek(0x30) # 48 bytes in
		cno=ntfsfile.read(longlongsize)
		global mftClusterNumber
		mftClusterNumber=struct.unpack('<q', binascii.unhexlify(binascii.hexlify(cno)))[0]

		self.debug('%d %d %d'%(bytesPerSector,sectorsPerCluster,mftClusterNumber))

		#MFT is then at NTFS + (bytesPerSector*sectorsPerCluster*mftClusterNumber)
		global mftloc
		mftloc=long(bytesPerSector*sectorsPerCluster*mftClusterNumber)	 
		#print mftloc
		ntfsdrive.seek(0)
		ntfsdrive.seek(mftloc)
		mftcount = 1
		mftsize = 1024
		mftentry = mftcount * mftsize
		self.mftraw=ntfsdrive.read(mftentry)
		self.analyzeATRs()

	#utility functions for printing data as self.hexdumps
	def hexbytes(self, xs, group_size=1, byte_separator=' ', group_separator=' '):
		def ordc(c):
			return ord(c) if isinstance(c,str) else c
		
		if len(xs) <= group_size:
			s = byte_separator.join('%02X' % (ordc(x)) for x in xs)
		else:
			r = len(xs) % group_size
			s = group_separator.join(
				[byte_separator.join('%02X' % (ordc(x)) for x in group) for group in zip(*[iter(xs)]*group_size)]
			)
			if r > 0:
				s += group_separator + byte_separator.join(['%02X' % (ordc(x)) for x in xs[-r:]])
		return s.lower()



	def hexprint(self, xs):
		xs = xs
		def chrc(c):
			return c if isinstance(c,str) else chr(c)
		
		def ordc(c):
			return ord(c) if isinstance(c,str) else c
		
		def isprint(c):
			return ordc(c) in range(32,127) if isinstance(c,str) else c > 31
		
		return ''.join([chrc(x) if isprint(x) else '.' for x in xs])



	def hexdump(self,xs, group_size=4, byte_separator=' ', group_separator='-', printable_separator='  ', address=0, address_format='%04X', line_size=16):
		xs = xs
		if address is None:
			s = self.hexbytes(xs, group_size, byte_separator, group_separator)
			if printable_separator:
				s += printable_separator + self.hexprint(xs)
		else:
			r = len(xs) % line_size
			s = ''
			bytes_len = 0
			for offset in range(0, len(xs)-r, line_size):
				chunk = xs[offset:offset+line_size]
				bytes = self.hexbytes(chunk, group_size, byte_separator, group_separator)
				s += (address_format + ': %s%s\n') % (address + offset, bytes, printable_separator + self.hexprint(chunk) if printable_separator else '')
				bytes_len = len(bytes)
			
			if r > 0:
				offset = len(xs)-r
				chunk = xs[offset:offset+r]
				bytes = self.hexbytes(chunk, group_size, byte_separator, group_separator)
				bytes = bytes + ' '*(bytes_len - len(bytes))
				s += (address_format + ': %s%s\n') % (address + offset, bytes, printable_separator + self.hexprint(chunk) if printable_separator else '')
		
		return s

	def twos_comp(self, val, bits):
		"""compute the 2's compliment of int value val"""
		if( (val&(1<<(bits-1))) != 0 ):
			val = val - (1<<bits)
		return val



	def decodeATRHeader(self,s):
		d = {}
		d['type'] = struct.unpack("<L",s[:4])[0]
		#print("Type is " + hex(d['type']))
		if d['type'] == 0xffffffff: # End Marker
			return d
		d['len'] = struct.unpack("<L",s[4:8])[0]
		#print("Len is " + str(d['len']))
		d['res'] = struct.unpack("B",s[8])[0]
		#print("RES=", d['res'])
		d['nlen'] = struct.unpack("B",s[9])[0]					# This name is the name of the ADS, I think.
		#print("nlen", d['res']) ###
		d['name_off'] = struct.unpack("<H",s[10:12])[0]
		#print("name_off", d['name_off']) ###
		d['flags'] = struct.unpack("<H",s[12:14])[0]
		#print("Flags", d['flags'])
		d['id'] = struct.unpack("<H",s[14:16])[0]
		#print('ID=',d['id'])
		if d['res'] == 0:
			d['ssize'] = struct.unpack("<L",s[16:20])[0] # Content Length
			d['soff'] = struct.unpack("<H",s[20:22])[0] # Content Attribute
			d['idxflag'] = struct.unpack("<H",s[22:24])[0]
		else:
			d['start_vcn'] = struct.unpack("<d",s[16:24])[0]
			#print('Start_VCN', d['start_vcn'])
			d['last_vcn'] = struct.unpack("<d",s[24:32])[0]
			#print('last_vcn',d['last_vcn'])
			d['run_off'] = struct.unpack("<H",s[32:34])[0]
			d['compusize'] = struct.unpack("<H",s[34:36])[0]
			d['f1'] = struct.unpack("<I",s[36:40])[0]
			d['alen'] = struct.unpack("<d",s[40:48])[0]
			d['ssize'] = struct.unpack("<d",s[48:56])[0]   ##### Add check to see if HD has enough free space from value here
			d['initsize'] = struct.unpack("<d",s[56:64])[0]
		return d

	def decodeDataRuns(self,dataruns):
		decodePos=0
		header=dataruns[decodePos]
		while header !='\x00':
			#print(header)
			#print('HEADER\n' + self.hexdump(header))
			offset=int(binascii.hexlify(header)[0])
			runlength=int(binascii.hexlify(header)[1])
			#print('OFFSET %d LENGTH %d' %( offset,runlength))
			
			#move into the length data for the run
			decodePos+=1

			#print(decodePos,runlength)
			length=dataruns[decodePos:decodePos +int(runlength)][::-1]
			#print(length)
			#print type(length)
			#print('LENGTH\n'+self.hexdump(length))
			length=int(binascii.hexlify(length),16)
				
			
			hexoffset=dataruns[decodePos +runlength:decodePos+offset+runlength][::-1]
			#print('HEXOFFSET\n' +self.hexdump(hexoffset))
			cluster=self.twos_comp(int(binascii.hexlify(hexoffset),16),offset*8)
			
			yield(length,cluster)
			decodePos=decodePos + offset+runlength
			header=dataruns[decodePos]
			#break
			
	def debug(self,message):
		sys.stderr.write(message +'\n')
		print(message +'\n')		


	def analyzeATRs(self):
		ReadPtr=0
		mftDict={}
		mftDict['attr_off'] = struct.unpack("<H",self.mftraw[20:22])[0]
		ReadPtr=mftDict['attr_off']	   
		#self.debug(str(mftDict))
		while ReadPtr<len(self.mftraw):	  
			ATRrecord = self.decodeATRHeader(self.mftraw[ReadPtr:])

			if ATRrecord['type'] == 0x80:
				#print("Type is 80, $data---true")
				dataruns=self.mftraw[ReadPtr+ATRrecord['run_off']:ReadPtr+ATRrecord['len']]
				#print("dataruns " +  dataruns)
				prevCluster=None
				prevSeek=0
				mftfile = open('C:\\dev\\MFTtest.dat', "wb")		
				
				for length,cluster in self.decodeDataRuns(dataruns):
					self.debug('%d %d'%(length,cluster))
					self.debug('drivepos: %d'%(ntfsdrive.tell()))
					
					if prevCluster==None:	 
						ntfsdrive.seek(cluster*bytesPerSector*sectorsPerCluster)
						prevSeek=ntfsdrive.tell()
						mftfile.writelines(ntfsdrive.read(length*bytesPerSector*sectorsPerCluster))
						prevCluster=cluster
					else:
						ntfsdrive.seek(prevSeek)
						newpos=prevSeek + (cluster*bytesPerSector*sectorsPerCluster)
						self.debug('seekpos: %d'%(newpos))
						ntfsdrive.seek(newpos)
						prevSeek=ntfsdrive.tell()					 
						mftfile.writelines(ntfsdrive.read(length*bytesPerSector*sectorsPerCluster))
						prevCluster=cluster				   
				mftfile.close
				break
			

			if ATRrecord['type'] == 0xffffffff:
				mftcount += 1
				
			if ATRrecord['len'] > 0:
				ReadPtr = ReadPtr + ATRrecord['len']
			
			
			
MFT()			