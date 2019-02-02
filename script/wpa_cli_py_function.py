
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

import time
import re


class SendCommandException(Exception):
	pass


def sendCommand(socket, socket_file, command, timeout=10.0):
	try:
		socket.settimeout(timeout)
		socket.sendto(command, socket_file)
		data, addr = socket.recvfrom(4096)
	except socket.error:
		raise SendCommandException('Send failed. Command: ' + command)
	except timeout:
		raise SendCommandException('Read timeout. Command: ' + command)

	return data


class SendCommandNotOkException(Exception):
	pass


def sendCommandOkValidated(socket, socket_file, command, timeout=10.0, socket_timeout=5.0):
	try:
		socket.settimeout(timeout)
		socket.sendto(command, socket_file)
		data = '<'
		start_time = time.time()
		while data[0:1] == "<":
			if time.time() - start_time > timeout:
				data = "Timeout waiting for data."
				raise ReadTimeoutException(data)

			socket.settimeout(socket_timeout)
			data, addr = socket.recvfrom(4096)

	except socket.error:
		raise SendCommandException('Send faild. Command: ' + command)
	except timeout:
		raise SendCommandException('Read timeout. Command: ' + command)

	if str(data[0:2]) != 'OK':
		# print "Error: " + command + " " + data
		raise SendCommandNotOkException(command + '\n' + data + '\nKO')

	return command + '\n' + data


def sendAttach(socket, socket_file):
	command = 'ATTACH'
	data = sendCommandOkValidated(socket, socket_file, command, 5.0, 5.0)
	return command + '\n' + data


def sendDetach(socket, socket_file):
	command = 'DETACH'
	data = sendCommandOkValidated(socket, socket_file, command, 5.0, 5.0)
	return command + '\n' + data


def startScan(socket, socket_file):
	command = 'SCAN'
	data = sendCommandOkValidated(socket, socket_file, command, 5.0, 5.0)
	return command + '\n' + data


def selectNetwork(socket, socket_file, net_id):
	command = 'SELECT_NETWORK ' + net_id.rstrip()
	data = sendCommandOkValidated(socket, socket_file, command, 5.0, 5.0)
	return command + '\n' + data


def enableNetwork(socket, socket_file, net_it):
	command = 'ENABLE_NETWORK ' + net_it.rstrip()
	data = sendCommandOkValidated(socket, socket_file, command, 5.0, 5.0)
	return command + '\n' + data


def disableNetwork(socket, socket_file, net_it):
	command = 'DISABLE_NETWORK ' + net_it.rstrip()
	data = sendCommandOkValidated(socket, socket_file, command, 5.0, 5.0)
	return command + '\n' + data


def addNetwork(socket, socket_file):
	command = 'ADD_NETWORK'
	data = sendCommand(socket, socket_file, command, 5.0)
	return data.rstrip(), command + '\n' + data


def removeNetwork(socket, socket_file, id):
	command = 'REMOVE_NETWORK ' + id.rstrip()
	data = sendCommandOkValidated(socket, socket_file, command, 5.0, 5.0)
	return command + '\n' + data


def saveConfig(socket, socket_file):
	command = 'SAVE_CONFIG'
	data = sendCommandOkValidated(socket, socket_file, command, 5.0, 5.0)
	return command + '\n' + data


def setNetworkProperty(socket, socket_file, net_id, net_property, value):
	command = 'SET_NETWORK ' + net_id.rstrip() + ' ' + net_property.rstrip() + ' ' + value.rstrip()
	data = sendCommandOkValidated(socket, socket_file, command)
	return command + '\n' + data


class ReadTimeoutException(Exception):
	pass


def readDataUntilFound(socket, strings_to_find, timeout, socket_timeout=5.0):

	def notFound(to_find, in_str):
		out = True
		for toCheck in to_find:
			found = re.search(toCheck, in_str)
			if found:
				out = False
				break
		return out

	start_time = time.time()
	data = ''
	log_out = ''
	while notFound(strings_to_find, data):
		# Receive data
		# print('# Receive data from server')
		# print 'leggo'
		if time.time() - start_time > timeout:
			data = "Timeout waiting for data."
			log_out += data + '\n'
			raise ReadTimeoutException(log_out)
		try:
			socket.settimeout(socket_timeout)
			data, addr = socket.recvfrom(4096)
			log_out += data + '\n'
		except timeout:
			raise SendCommandException('Read timeout.' + log_out)

	# print '----Scan ' + data
	# print reply
	return data, log_out


def readDataUntil(socket, string_to_find, timeout, socket_timeout=5.0):
	start_time = time.time()
	data = ''
	log_out = ''
	while data != string_to_find:
		# Receive data
		# print('# Receive data from server')
		# print 'leggo'
		if time.time() - start_time > timeout:
			data = "Timeout waiting for data."
			log_out += data + '\n'
			raise ReadTimeoutException(log_out)
		try:
			socket.settimeout(socket_timeout)
			data, addr = socket.recvfrom(4096)
			log_out += data + '\n'
		except timeout:
			raise SendCommandException('Read timeout.' + log_out)

	# print '----Scan ' + data
	# print reply
	return data, log_out


def getScanResultData(socket, socket_file, timeout=5.0, socket_timeout=5.0):

	command = 'SCAN_RESULTS'
	try:
		socket.sendto(command, socket_file)
	except socket.error:
		raise SendCommandException('Send failed. Command: ' + command)

	try:
		data = '<'
		start_time = time.time()
		while data[0:1] == "<":
			if time.time() - start_time > timeout:
				data = "Timeout waiting for data."
				raise ReadTimeoutException(data)

			socket.settimeout(socket_timeout)
			data, addr = socket.recvfrom(4096)

	except timeout:
		raise SendCommandException('Read timeout. Command: ' + command)

	return data


def getNetworkListAndCurrentId(socket, socket_file, out):

	command = 'LIST_NETWORKS'
	out = out + command + '\n'

	data = sendCommand(socket, socket_file, command, timeout=10.0)

	out = out + data + '\n'
	current_network_id = ""
	network_list = []
	data_list = data.split('\n')
	for line in data_list:
		# sys.stdout.write(line[0:4] + '\n')
		if str(line[0:4]) == "netw":
			continue
		line_value = line.split('\t')
		if len(line_value) == 1:
			continue
		net = NetworkItem()
		net.id = line_value[0]
		net.ssid = line_value[1]
		# sys.stdout.write(net.ssid)
		net.bssid = line_value[2]
		if len(line_value) == 4:
			net.flags = line_value[3]
		network_list.append(net)
		if "[CURRENT]" in net.flags:
			current_network_id = net.id
	return network_list, current_network_id, out


class NetworkItem:
	id = ""
	ssid = ""
	bssid = ""
	flags = ""


def setNetworkCrtRspIdentity(socket, socket_file, net_id, value):
	# https://w1.fi/wpa_supplicant/devel/ctrl_iface_page.html

	# prova a gestirle come set_network n identity ....

	command = 'CTRL-RSP-IDENTITY-' + str(net_id.rstrip()) + ':' + value
	data = sendCommandOkValidated(socket, socket_file, command, 5.0, 5.0)
	return command + '\n' + data


def setNetworkCrtRspPassword(socket, socket_file, net_id, value):
	command = 'CTRL-RSP-PASSWORD- ' + net_id + ':' + value
	data = sendCommandOkValidated(socket, socket_file, command, 5.0, 5.0)
	return command + '\n' + data
