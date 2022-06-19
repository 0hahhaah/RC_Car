import sys
sys.path.append('./Raspi-MotorHAT-python3')

from Raspi_MotorHAT import Raspi_MotorHAT, Raspi_DCMotor
from Raspi_PWM_Servo_Driver import PWM
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtSql
import time
import atexit
from sense_hat import SenseHat


class pollingThread(QThread):
    def __init__(self):
        super().__init__()

    def run(self):
        self.db = QtSql.QSqlDatabase.addDatabase('QMYSQL')
        self.db.setHostName("ec2-3-36-129-200.ap-northeast-2.compute.amazonaws.com")
        self.db.setDatabaseName("2-5")
        self.db.setUserName("ssafy2_5")
        self.db.setPassword("ssafy1234")
        ok = self.db.open()
        print(ok)
        
        self.speed = 100
        self.query = QtSql.QSqlQuery("TRUNCATE TABLE sensing2") #######

        self.sense = SenseHat()
        
        self.mh = Raspi_MotorHAT(addr=0x6f)
        self.myMotor = self.mh.getMotor(2)
        self.myMotor.setSpeed(100)
        
        self.pwm = PWM(0x6f)
        self.pwm.setPWMFreq(60)
        
        while True:
            time.sleep(0.5)
            self.setQuery()
            self.getQuery()

    def setQuery(self):
         pressure = self.sense.get_pressure()
         temp = self.sense.get_temperature()
         humidity = self.sense.get_humidity()
         
         p = round(pressure, 2)
         t = round(temp, 2)
         h = round(humidity, 2)
         
         msg = "Press : " + str(p) + " Temp : " + str(t) + " Humid : " + str(h)
         print(msg)
         
         self.query.prepare("insert into sensing2 (time, num1, num2, num3, meta_string, is_finish) values (:time, :num1, :num2, :num3, :meta, :finish)");
         time = QDateTime().currentDateTime()
         self.query.bindValue(":time", time)
         self.query.bindValue(":num1", p)
         self.query.bindValue(":num2", t)
         self.query.bindValue(":num3", h)
         self.query.bindValue(":meta", "")
         self.query.bindValue(":finish", 0)
         self.query.exec()
         
         self.sense.clear(0, 0, 0)

    
    def getQuery(self):
        query = QtSql.QSqlQuery("select * from command2 order by time desc limit 1");
        query.next()
        cmdTime = query.record().value(0)
        cmdType = query.record().value(1)
        cmdArg = query.record().value(2)
        is_finish = query.record().value(3)

        if is_finish == 0:
            # detect new command
            print(cmdTime.toString(), cmdType, cmdArg)
            # update
            query = QtSql.QSqlQuery("update command2 set is_finish=1 where is_finish=0");

        # motor
        if cmdType == "go": self.go()
        if cmdType == "back": self.back()
        if cmdType == "left": self.left()
        if cmdType == "right": self.right()
        if cmdType == "mid": self.middle()
        if cmdType == "stop": self.stop()
        if cmdType == "faster": self.faster()
        if cmdType == "slower": self.slower()
        
        if cmdType == "front" and cmdArg == "press":
            self.go()
            self.middle()
            
        if cmdType == "front" and cmdArg == "release":
            self.stop()
            
        if cmdType == "leftside" and cmdArg == "press":
            self.go()
            self.left()
            self.sense.set_pixel(0, 7, (255,50,0))

            
        if cmdType == "leftside" and cmdArg == "release":
            self.stop()
            
        if cmdType == "rightside" and cmdArg == "press":
            self.go()
            self.right()
            self.sense.set_pixel(0, 0, (255,50,0))

            
        if cmdType == "rightside" and cmdArg=="release":
            self.stop()

        if cmdType == "setSpeed":
            self.speed = (int(cmdArg)*10 + 50)
            self.myMotor.setSpeed(self.speed)
            
            
                    
    def stop(self):
        self.myMotor.run(Raspi_MotorHAT.RELEASE)
        print('MOTOR STOP')

    def go(self):
        self.myMotor.setSpeed(self.speed)
        self.myMotor.run(Raspi_MotorHAT.FORWARD)
        print("MOTOR GO")

    def back(self):
        self.myMotor.setSpeed(self.speed)
        self.myMotor.run(Raspi_MotorHAT.BACKWARD)
        for i in range(8):
            self.sense.set_pixel(7,i,(255,0,0))
        print("MOTOR BACK")

    def left(self):
        self.pwm.setPWM(0, 0, 200)
        self.sense.set_pixel(0, 7, (255,50,0))
        print("MOTOR LEFT")

    def right(self):
        self.pwm.setPWM(0, 0, 480)
        self.sense.set_pixel(0, 0, (255,50,0))
        print("MOTOR RIGHT")

    def middle(self):
        self.pwm.setPWM(0, 0, 350)
        print("MOTOR MIDDLE")
        
        


th = pollingThread()
th.start()
app = QApplication([])
# infinity loop

while True:
    pass
