# Aplicación Yolo

Nuestra aplicación consiste en el reconocimiento de objetos usando las librerías como OpenCV y Yolo. Cada vez que la aplicación encuentra a una persona usando su celular esta notificará a través de un bot en Telegram.

## Instalación

Lo primero que debemos hacer si queremos usar la aplicación es clonar el repositorio y dirigirnos a la carpeta de este:

```
git clone https://github.com/cesaralvarod/aplicacion-yolo
cd aplicacion-yolo/
```

Descargamos los modelos pre-entrenados de Yolo v3:

```
cd weights/
sh ./download_weights.sh
```

Nota: Si eres usuario de Windows puedes descargar los modelos pre-entrenados de Yolo v3 en el siguiente link y copiarlos en la carpeta *weights*:

```
https://pjreddie.com/media/files/yolov3.weights
```

Una vez descarguemos nuestros weights de yolo nos redirigimos a la raíz del proyecto y creamos un ambiente con Anaconda:

```
cd ..
conda create --name lobe-app python=3.9.12
```

Activamos nuestro ambiente de Anaconda:

```
conda activate lobe-app
```

Una vez trabajando en nuestro ambiente de Anaconda, instalamos nuestras librerías de python:

```
pip install -r requirements.txt
```

Lo anteriormente mencionado es necesario si queremos usar nuestra aplicación con envío de notificaciones a través de un bot de Telegram.
Para ejecutar nuestra aplicación debemos escribir el siguiente comando:

```
python main.py
```

 o también 
 
```
python main.py -i RUTA_DE_LA_IMAGEN
```

## Bibliografía

- https://core.telegram.org/bots/api
- https://pypi.org/project/python-dotenv/
