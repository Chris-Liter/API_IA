# Usa una imagen base oficial de Python
FROM python:latest

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
RUN pip install Django
RUN pip install djangorestframework

# Copia el resto del proyecto
COPY ./miproyecto .

# Expone el puerto en el que corre la aplicación
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
