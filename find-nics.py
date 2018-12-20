#!/usr/bin/env python

'''
Takes the pci file (from hdt dump) as an argument, parses it into a list of
dictionaries, then searches that list for dictionaries with network devices, and looks in 
and returns some ethernet (wired) and wlan (wireless) device models and manufacturers.
Takes two arguments: an '-e' or a '-w' and the pci file.  -e will return the wired 
ethernet info, -w will return the wireless info.
'''

import re
import sys

# Define a function that returns a dictionary
def new_dict(): return {}

def main():
    nic = ''
    dicts = []
    index = 0
    count = 0
    f = open(sys.argv[2])
    for line in f:
        line = re.sub('"','',line) # strip out quotes; strip, below, only removes one instance of quote
        line = line.strip('\n, ') # strip off newline, commas, whitespace
        if re.match('^{', line):
            dicts.append(new_dict())
        elif re.match('^}{', line):
            dicts.append(new_dict())
            index += 1
        elif re.match('^}$', line):
            pass
        else:
            key,value = line.split(':',1) # don't use split because some values contain colons
            key = key.strip() # get rid of extra white space
            value = value.strip() # get rid of extra white space
            dicts[index][key] = value.strip()
            #print "index is", index, "key is", key, "and value is", value
    
    for d in dicts:
        if 'pci_device.class_id' in d.keys():
            if d['pci_device.class_id'] == '02.80.00' and sys.argv[1] == '-w':
                count += 1
                if count >= 3:
                    nic = nic + ' ' + str(count) + '-'
                elif count == 2:
                    nic = '1-' + nic + ' 2-'
                nic += d['pci_device.vendor_name'] + ' - ' + d['pci_device.product_name'] + ' '
            if d['pci_device.class_id'] == '02.00.00' and sys.argv[1] == '-e':
                count += 1
                if count >= 3:
                    nic = nic + ' NIC' + str(count) + '-'
                elif count == 2:
                    nic = 'NIC1-' + nic + ' NIC2-'
                nic += d['pci_device.vendor_name'] + ' - ' + d['pci_device.product_name'] + ' '
    
    print nic.replace('/','-')

if __name__ == '__main__':
    main()

