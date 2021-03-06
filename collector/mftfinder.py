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
		self.open_mftfile()
		
	def open_mftfile(self):
		global mftfile
		mftfile = open('\\\\.\\\\C:\\dev\\MFTtest.dat', 'rb')
		mftfile.seek(0)
		mftcount = 1
		mftsize = 1024
		mftentry = mftcount * mftsize
		self.mftraw=mftfile.read(mftentry)
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
		print("Type is " + hex(d['type']))
		if d['type'] == 0xffffffff: # End Marker
			return d
		d['len'] = struct.unpack("<L",s[4:8])[0]
		print("Len is " + str(d['len']))
		d['res'] = struct.unpack("B",s[8])[0]
		print("RES=", d['res'])
		d['nlen'] = struct.unpack("B",s[9])[0]					# This name is the name of the ADS, I think.
		print("nlen", d['res']) ###
		d['name_off'] = struct.unpack("<H",s[10:12])[0]
		print("name_off", d['name_off']) ###
		d['flags'] = struct.unpack("<H",s[12:14])[0]
		print("Flags", d['flags'])
		d['id'] = struct.unpack("<H",s[14:16])[0]
		print('ID=',d['id'])
		if d['res'] == 0:
			d['ssize'] = struct.unpack("<L",s[16:20])[0] # Content Length
			d['soff'] = struct.unpack("<H",s[20:22])[0] # Content Attribute
			d['idxflag'] = struct.unpack("<H",s[22:24])[0]
		else:
			d['start_vcn'] = struct.unpack("<d",s[16:24])[0]
			print('Start_VCN', d['start_vcn'])
			d['last_vcn'] = struct.unpack("<d",s[24:32])[0]
			print('last_vcn',d['last_vcn'])
			d['run_off'] = struct.unpack("<H",s[32:34])[0]
			d['compusize'] = struct.unpack("<H",s[34:36])[0]
			d['f1'] = struct.unpack("<I",s[36:40])[0]
			d['alen'] = struct.unpack("<d",s[40:48])[0]
			d['ssize'] = struct.unpack("<d",s[48:56])[0]
			d['initsize'] = struct.unpack("<d",s[56:64])[0]
		return d

	def decodeDataRuns(self,dataruns):
		decodePos=0
		header=dataruns[decodePos]
		while header !='\x00':
			print(header)
			print('HEADER\n' + self.hexdump(header))
			offset=int(binascii.hexlify(header)[0])
			runlength=int(binascii.hexlify(header)[1])
			print('OFFSET %d LENGTH %d' %( offset,runlength))
			
			#move into the length data for the run
			decodePos+=1

			print(decodePos,runlength)
			length=dataruns[decodePos:decodePos +int(runlength)][::-1]
			print(length)
			print type(length)
			print('LENGTH\n'+self.hexdump(length))
			length=int(binascii.hexlify(length),16)
			
			hexoffset=dataruns[decodePos +runlength:decodePos+offset+runlength][::-1]
			print('HEXOFFSET\n' +self.hexdump(hexoffset))
			cluster=self.twos_comp(int(binascii.hexlify(hexoffset),16),offset*8)
			
			yield(length,cluster)
			decodePos=decodePos + offset+runlength
			header=dataruns[decodePos]
			#break
			
	def decodeFileNameAttrib(self,s):
			f = {}
			f['parentdir'] = struct.unpack("<Q",s[:8])[0]
			print("Parent Directory is " + hex(f['parentdir']))
			f['datecrt'] = struct.unpack("<Q",s[8:16])[0]
			print("Date Creation is " + str(f['datecrt']))
			f['datemod'] = struct.unpack("<Q",s[16:24])[0]
			print("Date Modified ", f['datemod'])
			f['datemftmod'] = struct.unpack("<Q",s[24:32])[0]
			print("Date MFT Modified ", f['datemftmod'])
			f['dateacs'] = struct.unpack("<Q",s[32:40])[0]
			print("Date Accessed ", f['dateacs'])
			f['logfsize'] = struct.unpack("<Q",s[40:48])[0]
			print("Logical File Size ", f['logfsize'])
			f['disksize'] = struct.unpack("<Q",s[48:56])[0]
			print("Size of Disk ", f['disksize'])
			f['flags'] = struct.unpack("<I",s[56:60])[0]
			print("Flags ", f['flags'])
			try:												# Circle back - do we care about this value?
				f['reparse'] = struct.unpack("<s",s[60:64])[0]
			except:
				f['reparse'] = 0
			print("Reparse Value ", f['reparse'])
			f['namelen'] = struct.unpack("<B",s[64])[0]
			print("Name Length ", f['namelen']) # Take this hex value x2
			f['nametype'] = struct.unpack("<B",s[65])[0]
			print("Name Type - 3=Win32DOSCompat,2=DOS,1=Win32,0=Posix ", f['nametype'])
			#f['name'] = s[66:70][2]
		#try:
			i=0
			f['name'] = ""
			ReadPtr=0
			mftDict={}		
			mftDict['attr_off'] = struct.unpack("<H",self.mftraw[20:22])[0]
			ReadPtr=mftDict['attr_off']
			ATRrecord = self.decodeATRHeader(self.mftraw[ReadPtr:])
			while i < f['namelen']*2:

				## namelocrun = 66 + i
				## temp = struct.unpack("<s",s[namelocrun])[0]
				## f['name'] += temp
				## i+=1
				## print(f['name'])
				
				namelocrun = 66 + i
				temp = struct.unpack("<s",s[namelocrun])[0]
				f['name'] += temp
				i+=1
				print(f['name'])			
				
				
		#except:
			#f['name'] = "MFTREADINGERROR"
			print("Name ", f['name'])

	def decodeSIRecord(self,s):
			si = {}
			si['datecrt'] = struct.unpack("<Q",s[0:8])[0]
			print("Date Creation is " + str(si['datecrt']))
			si['filealt'] = struct.unpack("<Q",s[8:16])[0]
			print("File Altered ", si['filealt'])
			si['filemftalt'] = struct.unpack("<Q",s[16:24])[0]
			print("File MFT Altered ", si['filemftalt'])
			si['fileacs'] = struct.unpack("<Q",s[24:32])[0]
			print("File Accessed ", si['fileacs'])
			si['flags'] = struct.unpack("<Q",s[32:36])[0]0
			print("Flags ", si['flags'])
			si['maxnumvers'] = struct.unpack("<Q",s[36:40])[0]
			print("Max Number of Versions ", si['maxnumvers'])
			si['vernum'] = struct.unpack("<I",s[40:44])[0]
			print("Version Number ", si['vernum'])
