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
		##########		  			script usage: ./install_conf.sh			 	 ##########
		##########																 ##########
		###################################################################################
		###################################################################################



read -p 'Nombre de base de datos: ' DB
read -p 'Ingrese un usuario exstente de la base de datos: ' DBUSER
read -p 'Enter password: ' DBPASS

# db user and pass
perl -p -i -e "s/dDDD/$DB/g" webApp/config.py
perl -p -i -e "s/uUUU/$DBUSER/g" webApp/config.py
perl -p -i -e "s/pPPP/$DBPASS/g" webApp/config.py
perl -p -i -e "s/dDDD/$DB/g" webApp/dgt2db.py
perl -p -i -e "s/uUUU/$DBUSER/g" webApp/dgt2db.py
perl -p -i -e "s/pPPP/$DBPASS/g" webApp/dgt2db.py

##
perl -p -i -e "s/dDDD/$DB/g" gram-counting/src/db2dens_estimator.py
perl -p -i -e "s/uUUU/$DBUSER/g" gram-counting/src/db2dens_estimator.py
perl -p -i -e "s/pPPP/$DBPASS/g" gram-counting/src/db2dens_estimator.py


echo 'Configuracion realizada!'