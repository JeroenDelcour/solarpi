# coding: utf-8
from struct import unpack, iter_unpack, calcsize
from datetime import datetime, timedelta
from os.path import getsize
from math import ceil

def tail(path, fmt='<Lff'):
    with open(path, 'rb') as f:
        f.seek(-calcsize(fmt), 2)
        return unpack(fmt, f.read())

def read(path, last_days=7, fmt='<Lff'):
    size = calcsize(fmt)
    with open(path, 'rb') as f:
        # search back given number of days
        epoch,_,_ = tail(path, fmt=fmt)
        since = datetime.timestamp(datetime.fromtimestamp(epoch) - timedelta(days=last_days))
        # binary search for starting index
        n = int(getsize(path) / size)
        l, r = 0, n-1
        while not l==r:
            m = ceil((l+r)/2)
            f.seek(m*size)
            if unpack(fmt, f.read(size))[0] > since:
                r = m-1
            else:
                l = m
        return iter_unpack(fmt, f.read())
