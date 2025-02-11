#Alba Payo Fernández
#Código Control Robot

#importación librerías
import RPi.GPIO as GPIO
from time import sleep
import sys
import socket
import ast
HOST=''
PORT=50001

#Variables de los motores del robot
enaA = 18
in1 = 23
in2 = 24

enaB = 19
in3 = 5
in4 = 6

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#Clase Motor
class Motor():
	#Función inicialización
	def __init__(self,EnaA,In1,In2,EnaB,In3,In4):
		self.EnaA=enaA
		self.In1=in1
		self.In2=in2
		self.EnaB=enaB
		self.In3=in3
		self.In4=in4
		
		GPIO.setup(self.EnaA,GPIO.OUT)
		GPIO.setup(self.In1,GPIO.OUT)
		GPIO.setup(self.In2,GPIO.OUT)

		GPIO.setup(self.EnaB,GPIO.OUT)
		GPIO.setup(self.In3,GPIO.OUT)
		GPIO.setup(self.In4,GPIO.OUT)


		self.pwmMotorA=GPIO.PWM(self.EnaA,1000)
		self.pwmMotorB=GPIO.PWM(self.EnaB,1000)

		self.pwmMotorA.start(0)
		self.pwmMotorB.start(0)
		
	#Función movimiento recto hacia delante
	def moveF(self,x):
		GPIO.output(self.In1,GPIO.HIGH)
		GPIO.output(self.In2,GPIO.LOW)
		GPIO.output(self.In3,GPIO.LOW)
		GPIO.output(self.In4,GPIO.HIGH)
		self.pwmMotorA.ChangeDutyCycle(x)
		self.pwmMotorB.ChangeDutyCycle(x)

	#Función movimiento recto hacia detrás
	def moveB(self,x):
		GPIO.output(self.In1,GPIO.LOW)
		GPIO.output(self.In2,GPIO.HIGH)
		GPIO.output(self.In3,GPIO.HIGH)
		GPIO.output(self.In4,GPIO.LOW)
		self.pwmMotorA.ChangeDutyCycle(x)
		self.pwmMotorB.ChangeDutyCycle(x)
	
	#Función movimiento giro a la izquierda hacia delante
	def moveL(self,x):
		GPIO.output(self.In1,GPIO.HIGH)
		GPIO.output(self.In2,GPIO.LOW)
		GPIO.output(self.In3,GPIO.LOW)
		GPIO.output(self.In4,GPIO.LOW)
		self.pwmMotorA.ChangeDutyCycle(x)
		self.pwmMotorB.ChangeDutyCycle(0)

	#Función movimiento giro a la izquierda hacia detrás
	def moveLB(self,x):
		GPIO.output(self.In1,GPIO.LOW)
		GPIO.output(self.In2,GPIO.LOW)
		GPIO.output(self.In3,GPIO.HIGH)
		GPIO.output(self.In4,GPIO.LOW)
		self.pwmMotorA.ChangeDutyCycle(0)
		self.pwmMotorB.ChangeDutyCycle(x)

	#Función movimiento giro a la derecha hacia delante	
	def moveR(self,x):
		GPIO.output(self.In1,GPIO.LOW)
		GPIO.output(self.In2,GPIO.LOW)
		GPIO.output(self.In3,GPIO.LOW)
		GPIO.output(self.In4,GPIO.HIGH)
		self.pwmMotorA.ChangeDutyCycle(0)
		self.pwmMotorB.ChangeDutyCycle(x)

	#Función movimiento giro a la derecha hacia detrás
	def moveRB(self,x):
		GPIO.output(self.In1,GPIO.LOW)
		GPIO.output(self.In2,GPIO.HIGH)
		GPIO.output(self.In3,GPIO.LOW)
		GPIO.output(self.In4,GPIO.LOW)
		self.pwmMotorA.ChangeDutyCycle(x)
		self.pwmMotorB.ChangeDutyCycle(0)

	#Función no movimiento
	def stop(self):
		GPIO.output(self.In1,GPIO.LOW)
		GPIO.output(self.In2,GPIO.LOW)
		GPIO.output(self.In3,GPIO.LOW)
		GPIO.output(self.In4,GPIO.LOW)
		self.pwmMotorA.ChangeDutyCycle(0)

#Función que según la dirección y velocidad llama a las de movimiento
def mandar_robot(direccion,velocidad):
    if(direccion==0):
        if(velocidad==0):
            motor1.stop()
        elif(velocidad>0):
            motor1.moveF(velocidad)
        else:
            motor1.moveB(abs(velocidad))
    if(direccion==1):
        if(velocidad==0):
            motor1.stop()
        elif(velocidad>0):
            motor1.moveR(velocidad)
        else:
            motor1.moveRB(abs(velocidad))
    if(direccion==-1):
        if(velocidad==0):
            motor1.stop()
        elif(velocidad>0):
            motor1.moveL(velocidad)
        else:
            motor1.moveLB(abs(velocidad))

#Establece la conexión con el otro subsistema
with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
    s.bind((HOST,PORT))
    s.listen(1)
    conn,addr=s.accept()
    motor1 = Motor(enaA,in1,in2,enaB,in3,in4)
    with conn:
        print('Connected by',addr)
        while True:
	    #Se reciben los datos, se modifican y se pasan a dirección y velocidad
            data=conn.recv(1024)
            if not data:break
            string=data.decode('utf8')
            pautas=ast.literal_eval(string)
            print(pautas)
            direccion=pautas['direccion']
            velocidad=pautas['porcentaje']
	    #Se llama a la función que proboca los movimientos del robot
            mandar_robot(direccion,velocidad)
	    #Se manda un mensaje de que está listo para recibir los próximos datos
            conn.send(bytes('True','utf-8'))