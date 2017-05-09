import sys
import ctypes
from PyQt4 import QtGui 
from PyQt4 import QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from socket import *

class Window(QtGui.QMainWindow):
    def __init__(self):
        
        self.serverName='m-gh.info'
        self.serverPort=12000
        self.clientSocket=socket(AF_INET,SOCK_STREAM)
        self.clientSocket.connect((self.serverName,self.serverPort))

        super(Window,self).__init__()
        self.setGeometry(50,50,500,300)
        self.setFixedSize(500,300)
        self.setWindowTitle("Chater")
        self.setWindowIcon(QtGui.QIcon('icon.png'))

        myappid = 'mycompany.myproduct.subproduct.version'  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

        self.textbox_Message = QLineEdit(self)
        self.textbox_Message.setAlignment(Qt.AlignTop)
        self.textbox_Message.move(5, 230)
        self.textbox_Message.resize(380,65)
        self.textbox_Message.returnPressed.connect(self.Send_Message)
        self.textbox_Message.setPlaceholderText("Type Your Message Here....")
        f = self.textbox_Message.font()
        f.setPointSize(18) # sets the size to 27
        self.textbox_Message.setFont(f)

        textbox_Messages_box=QLineEdit(self)
        textbox_Messages_box.setAlignment(Qt.AlignTop)
        textbox_Messages_box.setReadOnly(True)
        textbox_Messages_box.move(5, 5)
        textbox_Messages_box.resize(380,220)
        
        self.centerOnScreen()
        self.home()

    def home(self):
        btn_Send_Text=QtGui.QPushButton("Send",self)
        btn_Send_Text.clicked.connect(self.Send_Message)
        btn_Send_Text.move(390,233)

        btn_Send_File=QtGui.QPushButton("File",self)
        btn_Send_File.clicked.connect(self.Send_File)
        btn_Send_File.move(390,265)
        self.show()
    
    def Send_Message(self):
        sentence=self.textbox_Message.text()
        print(sentence)
        self.clientSocket.sendto(sentence.encode('utf-8'),(self.serverName, self.serverPort))
        modifiedSentence=self.clientSocket.recv(1024)
        print ('From Server:',modifiedSentence.decode())

    def Send_File(self):
        print("Sending File....")

    def close_application(self):
        print("\nClosing...\n")
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