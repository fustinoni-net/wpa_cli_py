#!/usr/bin/python

import socket
import sys
import os
import time
import argparse



def main(argv):

    parser = argparse.ArgumentParser(description='Send command directly to wpa_supplicant. Similar to wpa_cli, '
                                                 'but command line only.')
    parser.add_argument("ifname", help="Specify the interface that is being configured.")
    parser.add_argument("command", help="Run a command. See wpa_cli manual for all the possible options.")
    parser.add_argument("params", nargs='*', help="Command params. See wpa_cli manual for all the possible options.", default='')
    args = parser.parse_args()

    server_file = "/var/run/wpa_supplicant/" + args.ifname  # type: str
    client_file = "/tmp/wpa_cli_pi" + str(time.time())

    error = 0
    data = ''
    s = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)  # type: socket

    s.bind(client_file)

    # Send data to remote server
    # print('# Sending data to server')
    request = args.command.upper() + ' '.join(args.params)
    #print request


    try:
        try:
            s.sendto(request, server_file)
        except socket.error:
            data = 'Send failed'
            error = 1

         # Receive data
         # print('# Receive data from server')
        try:
            s.settimeout(5.0)
            data, addr = s.recvfrom(4096, )
        except socket.timeout:
            data = 'Read time out'
            error = 2

    finally:
        sys.stdout.write(data + '\n')
        s.close()
        os.unlink(client_file)
        os.system('rm -f ' + client_file)
        sys.exit(error)

if __name__ == "__main__":
	main(sys.argv)
