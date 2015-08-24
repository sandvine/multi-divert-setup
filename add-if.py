#!/usr/bin/env /usr/bin/python

import libvirt
import libxml2
import sys
#from xml.etree import ElementTree

vmname = sys.argv[1]
bridgename = sys.argv[2]
model = sys.argv[3]

conn=libvirt.open("qemu:///system")
dom=conn.lookupByName(vmname)

TEMPLATE = \
'''<interface type='bridge'>
      <source bridge='%s'/>
      <virtualport type='openvswitch'/>
      <model type='%s'/>
    </interface>
'''

dom.attachDevice(TEMPLATE % (bridgename,model))

xmldesc = dom.XMLDesc(0)
doc = libxml2.parseDoc(xmldesc)
ctx = doc.xpathNewContext()
devs = ctx.xpathEval("/domain/devices/interface")
for d in devs:
    ctx.setContextNode(d)
    devn = ctx.xpathEval("target/@dev")
    devname = devn[0].content

print(devname)


