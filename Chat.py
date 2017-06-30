import sys
from PyQt4 import QtGui

app=QtGui.QApplication(sys.argv)

window=QtGui.QWidget()
window.setGeometry(50,50,500,300)
window.setWindowTitle("Chater")

window.show()


sys.exit(app.exec_())

import os
import ctypes
import _thread
import time
from PyQt4 import QtGui 
from PyQt4 import QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from socket import *



class Window(QtGui.QMainWindow):
    
    def __init__(self):
        self.chatRoomWindow()

    def chatRoomWindow(self):
        super(Window, self).__init__()
        myappid = 'mycompany.myproduct.subproduct.version'  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

        nameDialog=QtGui.QInputDialog(None, QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint)
        nameDialog.setWindowTitle("Insert Your Name")
        nameDialog.setWindowIcon(QtGui.QIcon('icon.png'))
        nameDialog.setInputMode(QInputDialog.TextInput)
        nameDialog.setOkButtonText("Join")
        ok=nameDialog.exec()
        self.name=nameDialog.textValue()
        if ok:
            print(self.name)
        else:
            sys.exit()

        self.serverName = 'm-gh.info'
        self.serverPort = 12000
        self.clientSocket = socket(AF_INET, SOCK_STREAM)

        try:
            self.clientSocket.connect((self.serverName, self.serverPort))
            self.Join()
        except:
            print("Unable To Establish Connection")
            sys.exit()

        try:
            _thread.start_new_thread(self.Getting_Messages, (self.clientSocket,))
            print("Thread Created")
        except:
            print("Unable To Start New Thread")
            sys.exit()

        self.setGeometry(50, 50, 500, 300)
        self.setFixedSize(500, 300)
        self.setWindowTitle("Chater")
        self.setWindowIcon(QtGui.QIcon('icon.png'))

        self.textbox_Message = QLineEdit(self)
        self.textbox_Message.setAlignment(Qt.AlignTop)
        self.textbox_Message.move(5, 230)
        self.textbox_Message.resize(380, 65)
        self.textbox_Message.returnPressed.connect(self.Send_Message)
        self.textbox_Message.setPlaceholderText("Type Your Message Here....")
        f = self.textbox_Message.font()
        f.setPointSize(18)
        self.textbox_Message.setFont(f)

        self.textbox_Messages_box = QTextEdit(self)
        # self.textbox_Messages_box.setAlignment(Qt.AlignTop)
        self.textbox_Messages_box.setReadOnly(True)
        self.textbox_Messages_box.move(5, 5)
        self.textbox_Messages_box.resize(380, 220)

        self.centerOnScreen()
        self.home()


    def home(self):
        btn_Send_Text=QtGui.QPushButton("Send",self)
        btn_Send_Text.clicked.connect(self.Send_Message)
        btn_Send_Text.move(390,233)

        btn_Send_File=QtGui.QPushButton("File",self)
        btn_Send_File.clicked.connect(self.Select_File)
        btn_Send_File.move(390,265)
        self.show()

    def Join(self):
        self.clientSocket.sendto(("j").encode('utf-8'), (self.serverName, self.serverPort))
        self.clientSocket.sendto(self.name.encode('utf-8'), (self.serverName, self.serverPort))
    
    def Send_Message(self):
        self.clientSocket.sendto(("m").encode('utf-8'),(self.serverName, self.serverPort))
        sentence=self.textbox_Message.text()
        self.textbox_Message.setText("")
        print(sentence)
        self.clientSocket.sendto(sentence.encode('utf-8'),(self.serverName, self.serverPort))

    def Select_File(self):
        print("Sending File....")
        fileName = QFileDialog.getOpenFileName(self, 'Choose a TXT File','',"Text Files (*.txt)")
        
        self.clientSocket.sendall(("f").encode('utf-8'))
        fileName=os.path.basename(fileName)#Getting Pure File Name
        self.clientSocket.sendall(fileName.encode('utf-8'))
        try:
            _thread.start_new_thread(self.Send_file,(fileName,))
            print("Thread Created")
        except:
            print("Unable To Start New Thread")

    def Send_file(self,fileName):
        self.serverPortFTP=12001
        self.clientSocketFTP=socket(AF_INET,SOCK_STREAM)
        self.clientSocketFTP.connect((self.serverName,self.serverPortFTP))

        file=open(fileName,'rb')
        l = file.read()
        file.close()
        print(l)
        self.clientSocketFTP.sendall(l)
        # status=self.clientSocketFTP.recv(1024)
        # self.clientSocketFTP.close()
        # self.textbox_Messages_box.append(status.decode()+'\n')
        
    
    def Getting_Messages(self,conn):
        while 1:
            modifiedSentence=conn.recv(1024)
            if not modifiedSentence:
                break
            self.textbox_Messages_box.append(modifiedSentence.decode()+'\n')
        
    def closeEvent(self,event):
        print("\nClosing...\n")
        self.clientSocket.sendto(("c").encode('utf-8'), (self.serverName, self.serverPort))
        time.sleep(.5)
        self.clientSocket.sendto(self.name.encode('utf-8'), (self.serverName, self.serverPort))
        # event.ignore()
        sys.exit()

    def centerOnScreen (self):
        resolution = QtGui.QDesktopWidget().screenGeometry()
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                  (resolution.height() / 2) - (self.frameSize().height() / 2)-50)


def run():
    app=QtGui.QApplication(sys.argv)
    GUI=Window()
    sys.exit(app.exec_())

run()
