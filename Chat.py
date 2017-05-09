import sys
import ctypes
from PyQt4 import QtGui 
from PyQt4 import QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class Window(QtGui.QMainWindow):
    def __init__(self):
        super(Window,self).__init__()
        self.setGeometry(50,50,500,300)
        self.setFixedSize(500,300)
        self.setWindowTitle("Chater")
        self.setWindowIcon(QtGui.QIcon('icon.png'))

        myappid = 'mycompany.myproduct.subproduct.version'  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

        textbox_Message = QLineEdit(self)
        textbox_Message.setAlignment(Qt.AlignTop)
        textbox_Message.move(5, 230)
        textbox_Message.resize(380,65)
        textbox_Message.setPlaceholderText("Type Your Message Here....")

        textbox_Messages_box=QLineEdit(self)
        textbox_Messages_box.setAlignment(Qt.AlignTop)
        textbox_Messages_box.setReadOnly(True)
        textbox_Messages_box.move(5, 5)
        textbox_Messages_box.resize(380,220)
        
        self.centerOnScreen()
        self.home()

    def home(self):
        btn_Send_Text=QtGui.QPushButton("Send",self)
        btn_Send_Text.clicked.connect(self.close_application)
        btn_Send_Text.move(390,233)

        btn_Send_File=QtGui.QPushButton("File",self)
        btn_Send_File.clicked.connect(self.close_application)
        btn_Send_File.move(390,265)
        self.show()
    
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