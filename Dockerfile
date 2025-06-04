# Usamos una imagen de Python
FROM python:3.11

# Definimos el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos los archivos del proyecto
COPY . .

# Instalamos las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponemos el puerto 8000 para acceder a Django
EXPOSE 8000

# Comando para ejecutar el servidor de Django cuando se inicie el contenedor
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
