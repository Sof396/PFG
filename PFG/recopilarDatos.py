#importar las librerías necesarias
from mpu6050 import mpu6050
import time
import math
import csv

mpu1 = mpu6050(0x68)
mpu2 = mpu6050(0x69)

#todas las posibles direcciones que puede tomar la silla de ruedas
movimientos = ['parada', 'delante','parada', 'atras', 'parada', 'derechaDelante', 'parada','derechaAtras', 'parada', 'izquieraDelante','parada', 'izquieraDentrás ', 'parada' ]
m = 0

direccion = 0
porcentaje = 0
x2_rotacion = 0.0
y1_rotacion = 0.0

while True:
	
	#muestra por pantalla la dirección para que la persona coloque los acelerómetros en esa dirección
	print(movimientos[m])
	time.sleep(1)
	
	lista = []
	
	for i in range (10):
		
		if (i == 0) | (i== 1):
			
			#no se tienen en cuenta las dos primeras vueltas porque se ayume que es movimiento para llegar a la posición correcta
			print('n')
			
		else:
			
					
			accel1_data = mpu1.get_accel_data()
			accel2_data = mpu2.get_accel_data()
	
	
			x1=accel1_data['x']
			y1=accel1_data['y']
			z1=accel1_data['z']
	
			x2=accel2_data['x']
			y2=accel2_data['y']
			z2=accel2_data['z']
			
			#En caso de que alguna de las variables sea 0 se cambia para que las cuentas no den problemas al hacer raices cuadradas
			if x1 == 0.0: x1= 0.01
			if y1 == 0.0: y1= 0.01
			if z1 == 0.0: z1= 0.01
	
			if x2 == 0.0: x2= 0.01
			if y2 == 0.0: y2= 0.01
			if z2 == 0.0: z2= 0.01
	
			x1_rotacion = math.degrees(math.atan(x1/math.sqrt((y1*y1)+(z1*z1))))
			y1_rotacion = math.degrees(math.atan(y1/math.sqrt((x1*x1)+(z1*z1))))
			z1_rotacion = math.degrees(math.atan(z1/math.sqrt((x1*x1)+(y1*y1))))
	
			x2_rotacion = math.degrees(math.atan(x2/math.sqrt((y2*y2)+(z2*z2))))
			y2_rotacion = math.degrees(math.atan(y2/math.sqrt((x2*x2)+(z2*z2))))
			z2_rotacion = math.degrees(math.atan(z2/math.sqrt((x2*x2)+(y2*y2))))
			
			#se añaden a una lista todas las variables que se enviarán
			lista.extend((x1, y1, z1, x2,y2, z2, x1_rotacion, y1_rotacion, z1_rotacion, x2_rotacion, y2_rotacion, z2_rotacion))
			
			time.sleep(0.1)
			
			
	
	#En este caso se determina la dirección de manera tradicional para recopilar los datos
	if(x2_rotacion < (-20)):
		#derecha
		direccion = 1
		
	elif(x2_rotacion > 20):
		#izquiera
		direccion = -1
		
	else:
		direccion = 0
			
			
	if( y1_rotacion < (-15)):
		#delante
		porcentaje = ((-y1_rotacion )/85) *100
		if (porcentaje > 100):
			porcentaje = 100
	elif(y1_rotacion > 15):
		porcentaje = (( -y1_rotacion)/85)*100
		if (porcentaje < -100):
			porcentaje = -100
	else:
		porcentaje = 0
			
		
	lista.extend((direccion, porcentaje))
	print(direccion)
	print(porcentaje)
	
	
	
	file = open('dataMultipeTimes.csv', newline='', mode='a')
	
	with file:
		
		writer = csv.writer(file)
		writer.writerow(lista)
	   
	 
	m = m+1
	m = m % 13
	
	time.sleep(2)
