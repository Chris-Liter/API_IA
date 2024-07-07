from django.urls import reverse
import pandas as pd
from sklearn.pipeline import Pipeline
from tensorflow.python.keras.models import load_model, model_from_json
from keras import backend as K
from aplicacion.Logica import modeloSNN
import pickle
import keras

class modeloSNN():
    """Clase modelo Preprocesamiento y SNN"""
    #Función para cargar preprocesador
    def cargarPipeline(self,nombreArchivo):
        with open(nombreArchivo+'.pickle', 'rb') as handle:
            pipeline = pickle.load(handle)
        return pipeline
    #Función para cargar red neuronal 
    def cargarNN(self,nombreArchivo):  
        model = keras.models.load_model(nombreArchivo+'.h5')
        print("Red Neuronal Cargada desde Archivo") 
        return model
    #Función para integrar el preprocesador y la red neuronal en un Pipeline
    def cargarModelo(self):
        #Se carga el Pipeline de Preprocesamiento
        nombreArchivoPreprocesador='resources/pipeBalanceado'
        pipe=self.cargarPipeline(self,nombreArchivoPreprocesador)
        print('Pipeline de Preprocesamiento Cargado')
        cantidadPasos=len(pipe.steps)
        print("Cantidad de pasos: ",cantidadPasos)
        print(pipe.steps)
        #Se carga la Red Neuronal
        modeloOptimizado=self.cargarNN(self,'resources/modeloRedNeuronalOptimizadaTransformado')
        #Se integra la Red Neuronal al final del Pipeline
        pipe.steps.append(['modelNN',modeloOptimizado])
        cantidadPasos=len(pipe.steps)
        print("Cantidad de pasos: ",cantidadPasos)
        print(pipe.steps)
        print('Red Neuronal integrada al Pipeline')
        return pipe
    #La siguiente función permite predecir si se aprueba o no un crédito a un nuevo cliente. 
    #En la función se define el valor por defecto de las variables, se crea el dataframe con los nuevos valores y 
    #los nombres de las variables. 
    #El método "predict" ejecuta el Pipeline: los pasos de transformación y la clasificación (mediante la red neuronal). 
    #Así se predice si el cliente es bueno (1) o malo (0). 
    def predecirNuevoCliente(self, Age=20, Race='Black', TStage='T1', NStage='N1', SixthStage='IIB', differentiate='Poorly differentiated', Grade='3', AStage='Regional', 
                            TumorSize=10, EstrogenStatus='Positive', ProgesteroneStatus='Negative', RegionalNodeExamined=20, ReginolNodePositive=8):    
        
        pipe=self.cargarModelo(self)

        cnames=['Age', 'Race', 'TStage', 'NStage', 'SixthStage', 'differentiate',
        'Grade', 'AStage', 'TumorSize', 'EstrogenStatus',
        'ProgesteroneStatus', 'RegionalNodeExamined',
        'ReginolNodePositive']
        Xnew=[Age, Race, TStage, NStage, SixthStage, differentiate, Grade, AStage, 
            TumorSize, EstrogenStatus, ProgesteroneStatus, RegionalNodeExamined, 
            ReginolNodePositive]

        Xnew_Dataframe = pd.DataFrame(data=[Xnew],columns=cnames)
        print(Xnew_Dataframe)
        pred = (pipe.predict(Xnew_Dataframe) > 0.5).astype("int32")
        print(pred)
        pred = pred.flatten()[0]# de 2D a 1D

        if pred == 1:
            resultado = 'No te vas a morir. Felicidades =)'
        else:
            resultado = 'Te vas a morir :( lo siento mucho'

        return resultado