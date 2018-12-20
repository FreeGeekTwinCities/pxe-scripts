#!/usr/bin/env python

'''
Takes the dmi file (from hdt dump) as an argument, tallies all the sections 
within that have 'Memory Bank' *and* 'DIMM' or 'SODIMM' in them.  If you count 
just 'Memory Bank', you also pickup ROM chips on some machines, which is not 
what we want.
'''

import re
import sys

# Define a function that returns a dictionary
def new_dict(): return {}

def main():
    dicts = []
    index = 0
    f = open(sys.argv[1])
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
            #print "key is", key, "and value is", value
    
    banks = 0
    for d in dicts:
        if 'Memory Bank' in d.keys():
            if re.match('DIMM', d['dmi.memory.form_factor']) or re.match('SODIMM', d['dmi.memory.form_factor']) or re.match('RIMM', d['dmi.memory.form_factor']):
                #print 'Found Memory Bank'
                banks += 1
    
    print banks

if __name__ == "__main__":
    main()
