from django.urls import reverse
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from tensorflow.keras.models import load_model
import pickle
import keras

class modeloSNN():
    """Clase modelo Preprocesamiento y SNN"""
    
    def __init__(self):
        pass

    # Función para cargar preprocesador
    def cargarPipeline(self, nombreArchivo):
        with open(nombreArchivo + '.pickle', 'rb') as handle:
            pipeline = pickle.load(handle)
        return pipeline
    
    # Función para cargar red neuronal
    def cargarNN(self, nombreArchivo):  
        model = load_model(nombreArchivo + '.h5')    
        print("Red Neuronal Cargada desde Archivo") 
        return model
    
    # Función para obtener resultados y certezas
    def obtenerResultadosyCertezas(self, lista):
        predicciones = lista.argmax(axis=1)
        marcas = []
        certezas = []
        
        for i, prediccion in enumerate(predicciones):
            certeza = lista[i][prediccion] * 100  # Certeza en porcentaje
            if prediccion == 0:
                marca = 'Peso Bajo'
            elif prediccion == 1:
                marca = 'Peso Normal'
            elif prediccion == 2:
                marca = 'Sobrepeso Nivel 1'
            elif prediccion == 3:
                marca = 'Sobrepeso Nivel 2'
            elif prediccion == 4:
                marca = 'Obesidad Nivel 1'
            elif prediccion == 5:
                marca = 'Obesidad Nivel 2'
            elif prediccion == 6:
                marca = 'Obesidad Nivel 3'
            
            marcas.append(marca)
            certezas.append(f'{certeza:.2f}%')
        
        return predicciones, marcas, certezas
    
    # Función para predecir nuevo cliente
    def predecirNuevoCliente(self, EDAD=23, PESO=50, HISTORIAL_FAMILIAR='no', FAVC='no', CAEC='Sometimes', nombreModelo='resources/modeloRNOptimizadoBalanceado'):
        cnames = ["EDAD", "PESO", "HISTORIAL_FAMILIAR", "FAVC", "CAEC"]
        Xnew = [EDAD, PESO, HISTORIAL_FAMILIAR, FAVC, CAEC]
        Xnew_Dataframe = pd.DataFrame(data=[Xnew], columns=cnames)
        
        pipe = self.cargarPipeline("resources/pipePreprocesadores")
        Xnew_Transformado = pipe.transform(Xnew_Dataframe)
        
        modelo = self.cargarNN(nombreModelo)
        y_pred = modelo.predict(Xnew_Transformado)
        
        predicciones, marcas, certezas = self.obtenerResultadosyCertezas(y_pred)
        
        dataframeFinal = pd.DataFrame({'Predicción': predicciones, 'Resultado': marcas, 'Certeza': certezas})
        
        np.set_printoptions(formatter={'float': lambda x: "{0:0.0f}".format(x)})
        
        return dataframeFinal