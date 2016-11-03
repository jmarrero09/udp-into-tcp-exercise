import sys
from socket import *
import random

BUFSIZE = 1024


def main():
    port = eval(sys.argv[1])
    hport = eval(sys.argv[2])
    host='127.0.0.1'
    haddr = host, hport
    caddr=-1
    ran=.5

    print ('unreliable transport channel ready, listening on port', port)
    s = socket(AF_INET, SOCK_DGRAM)
    s.bind(('', port))
    while 1:
        corrupt=random.random()
        data, addr = s.recvfrom(BUFSIZE)
        if addr==haddr:
            if corrupt <ran:
                print 'unreliable transport channel received %r from %r' % (data, addr)
                print 'uncorrupted messege changing valid bit'
                data=data[:3]+b'0'+data[4:]
                print 'sending to client'
                s.sendto(data, caddr)
            elif corrupt >=ran:
                print 'unreliable transport channel received %r from %r' % (data, addr)
                print 'corrupted messege changing valid bit'
                data=data[:3]+b'1'+data[4:]
                print 'sending to client'
                s.sendto(data, caddr)
        else:
            if corrupt <ran:
                print 'unreliable transport channel received %r from %r' % (data, addr)
                print 'uncorrupted messege adding valid bit'
                data=b'0'+data
                caddr=addr
                s.sendto(data, haddr)
                print ('forwarding to ', haddr)
            elif corrupt >= ran:
                print 'unreliable transport channel received %r from %r' % (data, addr)
                print 'corrupted messge adding valid bit'
                data=b'1'+data
                caddr=addr
                s.sendto(data, haddr)
                print ('forwarding to', haddr)
            
main()
