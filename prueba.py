from django.shortcuts import render
from appCreditoBanco.Logica import modeloSNN #para utilizar el método inteligente
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
import json
from django.http import JsonResponse

class Clasificacion():
    def determinarAprobacion(request):
        return render(request, "aprobacioncreditos.html")
    @api_view(['GET','POST'])
    def predecir(request):
        try:
            #Formato de datos de entrada
            PLAZOMESESCREDITO = int(request.POST.get('PLAZOMESESCREDITO'))
            MONTOCREDITO = float(request.POST.get('MONTOCREDITO'))
            TASAPAGO = float(request.POST.get('TASAPAGO'))
            EDAD = int(''+request.POST.get('EDAD'))
            CANTIDADPERSONASAMANTENER= int(''+request.POST.get('CANTIDADPERSONASAMANTENER'))
            EMPLEO=request.POST.get('EMPLEO')
            #Consumo de la lógica para predecir si se aprueba o no el crédito
            resul=modeloSNN.modeloSNN.predecirNuevoCliente(modeloSNN.modeloSNN,PLAZOMESESCREDITO=PLAZOMESESCREDITO,MONTOCREDITO=MONTOCREDITO,TASAPAGO=TASAPAGO,EDAD=EDAD,CANTIDADPERSONASAMANTENER=CANTIDADPERSONASAMANTENER,EMPLEO=EMPLEO)
        except:
            resul='Datos inválidos'
        return render(request, "informe.html",{"e":resul})
    @csrf_exempt
    @api_view(['GET','POST'])
    def predecirIOJson(request):
        print(request)
        print('***********************************************')
        print(request.body)
        print('***********************************************')
        body = json.loads(request.body.decode('utf-8'))
        #Formato de datos de entrada
        PLAZOS = int(body.get("PLAZOMESESCREDITO"))
        MONTOCREDITO = float(body.get("MONTOCREDITO"))
        TASAPAGO = float(body.get("TASAPAGO"))
        EDAD = int(body.get("EDAD"))
        CANTIDADPERSONASAMANTENER= int(body.get("CANTIDADPERSONASAMANTENER"))
        EMPLEO=str(body.get("EMPLEO"))
        print(PLAZOS)
        print(MONTOCREDITO)
        print(TASAPAGO)
        print(EDAD)
        print(CANTIDADPERSONASAMANTENER)
        print(EMPLEO)
        resul=modeloSNN.modeloSNN.predecirNuevoCliente(modeloSNN.modeloSNN,PLAZOMESESCREDITO=PLAZOS,MONTOCREDITO=MONTOCREDITO,TASAPAGO=TASAPAGO,EDAD=EDAD,CANTIDADPERSONASAMANTENER=CANTIDADPERSONASAMANTENER,EMPLEO=EMPLEO)  
        data = {'result': resul}
        resp=JsonResponse(data)
        resp['Access-Control-Allow-Origin'] = '*'
        return resp
    

def predecirNuevoCliente(self,ESTADOCUENTACORRIENTE='A12', PLAZOMESESCREDITO=6, HISTORIALCREDITO='A34', PROPOSITOCREDITO='A43',
                                MONTOCREDITO=1169, SALDOCUENTAAHORROS='A65', TIEMPOACTUALEMPLEO='A75', TASAPAGO=4, 
                                ESTADOCIVILYSEXO='A93', GARANTE='A101', TIEMPORESIDENCIAACTUAL=4, ACTIVOS='A121', EDAD=67, 
                                VIVIENDA='A152', CANTIDADCREDITOSEXISTENTES=2, EMPLEO='A173', CANTIDADPERSONASAMANTENER=2,
                                TRABAJADOREXTRANJERO='A201'):  
        pipe=self.cargarModelo(self)
        cnames=['ESTADOCUENTACORRIENTE','PLAZOMESESCREDITO','HISTORIALCREDITO','PROPOSITOCREDITO','MONTOCREDITO',
                'SALDOCUENTAAHORROS','TIEMPOACTUALEMPLEO','TASAPAGO','ESTADOCIVILYSEXO','GARANTE','TIEMPORESIDENCIAACTUAL',
                'ACTIVOS','EDAD','VIVIENDA','CANTIDADCREDITOSEXISTENTES','EMPLEO','CANTIDADPERSONASAMANTENER',
                'TRABAJADOREXTRANJERO']
        Xnew=[ESTADOCUENTACORRIENTE,PLAZOMESESCREDITO,HISTORIALCREDITO,PROPOSITOCREDITO,MONTOCREDITO,SALDOCUENTAAHORROS,
              TIEMPOACTUALEMPLEO,TASAPAGO,ESTADOCIVILYSEXO,GARANTE,TIEMPORESIDENCIAACTUAL,ACTIVOS,EDAD,VIVIENDA,
              CANTIDADCREDITOSEXISTENTES,EMPLEO,CANTIDADPERSONASAMANTENER,TRABAJADOREXTRANJERO]
        
        Xnew_Dataframe = pd.DataFrame(data=[Xnew],columns=cnames)
        print(Xnew_Dataframe)
        pred = (pipe.predict(Xnew_Dataframe) > 0.5).astype("int32")
        print(pred)
        pred = pred.flatten()[0]# de 2D a 1D
        if pred==1:
            pred='Aprobado. Felicidades =)'
        else:
            pred='Negado. Lo sentimos, intenta en otra ocasión'
        return pred
