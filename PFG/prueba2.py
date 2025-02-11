#Importación librerías
import RPi.GPIO as GPIO
import socket
from mpu6050 import mpu6050
import time
import math
import numpy as np
import tflite_runtime.interpreter as tflite

#Inicialización variables
#HOST='172.20.10.6'
#HOST='192.168.165.199'  #ip robot
#PORT=50001 
mpu=mpu6050(0x68)
mpu2=mpu6050(0x69)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.IN)
pautas={'direccion':'','porcentaje':''}

interpreter = tflite.Interpreter(model_path='model.tflite')
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

def predecir (entrada):
    entrada = np.array(entrada, dtype=np.float32)
    entrada = entrada.reshape(1,96)
	
    interpreter.set_tensor(input_details[0]['index'], entrada)
	
    interpreter.invoke()
	
    velocidad = interpreter.get_tensor(output_details[0]['index'])
    #está normalizaca, para llevarla al rango original
    velocidad = velocidad[0] * 100
    
    direccion = interpreter.get_tensor(output_details[1]['index'])

	#direccionesPosibles = ["Izquierda", "Centro", "Derecha"]
    direccionesPosibles = ["-1", "0", "1"]
    direccion = direccionesPosibles[np.argmax(direccion)]
	
    return velocidad, direccion

def leer_datos(accel_data):
    x=accel_data['x']
    y=accel_data['y']
    z=accel_data['z']
    return x,y,z
if(True):
        while True:

            lista = []
            
            for i in range (10):
                if (i == 0) | (i== 1):
			        #no se tienen en cuenta las dos primeras vueltas porque se ayume que es movimiento para llegar a la posición correcta
                    #print('n')
                    pass
                else:
                    x1,y1,z1=leer_datos(mpu.get_accel_data())
                    x2,y2,z2=leer_datos(mpu2.get_accel_data())
            
                    if x1 == 0.0: x=0.01
                    if y1 == 0.0: y=0.01
                    if z1 == 0.0: z=0.01
                    if x2 == 0.0: x2=0.01
                    if y2 == 0.0: y2=0.01
                    if z2 == 0.0: z2=0.01

                    x1_rotacion = math.degrees(math.atan(x1/math.sqrt((y1*y1)+(z1*z1))))
                    y1_rotacion = math.degrees(math.atan(y1/math.sqrt((x1*x1)+(z1*z1))))
                    z1_rotacion = math.degrees(math.atan(z1/math.sqrt((x1*x1)+(y1*y1))))
	
                    x2_rotacion = math.degrees(math.atan(x2/math.sqrt((y2*y2)+(z2*z2))))
                    y2_rotacion = math.degrees(math.atan(y2/math.sqrt((x2*x2)+(z2*z2))))
                    z2_rotacion = math.degrees(math.atan(z2/math.sqrt((x2*x2)+(y2*y2))))

                    #se añaden a una lista todas las variables que se enviarán
                    lista.extend((x1, y1, z1, x2,y2, z2, x1_rotacion, y1_rotacion, z1_rotacion, x2_rotacion, y2_rotacion, z2_rotacion))

                    time.sleep(0.1)
            
            porcentaje, direccion = predecir(lista)

            vector=[direccion,porcentaje]
            pautas['direccion']=direccion
            pautas['porcentaje']=porcentaje
            print(pautas)