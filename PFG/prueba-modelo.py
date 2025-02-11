import numpy as np
#import tensorflow as tf
import tflite_runtime.interpreter as tflite

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
	
	direccion = interpreter.get_tensor(output_details[1]['index'])

	#direccionesPosibles = ["Izquierda", "Centro", "Derecha"]
	direccionesPosibles = ["-1", "0", "1"]
	direccion = direccionesPosibles[np.argmax(direccion_predicha)]
	
	return velocidad, direccion
	
vector_prueba =np.random.rand(96).astype(np.float32)
velocidad_predicha, direccion_predicha = predecir(vector_prueba)

print(f"Velocidad:{velocidad_predicha}, direccion: {direccion_predicha}")
	
