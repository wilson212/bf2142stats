# -*- coding: utf-8 -*-

""" Battlefield 2142 Auth token encoder
This is the python module for creating auth tokens of EA/IGN's stat server.
"""

from time import time
from struct import pack

from aes import DefEncryptBlock as aes
from crc import compute         as crc

from base64 import b64encode
def base64(s):
    """ Base64-encode string and translate it for using as EA's auth token. """
    return b64encode(s,'[]').replace('=','_')

def make_auth(pid=0, as_server=False, timestamp=0):
    """ Assemble authentication token. """
    data = ['\x00']*16

    if not timestamp:
        timestamp = int(time())
    data[:4] = pack('L', timestamp)

    # 'magic number' 64 00 00 00
    data[4] = 'd'

    data[8:12] = pack('L', pid)

    if as_server:
        data[12] = 1

    dc = crc(data[:14])
    try:
        data[14:16] = pack('H', dc)
    except:
        print hex(dc)

    return base64(aes(data))

if __name__ == '__main__':
    import sys
    try:
        pid = int(sys.argv[1])
    except:
        pid = 0
    print make_auth(pid)
