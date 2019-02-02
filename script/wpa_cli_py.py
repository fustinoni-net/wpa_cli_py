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

from wpa_cli_py_function import sendCommand, SendCommandException


def main():

    parser = argparse.ArgumentParser(description='Send command directly to wpa_supplicant. Similar to wpa_cli, '
                                                 'but command line only.')
    parser.add_argument("ifname", help="Specify the interface that is being configured.")
    parser.add_argument("command", help="Run a command. See wpa_cli manual for all the possible options.")
    parser.add_argument("params", nargs='*', help="Command params. See wpa_cli manual for all the possible options.",
                        default='')
    args = parser.parse_args()

    server_file = "/var/run/wpa_supplicant/" + args.ifname  # type: str
    client_file = "/tmp/wpa_cli_pi" + str(time.time())

    error = 0
    data = ''

    request = args.command.upper()
    if args.params != '':
        request = request + ' ' + ' '.join(args.params)

    s = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)  # type: socket

    try:

        s.bind(client_file)

        data = sendCommand(s, server_file, request, 5.0)

    except SendCommandException as e1:
        data = data + 'E1: ' + e1.message + '\n'
        error = 1
    except BaseException as be:
        data = data + 'BE: ' + be.message + '\n'
        error = 10
    finally:
        sys.stdout.write(data)
        s.close()
        os.unlink(client_file)
        os.system('rm -f ' + client_file)
        sys.exit(error)


if __name__ == "__main__":
    main()
