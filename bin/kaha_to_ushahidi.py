#!/usr/bin/env python

import requests
import pdb

r = requests.get('http://kaha.co/api')
data = r.json()
pdb.set_trace()
print data[0]
