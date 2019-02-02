#!/bin/bash

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




INSTALL_DIR=/sbin/

cp script/wpa_cli_py.py ${INSTALL_DIR}wpa_cli_py
cp script/wpa_cli_py_connect_to_network.py ${INSTALL_DIR}wpa_cli_py_connect_to_network
cp script/wpa_cli_py_create_network.py ${INSTALL_DIR}wpa_cli_py_create_network
cp script/wpa_cli_py_function.py ${INSTALL_DIR}wpa_cli_py_function.py
cp script/wpa_cli_py_scan_results.py ${INSTALL_DIR}wpa_cli_py_scan_results

chmod +x ${INSTALL_DIR}wpa_cli_py
chmod +x ${INSTALL_DIR}wpa_cli_py_connect_to_network
chmod +x ${INSTALL_DIR}wpa_cli_py_create_network
chmod +x ${INSTALL_DIR}wpa_cli_py_scan_results



