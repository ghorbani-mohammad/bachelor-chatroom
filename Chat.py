import sys
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
    clearUserList = pyqtSignal()
    def __init__(self):
        self.chatRoomWindow()

    def handle_clearUserList(self):
        print("User List Clearing")
        self.userList.clear()
        print("User List Cleared")

    def chatRoomWindow(self):
        super(Window, self).__init__()
        myappid = 'mycompany.myproduct.subproduct.version'  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

        nameDialog=QtGui.QInputDialog(None, QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint)
        nameDialog.setWindowTitle("Your Name")
        # nameDialog.setTextValue("Please Insert Your Name")
        nameDialog.setLabelText("Please Insert Your Name")
        nameDialog.setWindowIcon(QtGui.QIcon('icon.png'))
        nameDialog.setInputMode(QInputDialog.TextInput)
        nameDialog.setOkButtonText("Join")
        ok=nameDialog.exec()
        self.name=nameDialog.textValue()
        if ok:
            print(self.name)
        else:
            sys.exit()


        self.clearUserList.connect(self.handle_clearUserList)

        # self.serverName = 'm-gh.info'
        self.serverName = 'localhost'

        self.serverPort = 12000
        self.clientSocket = socket(AF_INET, SOCK_STREAM)

        self.serverPortFTP = 12001
        # self.clientSocketFTP = socket(AF_INET, SOCK_STREAM)

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
        f.setPointSize(12)
        self.textbox_Message.setFont(f)

        self.textbox_Messages_box = QTextBrowser(self)
        # self.textbox_Messages_box.setAlignment(Qt.AlignTop)
        self.textbox_Messages_box.setOpenLinks(False)
        self.textbox_Messages_box.anchorClicked.connect(self.downFile)
        self.textbox_Messages_box.setReadOnly(True)
        self.textbox_Messages_box.move(5, 5)
        self.textbox_Messages_box.resize(380, 220)

        self.userList = QTextBrowser(self)
        # self.textbox_Messages_box.setAlignment(Qt.AlignTop)
        self.userList.setOpenLinks(False)
        # self.textbox_Messages_box.anchorClicked.connect(self.downFile)
        self.userList.setReadOnly(True)
        self.userList.move(390, 5)
        self.userList.resize(100, 220)
        # self.userList.clear()

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
        print("sending j")
        self.clientSocket.sendall(("j").encode('utf-8'))
        size=len(self.name)
        size="{:<5}".format(size)
        self.clientSocket.sendall(size.encode('utf-8'))
        self.clientSocket.sendall(self.name.encode('utf-8'))

    def Send_Message(self):
        self.clientSocket.sendall(("m").encode('utf-8'))
        sentence=self.textbox_Message.text()
        size = len(sentence)
        size = "{:<5}".format(size)
        self.clientSocket.sendall(size.encode('utf-8'))
        self.textbox_Message.setText("")
        print(sentence)
        self.clientSocket.sendall(sentence.encode('utf-8'))

    def Select_File(self):
        print("Sending File....")
        fileName = QFileDialog.getOpenFileName(self, 'Choose a TXT File','',"Text Files (*.txt)")
        # if !fileName.isEmpty && !fileName.isNull():
        if fileName:
            self.clientSocket.sendall(("u").encode('utf-8'))
            fileName=os.path.basename(fileName)#Getting Pure File Name
            size = len(fileName)
            size = "{:<5}".format(size)
            self.clientSocket.sendall(size.encode('utf-8'))
            self.clientSocket.sendall(fileName.encode('utf-8'))
            try:
                _thread.start_new_thread(self.Send_file,(fileName,))
                print("Thread Created")
            except:
                print("Unable To Start New Thread")

    def Send_file(self,fileName):
        self.clientSocketFTP = socket(AF_INET, SOCK_STREAM)
        self.clientSocketFTP.connect((self.serverName,self.serverPortFTP))
        file=open(fileName,'rb')
        l = file.read()
        file.close()
        # print(l)
        size = len(l)
        size = "{:<5}".format(size)
        self.clientSocketFTP.sendall(size.encode('utf-8'))
        self.clientSocketFTP.sendall(l)
        time.sleep(.5)
        self.clientSocketFTP.close()
        print("Ftp Connection Is Closed!")


    def Getting_Messages(self,conn):
        time.sleep(.5)
        while 1:
            event=conn.recv(1)
            event=event.decode()
            print("Getting Messages: "+event)
            if event=='j':
                print("Joined")
                #self.clearUserList.emit()
                size = conn.recv(5)
                size = size.decode()
                size = int(size)
                names = conn.recv(size)
                names = names.decode()
                names = names.split(',')
                print(names)
                name=names[-1]
                welcome="<span style=\"color:red;\">" + name+" Joined To Chat" + "</span>"
                self.textbox_Messages_box.append(welcome + '\n')
                for name in names:
                    self.userList.append(name)
            elif event=='q':
                #self.clearUserList.emit()
                size = conn.recv(5)
                size = size.decode()
                size = int(size)
                names = conn.recv(size)
                names = names.decode()
                names = names.split(',')
                name = names[0]
                bye = "<span style=\"color:brown;\">" + name + " Left The Chat" + "</span>"
                self.textbox_Messages_box.append(bye + '\n')
                for name in names[1:]:
                    self.userList.append(name)
            elif event=='m':
                size = conn.recv(5)
                size = size.decode()
                size = int(size)
                message=conn.recv(size)
                message=message.decode()
                self.textbox_Messages_box.append(message + '\n')
            elif event=='u':
                size = conn.recv(5)
                size = size.decode()
                size = int(size)
                message=conn.recv(size)
                message=message.decode()
                self.textbox_Messages_box.append(message + '\n')
            else:
                time.sleep(.5)
                self.textbox_Messages_box.append(event+'\n')

    def downFile(self,url):
        url=str(url.toString())
        print("anchor clicked!")
        fileName = QFileDialog.getSaveFileName(self, 'Determining A Path For Saving TXT File', '', "Text Files (*.txt)")
        if fileName:
            fileName = os.path.basename(fileName)  # Getting Pure File Name
            print(fileName)

            self.clientSocket.sendall(("d").encode('utf-8'))
            size = len(fileName)
            size = "{:<5}".format(size)
            self.clientSocket.sendall(size.encode('utf-8'))
            self.clientSocket.sendall(url.encode('utf-8'))
            try:
                _thread.start_new_thread(self.Get_File, (fileName,))
                print("Thread Created")
            except:
                print("Unable To Start New Thread")

    def Get_File(self,fileName):
        self.clientSocketFTP = socket(AF_INET, SOCK_STREAM)
        self.clientSocketFTP.connect((self.serverName, self.serverPortFTP))
        size = self.clientSocketFTP.recv(5)
        size = size.decode()
        size = int(size)
        data = self.clientSocketFTP.recv(size)
        myFile = open(fileName, "wb+")
        myFile.write(data)
        myFile.close()
        print(data)
        self.clientSocketFTP.close()
        print("Ftp Connection Is Closed!")
        QtGui.QMessageBox.information(None,"Succssful Operation","Downloading File Is Complete!")

    def closeEvent(self,event):
        print("\nClosing...\n")
        self.clientSocket.sendall(("q").encode('utf-8'))
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
