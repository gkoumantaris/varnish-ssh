#!/usr/bin/env python

# Copyright (C) 2014:
#     Georgios Koumantari, gkoumantaris@gmail.com
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
#


'''
 This script is a check for lookup at varnish statistics over ssh without
 having an agent on the other side
'''
import os
import sys
import optparse
import base64
import subprocess
try:
    import paramiko
except ImportError:
    print "ERROR : this plugin needs the python-paramiko module. Please install it"
    sys.exit(2)

# Ok try to load our directory to load the plugin utils.
my_dir = os.path.dirname(__file__) 
sys.path.insert(0, my_dir) 

try:
    import schecks
except ImportError:
    print "ERROR : this plugin needs the local schecks.py lib. Please install it"
    sys.exit(2)


VERSION = "0.1"
#DEFAULT_WARNING = '1,1,1'
#DEFAULT_CRITICAL = '2,2,2'


def get_stats(client):
    # We are looking for varnish statistics
    raw = r"""echo "$(varnishstat -1 -f client_conn,client_drop,client_req,cache_hit,cache_miss,backend_conn,backend_unhealthy,backend_fail,backend_busy,n_object,n_wrk,n_wrk_failed,n_lru_nuked,fetch_failed | awk '{print $1, " ", $3}')" """  
    stdin, stdout, stderr = client.exec_command(raw)
    stdin.close()
    stats = []
    for line in stdout.read().splitlines():
        stats.append( line )
  # print line

  # Before return, close the client
    client.close()

  #return load1, load5, load15, nb_cpus
    return stats

parser = optparse.OptionParser(
    "%prog [options]", version="%prog " + VERSION)
parser.add_option('-H', '--hostname',
    dest="hostname", help='Hostname to connect to')
parser.add_option('-p', '--port',
    dest="port", type="int", default=22,
    help='SSH port to connect to. Default : 22')
parser.add_option('-i', '--ssh-key',
    dest="ssh_key_file",
    help='SSH key file to use. By default will take ~/.ssh/id_rsa.')
parser.add_option('-u', '--user',
    dest="user", help='remote use to use. By default shinken.')
parser.add_option('-P', '--passphrase',
    dest="passphrase", help='SSH key passphrase. By default will use void')
parser.add_option('-w', '--warning',
    dest="warning",
    help='Warning value for value. Default : 75%')
parser.add_option('-c', '--critical',
    dest="critical",
    help='Critical value for value. In percent. Must be '
        'superior to warning value. Default : 90%')

if __name__ == '__main__':
#    Ok first job : parse args
    opts, args = parser.parse_args()
    if args:
        parser.error("Does not accept any argument.")

    hostname = opts.hostname
    if not hostname:
        print "Error : hostname parameter (-H) is mandatory"
        sys.exit(2)
    port = opts.port
    ssh_key_file = opts.ssh_key_file or os.path.expanduser('~/.ssh/id_rsa')
    user = opts.user or 'shinken'
    passphrase = opts.passphrase or ''

    # Ok now connect, and try to get values for memory
    client = schecks.connect(hostname, port, ssh_key_file, passphrase, user)
    statistics = get_stats(client)
    perfdata = ''
    for i in range(len(statistics)):
        statistics[i]=statistics[i].replace("   ","=")  
    perfdata += ' '.join(statistics)
    print "OK | %s" % (perfdata)
    sys.exit(0)