************************************************************************
			si['namelen'] = struct.unpack("<B",s[64])[0]
			print("Name Length ", si['namelen'])
			si['nametype'] = struct.unpack("<B",s[65])[0]
			print("Name Type - 3=Win32DOSCompat,2=DOS,1=Win32,0=Posix ", si['nametype'])
			#si['name'] = s[66:70][2]
		#try:
			i=0
			si['name'] = ""
			ReadPtr=0
			mftDict={}		
			mftDict['attr_off'] = struct.unpack("<H",self.mftraw[20:22])[0]
			ReadPtr=mftDict['attr_off']
			ATRrecord = self.decodeATRHeader(self.mftraw[ReadPtr:])
			while i < si['namelen']*2:

				## namelocrun = 66 + i
				## temp = struct.unpack("<s",s[namelocrun])[0]
				## si['name'] += temp
				## i+=1
				## print(si['name'])
				
				namelocrun = 66 + i
				temp = struct.unpack("<s",s[namelocrun])[0]
				si['name'] += temp
				i+=1
				print(si['name'])			
				
				
		#except:
			#si['name'] = "MFTREADINGERROR"
			print("Name ", si['name'])
			
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
			print ReadPtr
			print ("ReadPoint^^^")
			#self.debug("Attribute type: %x Length: %d Res: %x" % (ATRrecord['type'], ATRrecord['len'], ATRrecord['res']))
			if ATRrecord['type'] == 0x30:
				print("Type is 30, $filename---true")
				print("Attribute Length ",ATRrecord['len'])				
				print("Content Length ",ATRrecord['ssize'])
				print("Content Offset ",ATRrecord['soff'])
				print ATRrecord
				
				filenamecontent=self.mftraw[ReadPtr+ATRrecord['soff']:ReadPtr+ATRrecord['len']]
				
				# # for length,cluster in self.decodeFileNameContent(filenamecontent):
					# # # # # self.debug('%d %d'%(length,cluster))
						# # # # # self.debug('drivepos: %d'%(mftfile.tell()))
						# # print(filenamecontent['parentdir'])
						
						# if prevCluster==None:	 
							# mftfile.seek(cluster*bytesPerSector*sectorsPerCluster)
							# prevSeek=mftfile.tell()
							# #mftfile.writelines(mftfile.read(length*bytesPerSector*sectorsPerCluster))
							# prevCluster=cluster
						# else:
							# mftfile.seek(prevSeek)
							# newpos=prevSeek + (cluster*bytesPerSector*sectorsPerCluster)
							# self.debug('seekpos: %d'%(newpos))
							# mftfile.seek(newpos)
							# prevSeek=mftfile.tell()					 
							# #mftfile.writelines(mftfile.read(length*bytesPerSector*sectorsPerCluster))
							# prevCluster=cluster	
							
					## break
			
			if ATRrecord['type'] == 0x80:
				print("Type is 80, $data---true")
				#self.debug(self.hexdump(self.mftraw[ReadPtr:ReadPtr+ATRrecord['len']]))
				#self.debug(self.hexdump(self.mftraw[ReadPtr+ATRrecord['run_off']:ReadPtr+ATRrecord['len']]))
				dataruns=self.mftraw[ReadPtr+ATRrecord['run_off']:ReadPtr+ATRrecord['len']]
				print("dataruns " +  dataruns)
				prevCluster=None
				prevSeek=0
				outputfile = open('C:\\dev\\test2.dat', "wb")		
				
				for length,cluster in self.decodeDataRuns(dataruns):
					self.debug('%d %d'%(length,cluster))
					self.debug('drivepos: %d'%(mftfile.tell()))
					
					if prevCluster==None:	 
						outputfile.seek(cluster*bytesPerSector*sectorsPerCluster)
						prevSeek=outputfile.tell()
						outputfile.writelines(mftfile.read(length*bytesPerSector*sectorsPerCluster))
						prevCluster=cluster
					else:
						outputfile.seek(prevSeek)
						newpos=prevSeek + (cluster*bytesPerSector*sectorsPerCluster)
						self.debug('seekpos: %d'%(newpos))
						outputfile.seek(newpos)
						prevSeek=outputfile.tell()					 
						outputfile.writelines(mftfile.read(length*bytesPerSector*sectorsPerCluster))
						prevCluster=cluster				   
				outputfile.close
				##break
			

			if ATRrecord['type'] == 0xffffffff:
				mftcount += 1
				
				
			if ATRrecord['len'] > 0:
				ReadPtr = ReadPtr + ATRrecord['len']
				print("ReadPointer=", ReadPtr)
			
			
			
MFT()			