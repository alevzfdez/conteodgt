#!/bin/bash
# -* coding: utf-8 -*-

		###################################################################################
		###################################################################################
		##########																 ##########
		##########							 PROJECT:					 		 ##########
		##########				Conteo de vehiculos para situaciones de			 ##########
		##########			alta congestion en imagenes de video vigilancia.	 ##########
		##########																 ##########
		##########							DEPARTMENT:					 		 ##########
		##########				Teoría de la Señal y Comunicaciones				 ##########
		##########																 ##########
		##########																 ##########
		##########		---------------------------------------------------		 ##########
		##########					  Created on May 24, 2015					 ##########
		##########																 ##########
		##########				@author: Alejandro Véliz Fernández				 ##########
		##########																 ##########
		##########		  			 script usage: ./installer.sh			 	 ##########
		##########																 ##########
		###################################################################################
		###################################################################################
lang="en"
INSTALL_PATH=""
MYSQL=`which mysql`

# cameras table name
TABLE_1="cameras_dgt"
# processing table name
TABLE_2="processing_dgt"
# cameras columns
COLS_1="id INT, status INT(1), province CHAR(30), road CHAR(30), pk CHAR(30), way CHAR(30), codEle INT, lat FLOAT(20, 18), lng FLOAT(20, 18), timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
# processing columns
COLS_2="id INT, codEle INT, hash CHAR(35), processed INT(1), imt INT, img_original BLOB, img_processed BLOB, timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP"



read -p  "Select an installation languaje. (esES/enEN)[en by default]: " REPLY
if [ "$REPLY" == "es" ] || [ "$REPLY" == "ES" ]
then
	lang="es"
else
	lang="en"
fi



