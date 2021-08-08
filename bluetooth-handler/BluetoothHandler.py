#!/usr/bin/python3
# BluetoothHandler.py
# @author Dan Woolsey
#
# Handler class to setup Bluetooth connection to Android Application
# And receive data to be used by the Pumpy GUI
#
# NOTE: Superclassing QObject in order to thread this class with PyQt5

import bluetooth

from PyQt5.QtCore import QObject, QThread, pyqtSignal

class BluetoothHandler(QObject):

    UUID = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

    def __init__(self):
        self.buffer = []
        self.recieved_data = []
        self.server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.server_sock.bind(("", bluetooth.PORT_ANY))
        self.server_sock.listen(1)

        self.port = self.server_sock.getsockname()[1]

    # Thread starts:
    #   - Waits for connection from android app
    #   - Once connection is made, accept and go into while loop
    #   - Gets data sent, then adds it to the buffer list
    #   - TODO: Buffer needs to be shared with Pumpy
    #   - Connection broken, returns complete buffer
    # Thread ends
    # (NOTE: Thread should restart and wait for a connection again)

    def run(self):
        bluetooth.advertise_service(self.server_sock, "PumpyServer",
                                    service_id=BluetoothHandler.UUID,
                                    service_classes=[BluetoothHandler.UUID, bluetooth.SERIAL_PORT_CLASS],
                                    profiles=[bluetooth.SERIAL_PORT_PROFILE])
        print("Waiting for Bluetooth communication")
        client_sock, client_info = self.server_sock.accept()
        print("Accepted connection from ", client_info)
        try:
            while True:
                # recieve a byte
                data = client_sock.recv(1024)
                str_data = str(data, 'utf-8')
                if not data:
                    break
                self.buffer.append(str_data)
                print("Recieved: %s" % str_data)
        except OSError as err:
            print("ERROR: %s" % err)
        finally:
            self.recieved_data = [entry for entry in self.buffer]
            return self.recieved_data

if __name__ == "__main__":
    handler = BluetoothHandler()
    data = handler.run()
    print(data)
