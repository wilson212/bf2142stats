""" Battlefield 2142 Auth token encoder
This is the python module package for creating auth tokens of EA/IGN's stat server.

Copyright © 2006 Alexander Bondarenko <wiz@aenor.ru>

Licence:

    This library is free software; you can redistribute it and/or
    modify it under the terms of the GNU Lesser General Public
    License as published by the Free Software Foundation; either
    version 2.1 of the License, or (at your option) any later version.

    This library is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
    Lesser General Public License for more details.
"""

from time import time
from struct import pack

from aes import DefEncryptBlock as aes
from crc import compute         as crc

from base64 import b64encode
def base64(s):
        return b64encode(s,'[]').replace('=','_')

def make_auth(pid=0, as_server=False, timestamp=0):
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
