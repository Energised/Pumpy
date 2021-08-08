#!/usr/bin/python3
# server.py
#
# Testing suite for setting up a Bluetooth connection to my android app
# and receiving data byte by byte

import bluetooth

server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_sock.bind(("", bluetooth.PORT_ANY))
server_sock.listen(1)

uuid="94f39d29-7d6d-437d-973b-fba39e49d4ee"

port = server_sock.getsockname()[1]

bluetooth.advertise_service(server_sock, "SampleServer", service_id=uuid,
                            service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS],
                            profiles=[bluetooth.SERIAL_PORT_PROFILE])

print("Waiting for connection on RFCOMM channel ", port)

client_sock, client_info = server_sock.accept()
print("Accepted connection from ", client_info)

try:
    while True:
        data = client_sock.recv(1024)
        if not data:
            break
        print("Recieved ", data)
except OSError:
    pass

print("Disconnected")

client_sock.close()
server_sock.close()
print("Done")
