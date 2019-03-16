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


import argparse
import os
import socket
import sys
import time

from wpa_cli_py_function import sendWpsPbc, sendWpsPin
from wpa_cli_py_function import sendAttach, readDataUntilFound, \
    sendDetach, SendCommandNotOkException, SendCommandException, ReadTimeoutException


def main():

    parser = argparse.ArgumentParser(description='Force wpa_supplicant to connect to a network using wps.')
    parser.add_argument("ifname", help="Specify the interface that is being used.")
    parser.add_argument("-p", "--pin", help="If present the wps_pin connection will be use.")
    parser.add_argument("-b", "--bssid", help="The BSSID of the network. Specific for connections using pin. The default calue is any.", default='any')
    args = parser.parse_args()

    server_file = "/var/run/wpa_supplicant/" + args.ifname  # type: str
    client_file = "/tmp/wpa_cli_pi" + str(time.time())

    out = ''
    error = 0

    s = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)

    try:

        s.bind(client_file)

        data = sendAttach(s, server_file)
        out = out + data + '\n'

        if args.pin:
            data = sendWpsPin(s, server_file, args.bssid, args.pin)
        else:
            data = sendWpsPbc(s, server_file)

        out = out + data + '\n'

        data, log_out = readDataUntilFound(s, ['^<3>CTRL-EVENT-CONNECTED ', '<3>WPS-TIMEOUT ', '^<3>Association request to the driver failed', '^<4>Failed to initiate sched scan', '^FAIL\n'], 60, 5)
        out = out + log_out + '\n'

        data = sendDetach(s, server_file)
        out = out + data + '\n'

    except SendCommandException as e1:
        out = out + 'E1: ' + e1.message + '\n'
        error = 1
    except SendCommandNotOkException as e2:
        out = out + 'E2: ' + e2.message + '\n'
        error = 2
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
