from PyQt5.QtWidgets import *
from PyQt5.uic import *
from PyQt5 import QtSql
from PyQt5.QtCore import *
time = QDateTime().currentDateTime()


class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("hi.ui", self)
              
        self.db = QtSql.QSqlDatabase.addDatabase('QMYSQL')
        self.db.setHostName("ec2-3-36-129-200.ap-northeast-2.compute.amazonaws.com")
        self.db.setDatabaseName("2-5")
        self.db.setUserName("ssafy2_5")
        self.db.setPassword("ssafy1234")
        ok = self.db.open()
        print(ok)
        
        
        #self.query = QtSql.QSqlQuery()
        self.query = QtSql.QSqlQuery("TRUNCATE TABLE command2") ###########
        self.timer = QTimer()
        self.timer.setInterval(10)
        self.timer.timeout.connect(self.pollingQuery)
        self.timer.start()
        
    def pollingQuery(self):
        #command log
        self.query = QtSql.QSqlQuery("select * from command2 order by time desc limit 10")
        str = ""
        #self.text.clear()
        while (self.query.next()):
            self.record = self.query.record()
            str += "%s | %10s | %10s | %4d\n" % (self.record.value(0).toString(), self.record.value(1), self.record.value(2), self.record.value(3))
            self.text.appendPlainText(str)
            
        #sensing log
        self.query = QtSql.QSqlQuery("select * from sensing2 order by time desc limit 10")
        str = ""
        while (self.query.next()):
            self.record = self.query.record()
            str += "%s | %10s | %10s | %10s\n" % (self.record.value(0).toString(), self.record.value(1), self.record.value(2), self.record.value(3))
            self.text2.setPlainText(str)            
            #ldc display
            self.lcdTemp.display(self.record.value(2))
            self.lcdHumi.display(self.record.value(3))
            
    def commandQuery(self, cmd, arg):
        self.query.prepare("insert into command2 (time, cmd_string, arg_string, is_finish) values (:time, :cmd, :arg, :finish)")
        time = QDateTime().currentDateTime()
        self.query.bindValue(":time", time)
        self.query.bindValue(":cmd", cmd)
        self.query.bindValue(":arg", arg)
        self.query.bindValue(":finish", 0)
        self.query.exec()
    
    def clickedGo(self):
        print('go')
        self.commandQuery("go", "1 sec")
        
    def clickedLeft(self):
        print('left')
        self.commandQuery("left", "1 sec")
        
    def clickedRight(self):
        print('right')
        self.commandQuery("right", "1 sec")
        
    def clickedMid(self):
        print('mid')
        self.commandQuery("mid", "1 sec")

    def clickedBack(self):
        print('back')
        self.commandQuery("back", "1 sec")

    def clickedFaster(self):
        print('speed up')
        self.commandQuery('faster', 'press')
        
    def clickedSlower(self):
        print('speed down')
        self.commandQuery('slower', 'press')
        
    def clickedStop(self):
        print('stop')
        self.commandQuery('stop', '1sec')
        
    def LeftPress(self):
        #print('press')
        self.commandQuery("leftside", "press")
        
    def LeftRelease(self):
        #print('release')
        self.commandQuery("leftside", "release")
    
    def RightPress(self):
        #print('press')
        self.commandQuery("rightside", "press")
        
    def RightRelease(self):
        #print('release')
        self.commandQuery("rightside", "release")
        
    def FrontPress(self):
        #print('press')
        self.commandQuery("front", "press")
        
    def FrontRelease(self):
        #print('release')
        self.commandQuery("front", "release")

    def setSpeed(self):
        self.commandQuery("setSpeed", self.speed.value())


app = QApplication([])
win = MyApp()
win.show()
app.exec()
        