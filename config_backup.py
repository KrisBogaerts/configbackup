#!/usr/bin/python

import paramiko
import time
import sys
import getopt
import argparse
import fabric

__author__ = 'Kris Bogaerts'


parser = argparse.ArgumentParser(description='Configuration backup creator')
parser.add_argument('-i', '--input', help='Input file name', required=True)
parser.add_argument('-o', '--output', help='Output file name', required=True)
parser.add_argument('-u', '--user', help='Username', required=True)
parser.add_argument('-ip', '--ipaddress', help='IP address', required=True)
parser.add_argument('-p', '--passw', help='Password (optional with key based authentication')
args = parser.parse_args()
username = args.user
password = args.passw
ip = args.ipaddress

# show values ##
# print ("Input file: %s" % args.input)
# print ("Output file: %s" % args.output)
# print ("username: %s" % args.user)
# print ("Pass: %s" % args.passw)
# print ("IP address: %s" % args.ipaddress)

# Create file for output
file1 = open(args.input, "r")
file2 = open(args.output, "a")

lines = (file1.readlines())


try:
    # Create instance of SSHClient object
    remote_conn_pre = paramiko.SSHClient()

    # Automatically add untrusted hosts (make sure okay for security policy in your environment)
    remote_conn_pre.set_missing_host_key_policy(
    paramiko.AutoAddPolicy())

    # initiate SSH connection
    remote_conn_pre.connect(ip, username=username, password=password)
    print "SSH connection established to %s\n" % ip

    # Use invoke_shell to establish an 'interactive session'
    remote_conn = remote_conn_pre.invoke_shell()
    print "Interactive SSH session established\n"

finally:
    # Strip the initial prompt
    output = remote_conn.recv(1000)

    # Create loop for file input
    for inputlines in lines:
        if inputlines.startswith("cmd:"):
            cmd = inputlines.replace("cmd:", '')
            remote_conn.send(cmd)
            remote_conn.send("\n")

            # wait 2 seconds for completion
            time.sleep(2)

            output = remote_conn.recv(200000)
            file2.write(output)
            print output

remote_conn.close()
# file1.close()
# file2.close()



