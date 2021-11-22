# README #

Aplicación web como demostrador desarrollada para el proyecto: "Conteo Preciso de Vehículos párrafo Situaciones de alta congestión en imágenes de videovigilancia de tráfico" realizado por el grupo de investigación GRAM ubicado en la Universidad de Alcalá en colaboración con la dirección general de tráfico (DGT).

Aplicación desarrollada en base a flask (python web application framework).

## Contenidos ##

* Aplicaciones
* Estructura directorios
* Dependencias
* Arranque de aplicaciones
* Modificación de las configuraciones

### Aplicaciones ##

El paquete comprimido se compone de dos aplicaciones diferenciadas en dos carpetas distintas, esto se hace para diferenciar dos equipos distintos para cada una.

La primera 'gram-counting' debe ser copiada al escritorio del usuario 'dgt' y es la encargada de realizar el procesado de las imagenes; la segunda se almacena en  el directorio 'dgt', ésta es la encargada de la aplicación web, debe ser copiada en '/home/dgt'.


### Estructura de directorios ###

##### Aplicación web: #####

	dgt/
	|-- webApp/
	|-- |-- developing_tmp/
	|-- |-- |-- cam2db.py
	|-- |-- |-- cameras.json
	|-- |-- |-- cameras_dgt.sql
	|-- |-- |-- makerdb.sh
	|-- |-- flask/
	|-- |-- logs/
	|-- |-- |-- dgt2db.log
	|-- |-- |-- webApp.log
	|-- |-- static/
	|-- |-- |-- css/
	|-- |-- |-- fonts/
	|-- |-- |-- images/
	|-- |-- |-- js/
	|-- |-- |-- tmp/
	|-- |-- templates/
	|-- |-- |-- demonstrator.html
	|-- |-- |-- index.html
	|-- |-- |-- layout.html
	|-- |-- config.py
	|-- |-- dgt2db.py
	|-- |-- gramWebApp.conf
	|-- |-- index.html
	|-- |-- runwebapp.sh
	|-- |-- webApp.py
	|-- README.md

##### Aplicación de procesado de imágenes: #####

	gram-counting/
	|-- models/
	|-- |-- rf_model_multi.pkl
	|-- others/
	|-- |-- db2dens_estimator.log
	|-- |-- tmp/
	|-- src/
	|--	|-- cythonf/
	|-- |-- db2dens_estimator.py
	|-- |-- dens_estimator.py
	|-- |-- gen_features.py
	|-- |-- setup.py
	|-- |-- spatialAverage.py
	|-- |-- testing.py
	|-- |-- utils.py
	|-- compile.sh
	|-- run.sh



### Dependencias ###

A continuación se detallan las dependencias necesarias para cada aplicación.

##### Aplicación web: #####

	sudo apt-get install python-pip python-flask python-urllib3 python-mysqldb

	sudo pip install flask-mysql

Además será necesario disponer de 'mysql' para almacenar las bases de datos.


##### Aplicación de procesado de imágenes: #####

	sudo apt-get install python-pip cython python-numpy python-h5py python-scipy python-ibus libibus-1.0-5 python-vigra python-joblib python-skimage python-opencv python-mysqldb

	sudo pip install scikit-learn


Es importante que el paquete 'scikit-learn' sea la versión 0.16.0 o superior.


Además en el directorio 'dgt/webApp/developing_tmp' dispone de un script en python, 'makerdb.py' que le ayudará a crear la base de datos con las tablas necesarias, sólo necesita disponer de un usuario con el nombre 'dgt' en mysql y que disponga de permisos para poder crear bases de datos, sino quiere darle esos permisos puede crear la base de datos 'dgt' desde phpmyadmin y el script generará solo las tablas asociadas.

Una vez creadas, puede importar la tabla 'cameras_dgt.sql' contenida en dicha carpeta.


### Arranque ###

##### Aplicación web: #####
	
Para arrancarla lo único que debemos hacer es acceder al directorio '/dgt/webApp/'

		cd ~/dgt/webApp

y a continuación ejecutamos el script que se encargará de arrancar todo lo necesario,

		sh runwebapp.sh

o

		chmod 755 runwebapp.sh && ./runwebapp.sh 


##### Aplicación de procesado de imágenes: #####

De la misma forma accedemos a su directorio,

		cd ~/Desktop/gram-counting

Únicamente en su instalación debemos ejecutar el script 'compile.sh', una vez ejecutado NO será necesario volverlo a correr.

		sh compile.sh

y siempre que queramos lanzar la aplicación de procesado (por primera vez, cortes de luz, étc) ejecutaramos el script 'run.sh'

		sh run.sh

o

		chmod 755 run.sh && ./run.sh



### Modificación de las configuraciones ###

Si por algún motivo se desean modificar las aplicaciones se debe tener en cuenta lo siguiente,


Aplicación web,

	Debe revisar el fichero 'config.py' y las primeras líneas de 'dgt2db.py'.
	Nótese que 'config.py' es el fichero de configuración asociado a la aplicación web, y 
	'dgt2db.py' es la aplicación encargada de obtener las imágenes, de las cámaras activas, 
	de la dgt y las inserta en la base de datos asociada.

## LICENSE
### GNU GPL v3
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
