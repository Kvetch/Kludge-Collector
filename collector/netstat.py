## {{{ http://code.activestate.com/recipes/392572/ (r1)
# openPorts.py

import ctypes
import socket
import struct

def getOpenPorts():
    file = open("netstat.txt", 'w')
    file.write("Proto\t\tLocal Address\t\tForeign Address\tState\n")
    portList = []
    
    DWORD = ctypes.c_ulong
    NO_ERROR = 0
    NULL = ""
    bOrder = 0
    
    # define some MIB constants used to identify the state of a TCP port
    MIB_TCP_STATE_CLOSED = 1
    MIB_TCP_STATE_LISTEN = 2
    MIB_TCP_STATE_SYN_SENT = 3
    MIB_TCP_STATE_SYN_RCVD = 4
    MIB_TCP_STATE_ESTAB = 5
    MIB_TCP_STATE_FIN_WAIT1 = 6
    MIB_TCP_STATE_FIN_WAIT2 = 7
    MIB_TCP_STATE_CLOSE_WAIT = 8
    MIB_TCP_STATE_CLOSING = 9
    MIB_TCP_STATE_LAST_ACK = 10
    MIB_TCP_STATE_TIME_WAIT = 11
    MIB_TCP_STATE_DELETE_TCB = 12
    
    ANY_SIZE = 1         
    
    # defing our MIB row structures
    class MIB_TCPROW(ctypes.Structure):
        _fields_ = [('dwState', DWORD),
                    ('dwLocalAddr', DWORD),
                    ('dwLocalPort', DWORD),
                    ('dwRemoteAddr', DWORD),
                    ('dwRemotePort', DWORD)]
    
    class MIB_UDPROW(ctypes.Structure):
        _fields_ = [('dwLocalAddr', DWORD),
                    ('dwLocalPort', DWORD),
                    ('dwRemoteAddr', DWORD),
                    ('dwRemotePort', DWORD)]
  
    dwSize = DWORD(0)
    
    # call once to get dwSize 
    ctypes.windll.iphlpapi.GetTcpTable(NULL, ctypes.byref(dwSize), bOrder)
    
    # ANY_SIZE is used out of convention (to be like MS docs); even setting this
    # to dwSize will likely be much larger than actually necessary but much 
    # more efficient that just declaring ANY_SIZE = 65500.
    # (in C we would use malloc to allocate memory for the *table pointer and 
    #  then have ANY_SIZE set to 1 in the structure definition)
    
    ANY_SIZE = dwSize.value
    
    class MIB_TCPTABLE(ctypes.Structure):
        _fields_ = [('dwNumEntries', DWORD),
                    ('table', MIB_TCPROW * ANY_SIZE)]
    
    tcpTable = MIB_TCPTABLE()
    tcpTable.dwNumEntries = 0 # define as 0 for our loops sake

    # now make the call to GetTcpTable to get the data
    if (ctypes.windll.iphlpapi.GetTcpTable(ctypes.byref(tcpTable), 
        ctypes.byref(dwSize), bOrder) == NO_ERROR):
      
        maxNum = tcpTable.dwNumEntries
        placeHolder = 0
        
        # loop through every connection
        while placeHolder < maxNum:
        
            item = tcpTable.table[placeHolder]
            placeHolder += 1
            
            # format the data we need (there is more data if it is useful - 
            # see structure definition)
            lPort = item.dwLocalPort
            lPort = socket.ntohs(lPort)
            lAddr = item.dwLocalAddr
            lAddr = socket.inet_ntoa(struct.pack('L', lAddr))
            rPort = item.dwRemotePort
            rPort = socket.ntohs(rPort)
            rAddr = item.dwRemoteAddr
            rAddr = socket.inet_ntoa(struct.pack('L', rAddr))
            portState = item.dwState
            portStateInWords = ""
            if item.dwState==1:
                portStateInWords = 'CLOSED'
            elif item.dwState==2:
                portStateInWords = 'LISTENING'
            elif item.dwState==3:
                portStateInWords = 'SYN SENT'
            elif item.dwState==4:
                portStateInWords = 'SYN DCVD'
            elif item.dwState==5:
                portStateInWords = 'ESTABLISHED'
            elif item.dwState==6:
                portStateInWords = 'FIN WAIT1'
            elif item.dwState==7:
                portStateInWords = 'FIN WAIT2'
            elif item.dwState==8:
                portStateInWords = 'CLOSE WAIT'
            elif item.dwState==9:
                portStateInWords = 'CLOSING'
            elif item.dwState==10:
                portStateInWords = 'LAST ACK'
            elif item.dwState==11:
                portStateInWords = 'TIME WAIT'
            elif item.dwState==12:
                portStateInWords = 'DELETE TCB'               
                    
            # only record TCP ports where we're listening on our external 
            #    (or all) connections
            file.write("TCP\t\t" + lAddr + ':' + str(lPort) + "\t\t" + rAddr + ':' + str(rPort) + '\t\t' + portStateInWords +'\n')
            
    else:
        print("Error occurred when trying to get TCP Table")

    dwSize = DWORD(0)
    
    # call once to get dwSize
    ctypes.windll.iphlpapi.GetUdpTable(NULL, ctypes.byref(dwSize), bOrder)
    ANY_SIZE = dwSize.value # again, used out of convention 
    #                            (see notes in TCP section)
    
    class MIB_UDPTABLE(ctypes.Structure):
        _fields_ = [('dwNumEntries', DWORD),
                    ('table', MIB_UDPROW * ANY_SIZE)]  
                    
    udpTable = MIB_UDPTABLE()
    udpTable.dwNumEntries = 0 # define as 0 for our loops sake
    
    # now make the call to GetUdpTable to get the data
    if (ctypes.windll.iphlpapi.GetUdpTable(ctypes.byref(udpTable), 
        ctypes.byref(dwSize), bOrder) == NO_ERROR):
    
        maxNum = udpTable.dwNumEntries
        placeHolder = 0
        while placeHolder < maxNum:

            item = udpTable.table[placeHolder]
            placeHolder += 1
            lPort = item.dwLocalPort
            lPort = socket.ntohs(lPort)
            lAddr = item.dwLocalAddr
            lAddr = socket.inet_ntoa(struct.pack('L', lAddr))
            rPort = item.dwRemotePort
            rPort = socket.ntohs(rPort)
            rAddr = item.dwRemoteAddr
            rAddr = socket.inet_ntoa(struct.pack('L', rAddr))
            file.write("UDP\t\t" + lAddr + ':' + str(lPort) + "\t\t" + rAddr + ':' + str(rPort) + "\n")
    else:
        print("Error occurred when trying to get UDP Table")
    portList.sort()  
    
    file.close()

grabNetstat = getOpenPorts()

