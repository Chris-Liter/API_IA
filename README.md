La API se desarrollo con django, donde se usara un modelo de Machine Learning entrenado de obesidad, el cual se usara para predecir el grado de obesidad de las personas, este proyecto se
desplegara usando docker con el `Dockerfile` que incluira las dependencias de para su correcto funcionamiento, que en este caso son `pandas`, `numpy`, `scikit-learn`, `tensorflow`, `keras`,
`django`, `djangorestframework`, `django-cors-headers`, `drf_yasg`, `django.shortcuts`, `awsebcli`.
Y esta API sera desplegada en una maquina virtual de Google Cloud con un contenedor `Dockerfile`.

Los parametros que se pediran al usuario con `Entre comidas`, `Historial Familiar`, `Altura`, `Peso`, `Edad`, cada uno de estos sera dictado en un audio, y sera usado la API de Speech to Text
y se extraera los datos unicos para la predicción con el modelo.

Los datos de usuario se guardaran en una Base de datos `PostgreSQL` donde se tendran 3 tablas, tabla de usuario, tabla de medico, y tabla de turno, donde los datos incluida la prediccion dada
sera guardada en la base de datos. Ademas los medicos se podran ayudar de este prediagnostico que da la IA para poder ayudar al paciente, ademas este `ChatBot` que se podra acceder a el
por medio de `Telegram` y este otorgara sus datos al Chat y el chat le podra asignar un turno al paciente para que el medico le atienda, dependiendo si tiene un nivel de obesidad grave.

Para el caso de los medicos, podran ver los datos de los usuarios con su prediagnostico a travez de la pagina web: 
que usara una API aparte, creada con Spring-Boot para exclusivo consumo de la base de datos, leer y escribir en ella.
