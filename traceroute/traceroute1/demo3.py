#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Multi-source traceroute with geolocation information.
"""

import datetime
import json
import optparse
import os
import re
import signal
import sys
import urllib
import urllib2
from subprocess import Popen, PIPE

USER_AGENT = "traceroute/1.0 (+https://github.com/ayeowch/traceroute)"


class Traceroute(object):
    """
    Multi-source traceroute instance.
    """
    def __init__(self, ip_address, source=None, tmp_dir="/tmp",
                 no_geo=False, timeout=120, debug=False):
        super(Traceroute, self).__init__()
        self.ip_address = ip_address
        self.source = source
        if self.source is None:
            cur_dir = os.path.dirname(os.path.abspath(__file__))
            json_file = open(os.path.join(cur_dir, "sources.json"), "r").read()
            sources = json.loads(json_file.replace("_IP_ADDRESS_", ip_address))
            self.source = sources["LO"]
        self.tmp_dir = tmp_dir
        self.timeout = timeout
        self.debug = debug

    def traceroute(self):
        """
        Instead of running the actual traceroute command, we will fetch
        standard traceroute results from several publicly available webpages
        that are listed at traceroute.org. For each hop, we will then attach
        geolocation information to it.
        """
        self.print_debug("ip_address={}".format(self.ip_address))

        filename = "{}.txt".format(self.ip_address)
        filepath = os.path.join(self.tmp_dir, filename)

        if not os.path.exists(filepath):
            status_code, traceroute = self.execute_cmd(self.source['url'])
            if status_code != 0 and status_code != 200:
                return {'error': status_code}
            open(filepath, "w").write(traceroute)
        traceroute = open(filepath, "r").read()

        print(traceroute)

    def execute_cmd(self, cmd):
        """
        Executes given command using subprocess.Popen().
        """
        stdout = ""
        returncode = -1
        process = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        try:
            signal.signal(signal.SIGALRM, self.signal_handler)
            signal.alarm(self.timeout)
            stdout, stderr = process.communicate()
            returncode = process.returncode
            self.print_debug("cmd={}, returncode={}".format(cmd, returncode))
            if returncode != 0:
                self.print_debug("stderr={}".format(stderr))
            signal.alarm(0)
        except Exception as err:
            self.print_debug(str(err))
        return (returncode, stdout)


    def signal_handler(self, signum, frame):
        """
        Raises exception when signal is caught.
        """
        raise Exception("Caught signal {}".format(signum))

    def print_debug(self, msg):
        """
        Prints debug message to standard output.
        """
        if self.debug:
            print("[DEBUG {}] {}".format(datetime.datetime.now(), msg))


def main():
    cmdparser = optparse.OptionParser("%prog --ip_address=IP_ADDRESS")
    cmdparser.add_option(
        "-i", "--ip_address", type="string", default="8.8.8.8",
        help="IP address of destination host (default: 8.8.8.8)")
    cmdparser.add_option(
        "-j", "--json_file", type="string", default="sources.json",
        help="List of sources in JSON file (default: sources.json)")
    cmdparser.add_option(
        "-t", "--tmp_dir", type="string", default="./text",
        help=("Temporary directory to store downloaded traceroute results "
              "(default: /tmp)"))
    cmdparser.add_option(
        "-n", "--no_geo", action="store_true", default=False,
        help="No geolocation data (default: False)")
    cmdparser.add_option(
        "-s", "--timeout", type="int", default=120,
        help="Timeout in seconds for all downloads (default: 120)")
    cmdparser.add_option(
        "-d", "--debug", action="store_true", default=False,
        help="Show debug output (default: False)")
    options, _ = cmdparser.parse_args()
    json_file = open(options.json_file, "r").read()
    sources = json.loads(json_file.replace("_IP_ADDRESS_", options.ip_address))
    traceroute = Traceroute(ip_address=options.ip_address,
                            source=sources["LO"],
                            tmp_dir=options.tmp_dir,
                            no_geo=options.no_geo,
                            timeout=options.timeout,
                            debug=options.debug)
    traceroute.traceroute()
    # print(json.dumps(hops, indent=4))
    return 0


if __name__ == '__main__':
    sys.exit(main())