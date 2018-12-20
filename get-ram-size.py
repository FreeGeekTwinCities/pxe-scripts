#!/usr/bin/env python

'''
Takes the memory file (from hdt dump) as an argument, parses it into a list of
dictionaries, then searches that list for the e820 dictionary, and looks in 
that for the value assigned to the key memory.total.size (MiB).  That value
is typically, e.g., 511MB, and is then rounded to the most nearest commonly
known value, e.g., 511 is rounded to 512.
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
        if 'dmi.item' in d.keys():
            if d['dmi.item'] == 'memory via e820':
                ram =  int(d['memory.total.size (MiB)'])
                if 220 < ram < 280:
                    print '256MB'
                elif 340 < ram < 398:
                    print '384MB'
                elif 440 < ram < 530:
                    print '512MB'
                elif 550 < ram < 650:
                    print '640MB'
                elif 690 < ram < 790:
                    print '768MB'
                elif 900 < ram < 1100:
                    print '1GB'
                elif 1099 < ram < 1300:
                    print '1.2GB'
                elif 1400 < ram < 1600:
                    print '1.5GB'
                elif 1900 < ram < 2100:
                    print '2GB'
                elif 2300 < ram < 2700:
                    print '2.5GB'
                elif 2900 < ram < 3100:
                    print '3GB'
                elif 3300 < ram < 3700:
                    print '3.5GB'
                elif 3800 < ram < 4200:
                    print '4GB'
                else:
                    print ram, 'MB'

if __name__ == '__main__':
    main()

