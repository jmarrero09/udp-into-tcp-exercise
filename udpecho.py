#! /usr/bin/env python

# Client and server for udp (datagram) echo.
#
# Usage: udpecho -s [port]            (to start a server)
# or:    udpecho -c host [port] <file (client)

import sys
from socket import *

ECHO_PORT = 50000 + 7
BUFSIZE = 1024


def main():
    if len(sys.argv) < 2:
        usage()
    if sys.argv[1] == '-s':
        server()
    elif sys.argv[1] == '-c':
        client()
    else:
        usage()

def usage():
    sys.stdout = sys.stderr
    print 'Usage: python udpecho.py -s [port]           (to run server)'
    print 'or:    python udpecho.py -c [port]           (to run client)'
    sys.exit(2)

def server():
    lmsg='ack01First Message Was Corrupt'
    sMode='0'
    if len(sys.argv) > 2:
        port = eval(sys.argv[2])
    else:
        port = ECHO_PORT
    s = socket(AF_INET, SOCK_DGRAM)
    s.bind(('', port))
    print 'udp echo server ready'
    while 1:
        data, addr = s.recvfrom(BUFSIZE)

        if sMode=='0':
            if data[0]=='0' and data[1]=='0':
                print 'server received %r from %r' % (data[2:], addr)
                data=b'ack'+data
                lmsg=data
                print 'sending back'
                s.sendto(data, addr)
                sMode='1'
                print '||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||'
            else:
                print 'corrupted or not right mode not recieved resending.'
                s.sendto(lmsg, addr)
        elif sMode=='1':
            if data[1]=='1' and data[0]=='0':
                print 'server received %r from %r' % (data[2:], addr)
                data=b'ack'+data
                lmsg=data
                print 'sending back'
                s.sendto(data, addr)
                sMode='0'
                print '||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||'
            else:
                print 'corrupted or not right mode not recieved resending.'
                s.sendto(lmsg, addr)
            
def client():
    cMode='0'
    lmsg=b''
    if len(sys.argv) < 2:
        usage()
    host = '127.0.0.1'
    if len(sys.argv) > 2:
        port = eval(sys.argv[2])
    else:
        port = ECHO_PORT
    print("using port",port)
    addr = host, port
    s = socket(AF_INET, SOCK_DGRAM)
    s.bind(('', 0))
    print 'udp echo client ready, reading stdin'
    while True:
        line = sys.stdin.readline()
        print("sending",line)
        if not line:
            break
        line=cMode+line
        lmsg=line
        print 'adding mode as header'
        s.sendto(line, addr)
        print '||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||'
        while True:
            data, fromaddr = s.recvfrom(BUFSIZE)
            if cMode=='0':
                
                if  data[3]=='0' and data[4]=='0':
                    print 'client received %r from %r' % (data[0:3], fromaddr)
                    cMode='1'
                    break
                else:
                    print 'message was corrupted or not in the same mode. resending'
                    s.sendto(lmsg, addr)
            elif cMode=='1':
                
                if data[3]=='0' and data[4]=='1':
                    print 'client received %r from %r' % (data[0:3], fromaddr)
                    cMode='0'
                    break
                else:
                    print 'message was corrupted or not in the same mode. resending'
                    s.sendto(lmsg, addr)

                    
main()
