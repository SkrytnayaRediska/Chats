import binascii
import time
import random
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit,
    QTextEdit, QGridLayout, QApplication, QPushButton,
                             QMainWindow, QFileDialog, QMessageBox)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QRegExp, QMetaObject
import socket
import sys

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.resize(900, 500)
        MainWindow.setWindowTitle("TCP_CHAT")
        self.centralwidget = QWidget(MainWindow)

        self.grd = QGridLayout(self.centralwidget)
        self.grd.setSpacing(10)

        '''                              FONT                              '''

        self.font = QFont()
        self.font.setFamily("Arial")
        self.font.setPointSize(20)


        '''                           TEXT EDITS                           '''
        self.chat_edit = QTextEdit(self.centralwidget)
        self.chat_edit.setReadOnly(True)
        self.grd.addWidget(self.chat_edit, 1, 0, 5, 4)

        self.mess_edit = QTextEdit(self.centralwidget)
        self.grd.addWidget(self.mess_edit, 7, 1, 5, 3)


        '''                           LINE EDITS                           '''

        self.name_edit = QLineEdit(self.centralwidget)
        self.grd.addWidget(self.name_edit, 6, 1, 1, 3)

        '''                             LABELS                              '''

        self.name_lbl = QLabel(self.centralwidget)
        self.name_lbl.setText("Name")
        self.name_lbl.setFont(self.font)
        self.grd.addWidget(self.name_lbl, 6, 0)

        self.mess_lbl = QLabel(self.centralwidget)
        self.mess_lbl.setText("Message")
        self.mess_lbl.setFont(self.font)
        self.grd.addWidget(self.mess_lbl, 8, 0)

        self.emp_lbl = QLabel(self.centralwidget)
        self.grd.addWidget(self.emp_lbl, 7, 1)


        '''                    BUTTONS                   '''

        self.send_mess_btn = QPushButton(self.centralwidget)
        self.send_mess_btn.setText("Send")
        self.grd.addWidget(self.send_mess_btn, 12, 3)

        self.send_file_btn = QPushButton(self.centralwidget)
        self.send_file_btn.setText('Select File')
        self.grd.addWidget(self.send_file_btn, 12, 2)

        self.generate_file_btn = QPushButton(self.centralwidget)
        self.generate_file_btn.setText("Generate File")
        self.grd.addWidget(self.generate_file_btn, 12, 1)


        '''                                 CLIENT                                      '''
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = 'localhost'
        self.port = 8014

        '''Connect with a server'''
        self.sock.connect((self.host, self.port))

        self.file_flag = False
        self.file_name = ''
        self.file_buffer = bytes()
        self.block = 1024

        def select_file():
            fileName = QFileDialog().getOpenFileName()
            filePath = str(fileName[0])

            fileObject = filePath.split('/')
            self.file_name = fileObject[len(fileObject) - 1]

            fl = open(filePath, "rb")
            self.file_buffer = bytes(fl.read())
            self.file_flag = True
            self.mess_edit.setStyleSheet("QTextEdit {color:red}")
            self.mess_edit.setText(self.file_name)
            fl.close()

        def generate_file():
            fl = open('generated_file.txt', "wb")
            file_size = random.randint(50, 1024)
            arr_bytes = []
            for i in range(0, file_size):
                arr_bytes.append(random.randint(0, 255))

            fl.write(bytearray(arr_bytes))
            fl.close()



        def send_func():
            if(self.name_edit.text() != ''):
                if (self.file_flag == True):
                    now = time.time()

                    self.sock.send(bytes('file'.encode('utf-8')))
                    self.sock.send(bytes(self.file_name.encode('utf-8')))
                    name_rec = self.sock.recv(100000)

                    self.sock.send(bytes(self.file_buffer))
                    file_buf_rec = self.sock.recv(100000)

                    then = time.time()
                    delta_time = abs(then - now + 0.000001)
                    speed = len(self.file_buffer) / delta_time
                    blocks_send = len(self.file_buffer) // self.block + 1
                    blocks_rec = len(file_buf_rec) // self.block + 1

                    self.chat_edit.append(self.name_edit.text() + ': ' + name_rec.decode('utf-8') +
                                            '. Received ' + str(blocks_rec) + ' blocks of ' +
                                            str(blocks_send) +
                                          '.\n\tSpeed: ' + str('{0:.4f}').format(speed) + ' bytes/sec.')
                    self.file_flag = False
                    self.mess_edit.setText('')


                else:
                    self.mess_edit.setStyleSheet("QTextEdit {color:black}")
                    self.sock.send(bytes('message'.encode('utf-8')))
                    now = time.time()
                    message = self.mess_edit.toPlainText().encode('utf-8')
                    print('aa ' + self.mess_edit.toPlainText())

                    '''Send data to the server'''
                    self.sock.send(bytes(message))
                    self.chat_edit.append(self.name_edit.text() + ': ' + str(self.mess_edit.toPlainText()))

                    '''Get data from the server'''
                    data = self.sock.recv(10000)
                    print('received', data, len(data), 'bytes')
                    str_data = str(data.decode('utf-8'))
                    then = time.time()
                    delta_time = abs(then - now + 0.000001)
                    speed = len(data)/delta_time
                    self.chat_edit.append('server: received "' + str(str_data) + '", ' +
                                      str(len(data)) + ' bytes. Speed:' +
                                      str('{0:.4f}').format(speed) + ' bytes/sec')
                    self.mess_edit.setText('')


        MainWindow.setCentralWidget(self.centralwidget)
        QMetaObject.connectSlotsByName(MainWindow)

        self.send_mess_btn.clicked.connect(send_func)
        self.send_file_btn.clicked.connect(select_file)
        self.generate_file_btn.clicked.connect(generate_file)



if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())




