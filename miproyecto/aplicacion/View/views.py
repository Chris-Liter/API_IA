from django.shortcuts import render
from aplicacion.Logica import modeloSNN #para utilizar el método inteligente
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
import json
from django.http import JsonResponse

class Clasificacion():
    def determinarAprobacion(request):
        return render(request, "index.html")
    
    @api_view(['GET', 'POST'])
    def predecir(request):
        if request.method == 'POST':
            try:
                # Obtener datos de entrada del request
                EDAD = int(request.POST.get('EDAD'))
                PESO = float(request.POST.get('PESO'))
                HISTORIAL_FAMILIAR = str(request.POST.get('HISTORIAL_FAMILIAR'))
                FAVC = str(request.POST.get('FAVC'))
                CAEC = str(request.POST.get('CAEC'))
                
                # Crear instancia de la clase modeloSNN
                modelo = modeloSNN.modeloSNN()  # Asegúrate de que la clase sea accesible
                
                # Realizar predicción con los datos proporcionados
                resultado = modelo.predecirNuevoCliente(
                    EDAD=EDAD,
                    PESO=PESO,
                    HISTORIAL_FAMILIAR=HISTORIAL_FAMILIAR,
                    FAVC=FAVC,
                    CAEC=CAEC
                )
                
                # Convertir el resultado a JSON y devolverlo
                # resultado_json = json.dumps(resultado)
                return resultado
            except Exception as e:
                return JsonResponse({"error": str(e)})
        else:
            return JsonResponse({"error": "Método no permitido"}, status=405)

    @csrf_exempt
    @api_view(['GET', 'POST'])
    def predecirIOJson(request):
        print(request)
        print('***********************************************')
        print(request.body)
        print('***********************************************')
        if request.method == 'POST':
            try:
                body = json.loads(request.body.decode('utf-8'))
                
                # Obtener datos de entrada del request
                EDAD = int(body.get('EDAD'))
                PESO = float(body.get('PESO'))
                HISTORIAL_FAMILIAR = str(body.get('HISTORIAL_FAMILIAR'))
                FAVC = str(body.get('FAVC'))
                CAEC = str(body.get('CAEC'))
                
                # Crear instancia de la clase modeloSNN
                modelo = modeloSNN.modeloSNN()
                
                # Realizar predicción con los datos proporcionados
                resultado = modelo.predecirNuevoCliente(
                    EDAD=EDAD,
                    PESO=PESO,
                    HISTORIAL_FAMILIAR=HISTORIAL_FAMILIAR,
                    FAVC=FAVC,
                    CAEC=CAEC,
                    nombreModelo='resources/modeloRNOptimizadoBalanceado'  # Asegúrate de que el modelo esté accesible
                )
                
                # Convertir el resultado a JSON y devolverlo
                resultado_json = {
                    "Predicción": resultado['Predicción'].tolist(),
                    "Resultado": resultado['Resultado'].tolist(),
                    "Certeza": resultado['Certeza'].tolist()
                }
                
                return JsonResponse(resultado_json)
            except Exception as e:
                return JsonResponse({"Error": str(e)})
        else:
            return JsonResponse({"error": "Método no permitido"}, status=405)
