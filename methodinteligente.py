from flask import Flask, request, jsonify
import pathlib
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from tensorflow.keras.models import load_model
import pickle

app = Flask(__name__)

# Función para cargar el pipeline de preprocesamiento
def cargarPipeline(nombreArchivo):
    with open(nombreArchivo+'.pickle', 'rb') as handle:
        pipeline = pickle.load(handle)
    print("Pipeline de preprocesamiento cargado desde archivo")
    return pipeline

# Función para cargar el modelo entrenado
def cargarModelo(nombreArchivo):
    model = load_model(nombreArchivo+'.h5')
    print("Modelo entrenado cargado desde archivo")
    return model

# Función para preprocesar los datos y realizar la predicción
def predecirNuevoCliente(Age=20, Race='Black', TStage='T1', NStage='N1', SixthStage='IIB', differentiate='Poorly differentiated', Grade='3', AStage='Regional', 
                            TumorSize=10, EstrogenStatus='Positive', ProgesteroneStatus='Negative', RegionalNodeExamined=20, ReginolNodePositive=8):    
    cnames=['Age', 'Race', 'TStage', 'NStage', 'SixthStage', 'differentiate',
       'Grade', 'AStage', 'TumorSize', 'EstrogenStatus',
       'ProgesteroneStatus', 'RegionalNodeExamined',
       'ReginolNodePositive']
    Xnew=[Age, Race, TStage, NStage, SixthStage, differentiate, Grade, AStage, 
          TumorSize, EstrogenStatus, ProgesteroneStatus, RegionalNodeExamined, 
          ReginolNodePositive]

    Xnew_Dataframe = pd.DataFrame(data=[Xnew],columns=cnames)
    pipe = cargarPipeline("pipeBalanceado")
    Xnew_Transformado = pipe.transform(Xnew_Dataframe)
    modelo = cargarModelo("modeloRedNeuronalBase")
    y_pred = (modelo.predict(Xnew_Transformado) > 0.5).astype("int32")
    pred = y_pred.flatten()[0]

    if pred == 1:
        resultado = 'Crédito Aprobado. Felicidades =)'
    else:
        resultado = 'Crédito Negado. Lo sentimos, intenta en otra ocasión'

    return resultado

# Rutas de prueba para verificar el funcionamiento del método de machine learning
@app.route("/")
def hello():
    return "Hola Mundo!"

@app.route("/predecirCliente1")
def predecirCliente1():
    resultado = predecirNuevoCliente(PLAZOMESESCREDITO=10, MONTOCREDITO=40000, TASAPAGO=5, EDAD=25, CANTIDADPERSONASAMANTENER=3, EMPLEO='A173')
    return resultado

@app.route("/predecirCliente2")
def predecirCliente2():
    resultado = predecirNuevoCliente(PLAZOMESESCREDITO=10, MONTOCREDITO=400000, TASAPAGO=5, EDAD=25, CANTIDADPERSONASAMANTENER=3, EMPLEO='A173')
    return resultado

if __name__ == '__main__':
    app.run()

