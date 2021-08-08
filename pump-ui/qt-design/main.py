# main.py
# @author Dan Woolsey
#
# PyQt5 interface for Pumpy
#
# NOTE: When testing on laptop will comment out the following lines:
#   from Pumpy import Pumpy
#   self.pump = Pumpy(20,21,5,6,13,16,19)
#
# previous_operations stored data:
#   operation = [datetime, syringe_size, infusion_time, microstepping_value]

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QObject, QThread, pyqtSignal

from datetime import datetime

import sys

from BluetoothHandler import BluetoothHandler
from Pumpy import Pumpy

class Pumpy_Ui(QtWidgets.QMainWindow):

    previous_operations = []

    def __init__(self):
        super(Pumpy_Ui, self).__init__()
        uic.loadUi('ui/pumpy-2.ui', self)

        self.test_label.setText('Opened at ' + datetime.now().strftime("%c"))

        # setup Pumpy
        self.pump = Pumpy(20,21,5,6,13,16,19)
        self.bluetooth_handler = BluetoothHandler()

        # take each widget and connect it to a function of this class
        self.infuse_button.clicked.connect(self.infuse_button_pressed)
        self.infuse_cont.clicked.connect(self.infuse_continuous_pressed)
        self.withdraw_cont.clicked.connect(self.withdraw_continuous_pressed)
        self.prev_operations.triggered.connect(self.open_prev_ops)
        self.connect_bt.clicked.connect(self.connect_to_app)
        self.exit.triggered.connect(self.exit_ui)

        # setup test previous operations
        time = datetime.now().strftime("%c")
        operation = [time, "20ml", 20.0, "1/2"]
        self.previous_operations.append(operation)

        self.showMaximized()

        self.show()

    def infuse_button_pressed(self):
        # use self.infuse_button
        syringe_size = int(self.size_choice.currentText().strip("ml"))
        infusion_time = int(self.time_choice.value()) # might need to wrap with int/float
        ms_value = self.ms_choice.currentText()
        self.test_label.setText(str(syringe_size) + ";" + str(infusion_time) + ";" + ms_value)

        # store the operation in previous operations
        time = datetime.now().strftime("%c")
        operation = [time, self.size_choice.currentText(), infusion_time, ms_value]
        self.previous_operations.append(operation)
        # now to set up the pumping operation
        # just calling self.pump.pump will do it but now am trying threads
        #self.pump.pump(Pumpy.INFUSE, infusion_time, syringe_size, ms_value)
        self.infuse_thread = QThread()
        # our worker will be the variable 'self.pump'
        self.pump.moveToThread(self.infuse_thread)
        print("run moveToThread()")
        # now to connect functions properly
        # this lambda supposedly lets us pass the arguments properly, we will see
        self.infuse_thread.started.connect(lambda: self.pump.pump(Pumpy.INFUSE,
                                        infusion_time, syringe_size, ms_value))
        self.pump.finished.connect(self.infuse_thread.quit)
        # setup deleting thread once done, wont delete worker since thats used elsewhere
        self.infuse_thread.finished.connect(self.infuse_thread.deleteLater)
        # must write reportProgress to display the value of progress to the debug box
        #self.pump.progress.connect(self.reportProgress)
        print("starting thread")
        self.infuse_thread.start()

    def infuse_continuous_pressed(self):
        # uses self.infuse_cont var for the button
        # get given MS value for continuous operations
        ms_value = self.ms_choice_cont.currentText()
        self.pump.continuous(Pumpy.INFUSE, ms_value)
        pass

    def withdraw_continuous_pressed(self):
        # uses self.withdraw_cont var for the button
        # get given MS value for continuous operations
        ms_value = self.ms_choice_cont.currentText()
        self.pump.continuous(Pumpy.WITHDRAW, ms_value)
        pass

    def open_prev_ops(self):
        prev_op_win = PreviousOperations_Ui(self)
        prev_op_win.show()

    def load_prev_ops(self, operation):
        print("will take operation and set input boxes")
        self.test_label.setText(operation[0])
        self.size_choice.setCurrentText(operation[1])
        self.time_choice.setValue(float(operation[2]))
        self.ms_choice.setCurrentText(operation[3])

    def connect_to_app(self):
        try:
            op_data = self.bluetooth_handler.run()
            op_list = op_data[0].split(",")
            syringe_size = int(op_list[0].strip("mL"))
            infuse_time = int(op_list[1])
            ms_value = op_list[2]
            # add this to the list of previous operations
            self.test_label.setText(str(syringe_size) + ";" + str(infuse_time) + ";" + ms_value)

            # store the operation in previous operations
            time = datetime.now().strftime("%c")
            operation = [time, op_list[0], infuse_time, ms_value]
            self.previous_operations.append(operation)
            #self.pump.pump(Pumpy.INFUSE, infuse_time, syringe_size, ms)
            # do this the same way as infuse_button_pressed
            self.infuse_thread = QThread()
            self.pump.moveToThread(self.infuse_thread)
            self.infuse_thread.started.connect(lambda: self.pump.pump(Pumpy.INFUSE,
                                            infuse_time, syringe_size, ms_value))
            self.pump.finished.connect(self.infuse_thread.quit)
            self.infuse_thread.finished.connect(self.infuse_thread.deleteLater)
            print("starting thread")
            self.infuse_thread.start()
        except:
            print("Failure occurred with BluetoothHandler")

    def exit_ui(self):
        sys.exit(0)

class PreviousOperations_Ui(QtWidgets.QMainWindow):

    def __init__(self, parent):
        super().__init__(parent)
        uic.loadUi('ui/prev_op.ui', self)
        self.parent = parent

        # bind functions to buttons
        self.exit_prev_op.clicked.connect(self.exit_ui)
        self.select_prev_op.clicked.connect(self.load_operation)

        # load previous operations into QListView
        for item in parent.previous_operations:
            line = ""
            for attr in item:
                line += str(attr) + "-"
            self.list_prev_op.addItem(line)

    def load_operation(self):
        print("will load the previous operation back into the main window")
        selected = self.list_prev_op.currentItem().text().split("-")
        selected.pop()
        print(selected)
        self.parent.load_prev_ops(selected)
        self.exit_ui()

    def exit_ui(self):
        self.close()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Pumpy_Ui()
    app.exec_()
