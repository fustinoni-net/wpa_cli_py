#!/usr/bin/python

#
#   MIT License
#
#   Copyright (c) 2019 Enrico Fustinoni
#
#   Permission is hereby granted, free of charge, to any person obtaining a copy
#   of this software and associated documentation files (the "Software"), to deal
#   in the Software without restriction, including without limitation the rights
#   to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#   copies of the Software, and to permit persons to whom the Software is
#   furnished to do so, subject to the following conditions:
#
#   The above copyright notice and this permission notice shall be included in all
#   copies or substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NON INFRINGEMENT. IN NO EVENT SHALL THE
#   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#   SOFTWARE.
#

import socket
import sys
import os
import time
import argparse
from __builtin__ import int

from wpa_cli_py_function import addNetwork, setNetworkProperty, enableNetwork, disableNetwork, saveConfig, \
    SendCommandNotOkException, removeNetwork, SendCommandException, ReadTimeoutException


def main():

    parser = argparse.ArgumentParser(description='Set WIFI connection parameters using wpa_supplicant. '
                                                 'For more information see: https://w1.fi/cgit/hostap/plain/wpa_supplicant/wpa_supplicant.conf')
    parser.add_argument("ifname", help="Specify the interface that is being used.")
    parser.add_argument("protocol", choices=['OPEN', 'WEP', 'WPA', 'WPA2', 'EAP'],
                        help="Specify the protocol used by the wifi network. Needed to setup the required parameters.", default='')
    # parser.add_argument("-i", "--idNetwork", help="Specify the network id.")
    parser.add_argument("-s", "--ssid", help="The SSID of the network.")
    parser.add_argument("-b", "--bssid", help="The BSSID of the network.")
    parser.add_argument("-P", "--password", help="The network password. Converted in the right parameters needed by the network protocol.")
    parser.add_argument("-r", "--priority",
                        help="The network priority.", default='0', type=lambda d: int(d))
    parser.add_argument("-e", "--enabled",
                        help="Enable the network.", action="store_true")
    parser.add_argument("-k", "--keyMgmt",
                        help="EAP type for EAP connections. See: https://w1.fi/cgit/hostap/plain/wpa_supplicant/wpa_supplicant.conf",
                        choices=['WPA-PSK', 'WPA-EAP', 'NONE', 'WPA-NONE', 'FT-PSK', 'FT-EAP', 'FT-EAP-SHA384', 'WPA-PSK-SHA256', 'WPA-EAP-SHA256', 'SAE', 'FT-SAE', 'WPA-EAP-SUITE-B', 'WPA-EAP-SUITE-B-192', 'OSEN', 'FILS-SHA256', 'FILS-SHA384', 'FT-FILS-SHA256', 'FT-FILS-SHA384', 'OWE', 'DPP'])
    parser.add_argument("-I", "--identity",
                        help="Identity for EAP connections.")
    parser.add_argument("-E", "--eap",
                        help="EAP type for EAP connections.See: https://w1.fi/cgit/hostap/plain/wpa_supplicant/wpa_supplicant.conf",
                        choices=['PEAP', 'TLS', 'TTLS', 'PWD', 'SIM', 'AKA', 'AKA''', 'FAST', 'LEAP'])

    args = parser.parse_args()

    server_file = "/var/run/wpa_supplicant/" + args.ifname  # type: str
    client_file = "/tmp/wpa_cli_pi" + str(time.time())

    if args.ssid:
        args.ssid = '"' + args.ssid + '"'

    if args.password and not args.password.startswith('0x'):
        args.password = '"' + args.password + '"'

    error = 0
    out = ''
    net_id = ''

    s = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)

    try:

        # Removed to be able to connect to any open network.
        # if not args.ssid and not args.bssid:
        #     raise SendCommandNotOkException('ssid or bssid needed' + '\nKO')

        s.bind(client_file)

        net_id, data = addNetwork(s, server_file)
        out = out + data + '\n'

        if args.ssid and args.ssid != '""' and args.ssid != '':
            data = setNetworkProperty(s, server_file, net_id, 'ssid', args.ssid)
            out = out + data + '\n'
        else:
            data = setNetworkProperty(s, server_file, net_id, 'scan_ssid', '1')
            out = out + data + '\n'

        if args.bssid and args.bssid != '':
            data = setNetworkProperty(s, server_file, net_id, 'bssid', args.bssid)
            out = out + data + '\n'

        if args.priority != '':
            data = setNetworkProperty(s, server_file, net_id, 'priority', str(args.priority))
            out = out + data + '\n'

        if args.protocol == 'OPEN':
            print 'Open'
            # open network
            data = setNetworkProperty(s, server_file, net_id, 'key_mgmt', 'NONE')
            out = out + data + '\n'

        elif args.protocol == 'WEP':
            # WEP
            print 'WEP'
            data = setNetworkProperty(s, server_file, net_id, 'key_mgmt', 'NONE')
            out = out + data + '\n'
            if args.password and args.password != '""':
                data = setNetworkProperty(s, server_file, net_id, 'wep_key0', args.password)
                out = out + data + '\n'
                data = setNetworkProperty(s, server_file, net_id, 'wep_tx_keyidx', '0')
                out = out + data + '\n'

        elif args.protocol == 'WPA' or args.protocol == 'WPA2':
            # WAP/WAP2
            print 'WPA'
            if args.password:
                data = setNetworkProperty(s, server_file, net_id, 'psk', args.password)
                out = out + data + '\n'

        elif args.protocol == 'EAP':
            # EAP
            print 'EAP'

            if args.identity:
                data = setNetworkProperty(s, server_file, net_id, 'identity', args.identity)
                out = out + data + '\n'

            if args.password:
                data = setNetworkProperty(s, server_file, net_id, 'password', args.password)
                out = out + data + '\n'

            #  scan_ssid=1

            #  eap=PEAP
            if args.eap:
                data = setNetworkProperty(s, server_file, net_id, 'eap', args.eap)
                out = out + data + '\n'

            #  key_mgmt=WPA-EAP
            data = setNetworkProperty(s, server_file, net_id, 'key_mgmt', args.key_mgmt)
            out = out + data + '\n'

        if args.enabled:
            print 'enabled'
            data = enableNetwork(s, server_file, net_id)
            out = out + data + '\n'
        else:
            data = disableNetwork(s, server_file, net_id)
            out = out + data + '\n'

        data = saveConfig(s, server_file)
        out = out + data + '\n'

    except SendCommandException as e1:
        out = out + 'E1: ' + e1.message + '\n'
        error = 1
    except SendCommandNotOkException as e2:
        out = out + 'E2: ' + e2.message + '\n'
        error = 2

        try:
            data = removeNetwork(s, server_file, net_id)
            out = out + data + '\n'
        except BaseException as ee:
            out = out + ee.message + '\n'

    except ReadTimeoutException as e3:
        out = out + 'E3: ' + e3.message + '\n'
        error = 3
    except BaseException as be:
        out = out + 'BE: ' + be.message + '\n'
        error = 10

    finally:
        sys.stdout.write(out)
        s.close()
        os.unlink(client_file)
        os.system('rm -f ' + client_file)
        sys.exit(error)


if __name__ == "__main__":
    main()
