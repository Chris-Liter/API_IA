# Usa una imagen base oficial de Python
FROM python:3.9-slim-buster


# Establece el directorio de trabajo
WORKDIR /app

# Copia el archivo de requerimientos y el proyecto en el contenedor
COPY ./miproyecto .

# Instala las dependencias
RUN pip install --upgrade pip

# WORKDIR /app

# RUN pip install -r requirements.txt
RUN pip install pandas
RUN pip install numpy
RUN pip install scikit-learn
RUN pip install tensorflow
RUN pip install keras
RUN pip install django
RUN pip install djangorestframework
RUN pip install --upgrade pip setuptools
RUN pip install django-cors-headers
RUN pip install drf_yasg
RUN pip install keras
RUN pip install django.shortcuts
RUN pip install awsebcli


# Copia el resto del proyecto
COPY ./miproyecto .

# Expone el puerto en el que corre la aplicación
EXPOSE 8000
EXPOSE 8001

# Comando para ejecutar la aplicación
ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8001"]