## English languaje chosen
if [ "$lang" == 'en' ]
then
	echo -e "\nWelcome to gram's web application installer!\n\n"

	echo -e "Before continue check you have mysql installed. [press enter to continue]\n"
	read -p ""

	read -p 'Write your installation path:' INSTALL_PATH
	if [ -z "$INSTALL_PATH" ]
	then
		echo -e "\nPlease write an installation path.\n";
		exit 1;
	fi

	# create install directory and copy files
	INSTALL_PATH_FULL="$INSTALL_PATH/gramWebApp"
	sudo mkdir $INSTALL_PATH_FULL
	sudo cp -r ../gramWebApp/*  $INSTALL_PATH_FULL

	# install dependencies
	echo -e "First of all the script is going to install needed dependencies.\n"

	echo -e 'You are going to install:\n\t python-pip, python-dev, build-essential, virtualenv \n\t flask, urllib3, MySQL-Python, flask-mysql, gevent, gunicorn\n'
	read -p  'Are you sure? (yY/nN): ' REPLY
	if [ "$REPLY" != 'y' ] && [ "$REPLY" != 'Y' ]
	then
		echo -e "\nPlease answer 'y' or 'Y' to continue\n";
		exit 1;
	fi
		sudo aptitude install python-pip python-dev build-essential -y
		sudo pip install virtualenv

		cd $INSTALL_PATH_FULL
		virtualenv flask
		. flask/bin/activate
		echo -e '\nActivated virtual environment\n'
		sudo pip install flask urllib3 MySQL-Python flask-mysql gevent gunicorn


	sudo cp $INSTALL_PATH_FULL/webApp/install/gramWebApp.conf /etc/init/
	sudo perl -p -i -e "s/xX/$INSTALL_PATH_FULL/g" webApp/runwebapp.sh
	sudo perl -p -i -e "s/xXcat /$INSTALL_PATH_FULL/g" /etc/init/gramWebApp.conf

	# config web page user
	read -p 'Web application user name: ' WUSER
	read -p 'Password: ' DWPASS
	sudo perl -p -i -e "s/wUUU/$WUSER/g" webApp/config.py
	sudo perl -p -i -e "s/wPPP/$DWPASS/g" webApp/config.py


	# make db tables (if not, make manueally)
	echo -e 'Now we are going to create 2 mysql database tables, if database does not exist it will be created.\n'
	echo -e 'You can cancel this operation and make by hand following README steps.'
	read -p  'Are you sure to continue? (yY/nN): ' REPLY
	if [ "$REPLY" != 'y' ] && [ "$REPLY" != 'Y' ]
	then
		echo -e "\nDon't forget to make proper database tables!\n";
		exit 1;
	fi

	read -p 'Database name: ' DB
	read -p 'Existing mysql user: ' DBUSER
	read -p 'Enter password: ' DBPASS

	# config path db user and pass
	sudo perl -p -i -e "s/dDDD/$DB/g" webApp/config.py
	sudo perl -p -i -e "s/uUUU/$DBUSER/g" webApp/config.py
	sudo perl -p -i -e "s/pPPP/$DBPASS/g" webApp/config.py
	sudo perl -p -i -e "s/dDDD/$DB/g" webApp/dgt2db.py
	sudo perl -p -i -e "s/uUUU/$DBUSER/g" webApp/dgt2db.py
	sudo perl -p -i -e "s/pPPP/$DBPASS/g" webApp/dgt2db.py
	sudo perl -p -i -e "s/dDDD/$DB/g" gram-counting/src/db2dens_estimator.py
	sudo perl -p -i -e "s/uUUU/$DBUSER/g" gram-counting/src/db2dens_estimator.py
	sudo perl -p -i -e "s/pPPP/$DBPASS/g" gram-counting/src/db2dens_estimator.py

	C1="CREATE DATABASE IF NOT EXISTS $DB;"
	C2="USE $DB;"
	C3="CREATE TABLE $TABLE_1 ($COLS_1);"
	C4="CREATE TABLE $TABLE_2 ($COLS_2);"
	C5="SHOW TABLES;"

	SQL="${C1}${C2}${C3}${C4}${C5}"

	$MYSQL -u $DBUSER -p$DBPASS -e "$SQL"
	mysql -u $DBUSER -p$DBPASS -D $DB < webApp/install/cameras_dgt.sql
	sudo rm -rf webApp/install/*

	echo -e '\nThanks for installing!\n'
	exit 0;
fi 

## Spanish languaje chosen
	echo -e "\nBienvenido al instalador!\n\n"

	echo -e "Antes de continuar comprueba que tengas instalado mysql. [presiona enter para continuar]\n"
	read -p ""

	read -p  'Escribe una ruta de instalacion:' INSTALL_PATH
	if [ -z $INSTALL_PATH]
	then
		echo -e "\nPor favor, elija una ruta de instalacion.\n";
		exit 1;
	fi


	# create install directory and copy files
	INSTALL_PATH_FULL="$INSTALL_PATH/gramWebApp"
	sudo mkdir $INSTALL_PATH_FULL
	sudo cp -r ../gramWebApp/*  $INSTALL_PATH_FULL

	# install dependencies
	echo -e "Antes de nada vamos a installar las dependencias necesarias.\n"

	echo -e 'Los siguientes paquetes van a ser instalados:\n\t python-pip, python-dev, build-essential, virtualenv \n\t flask, urllib3, MySQL-Python, flask-mysql, gevent, gunicorn\n'
	read -p  'Estas seguro? (sS/nN): ' REPLY
	if [ "$REPLY" != 's' ] && [ "$REPLY" != 'S' ] && [ "$REPLY" != 'y' ] && [ "$REPLY" != 'Y' ]
	then
		echo -e "\nPor favor, conteste 's' o 'S' para continuar\n";
		exit 1;
	fi
		sudo aptitude install python-pip python-dev build-essential -y
		sudo pip install virtualenv

		cd $INSTALL_PATH_FULL
		virtualenv flask
		. flask/bin/activate
		echo -e '\nEntorno virtual activado\n'
		sudo pip install flask urllib3 MySQL-Python flask-mysql gevent gunicorn

	sudo cp $INSTALL_PATH_FULL/webApp/install/gramWebApp.conf /etc/init/
	sudo perl -p -i -e "s/xX/$INSTALL_PATH_FULL/g" webApp/runwebapp.sh
	sudo perl -p -i -e "s/xXcat /$INSTALL_PATH_FULL/g" /etc/init/gramWebApp.conf

	# config web page user
	read -p 'Nombre de usuario para acceso a la aplicacion web: ' WUSER
	read -p 'Contraseña del usuario: ' WPASS
	sudo perl -p -i -e "s/wUUU/$WUSER/g" webApp/config.py
	sudo perl -p -i -e "s/wPPP/$WPASS/g" webApp/config.py


	# make db tables (if not, make manueally)
	echo -e 'Ahora vamos a crear 2 tablas en la base de datos mysql.\n'
	echo -e 'Si usted no quiere realizar este paso en la instalacion, puede hacerlo a mano siguiendo los pasos descritos en el fichero README.\n'
	read -p 'Desea continuar? (sS/nN): ' REPLY
	if [ "$REPLY" != 's' ] && [ "$REPLY" != 'S' ] && [ "$REPLY" != 'y' ] && [ "$REPLY" != 'Y' ]
	then
		echo -e "\nNo olvide mirar el fichero README!\n";
		exit 1;
	fi

	read -p 'Nombre de base de datos: ' DB
	read -p 'Ingrese un usuario exstente de la base de datos: ' DBUSER
	read -p 'Enter password: ' DBPASS

	# config path db user and passen la
	perl -p -i -e "s/dDDD/$DB/g" webApp/config.py
	perl -p -i -e "s/uUUU/$DBUSER/g" webApp/config.py
	perl -p -i -e "s/pPPP/$DBPASS/g" webApp/config.py
	perl -p -i -e "s/dDDD/$DB/g" webApp/dgt2db.py
	perl -p -i -e "s/uUUU/$DBUSER/g" webApp/dgt2db.py
	perl -p -i -e "s/pPPP/$DBPASS/g" webApp/dgt2db.py
	perl -p -i -e "s/dDDD/$DB/g" gram-counting/src/db2dens_estimator.py
	perl -p -i -e "s/uUUU/$DBUSER/g" gram-counting/src/db2dens_estimator.py
	perl -p -i -e "s/pPPP/$DBPASS/g" gram-counting/src/db2dens_estimator.py

	C1="CREATE DATABASE IF NOT EXISTS $DB;"
	C2="USE $DB;"
	C3="CREATE TABLE $TABLE_1 ($COLS_1);"
	C4="CREATE TABLE $TABLE_2 ($COLS_2);"
	C5="SHOW TABLES;"

	SQL="${C1}${C2}${C3}${C4}${C5}"


	cp webApp/install/cameras_dgt.sql .

	$MYSQL -u $DBUSER -p$DBPASS -e "$SQL"
	mysql -u $DBUSER -p$DBPASS -D $DB < cameras_dgt.sql
	rm -rf cameras_dgt.sql

	echo -e 'Gracias por seguir este instalador!'