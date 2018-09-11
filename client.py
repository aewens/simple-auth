#!/usr/bin/env python3 

import sys
import urllib.request
import urllib.parse

if len(sys.argv) < 4:
    print(sys.argv)
    print("ERROR: Missing parameters")
    sys.exit(1)
    
url, flag, param = sys.argv[1:]

data = dict()
if flag == "-v":
    data["voucher"] = param
elif flag == "-t":
    data["token"] = param
else:
    print("ERROR: Unknown parameter '%s'" % flag)
    sys.exit(1)

post_data = urllib.parse.urlencode(data).encode("utf-8")

simple = urllib.request.urlopen(url, post_data)
print(simple.read().decode("utf-8"))