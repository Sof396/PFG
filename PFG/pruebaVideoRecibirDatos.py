

#importación librerías
from time import sleep
import sys
import socket
import ast
HOST=''
PORT=50001

#Establece la conexión con el otro subsistema
with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
    s.bind((HOST,PORT))
    s.listen(1)
    conn,addr=s.accept()
    #motor1 = Motor(enaA,in1,in2,enaB,in3,in4)
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
            #mandar_robot(direccion,velocidad)
	    #Se manda un mensaje de que está listo para recibir los próximos datos
            conn.send(bytes('True','utf-8'))