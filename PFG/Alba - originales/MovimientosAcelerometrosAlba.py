# Alba Payo Fernández
# Codigo Movimientos Acelerómetros

#Importación librerías
import RPi.GPIO as GPIO
import socket
from mpu6050 import mpu6050
import time
import math

#Inicialización variables
#HOST='172.20.10.6'
HOST='192.168.165.199'  #ip robot
PORT=50001 
mpu=mpu6050(0x68)
mpu2=mpu6050(0x69)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.IN)
pautas={'direccion':'','porcentaje':''}

#Función que lee los datos del fichero de inicialización
def leer_fichero():
    with open('/home/pi/Documents/fichero_setup','r') as f:
        derecha=float(f.readline())
        izquierda=float(f.readline())
        delante=float(f.readline())
        cero_max=float(f.readline())
        cero_min=float(f.readline())
        detras=float(f.readline())
        return derecha,izquierda,delante,cero_max,cero_min,detras

#Función que devuelve los valores de las aceleraciones en los tres ejes
def leer_datos(accel_data):
    x=accel_data['x']
    y=accel_data['y']
    z=accel_data['z']
    return x,y,z
if(True):
    
#Establecemos la conexión con el otro subsistema
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
        s.connect((HOST,PORT))
        derecha,izquierda,delante,cero_max,cero_min,detras=leer_fichero()
        while True:
#Leemos los datos de los acelerómetros
            x,y,z=leer_datos(mpu.get_accel_data())
            x2,y2,z2=leer_datos(mpu2.get_accel_data())
            
            if x == 0.0: x=0.01
            if y == 0.0: y=0.01
            if z == 0.0: z=0.01
            if x2 == 0.0: x2=0.01
            if y2 == 0.0: y2=0.01
            if z2 == 0.0: z2=0.01
            #print(x2, y2, z2)

    #Calculamos ángulos de rotación
            x_rotation=math.degrees(math.atan(x/math.sqrt((y*y)+(z*z))))
            y_rotation2=math.degrees(math.atan(y2/math.sqrt((x2*x2)+(z2*z2))))
            print(x_rotation, y_rotation2)

    #Analizamos los ángulos y calculamos dirección y porcentaje
            if(y_rotation2<cero_min):
                rango=abs(delante)+cero_min
                valor=-y_rotation2+cero_min
                porcentaje=valor/rango*100
                if(porcentaje>100):
                    porcentaje=100
            elif(y_rotation2>cero_max):
                rango=detras-cero_max
                valor=y_rotation2-cero_max
                porcentaje=-valor/rango*100
                if(porcentaje<-100):
                    porcentaje=-100
            else:
                porcentaje=0
            if(x_rotation<derecha):
                direccion=1
            elif(x_rotation>izquierda):
                direccion=-1
            else:
                direccion=0
            vector=[direccion,porcentaje]
            pautas['direccion']=direccion
            pautas['porcentaje']=porcentaje
            print(pautas)

    #Se mandan los datos al otro subsistema
            s.send(bytes(str(pautas),'utf8'))

    #Se bloquea hasta recibir confirmación del otro subsistema
            data=s.recv(1024)
            time.sleep(0.1)
