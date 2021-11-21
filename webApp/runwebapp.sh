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
		##########					  Created on Apr 29, 2015					 ##########
		##########																 ##########
		##########				@author: Alejandro Véliz Fernández				 ##########
		##########																 ##########
		###################################################################################
		###################################################################################

PATHTO='/home/alex/Documentos/Repositories/conteodgt/webApp/'

cd $PATHTO
. flask/bin/activate

echo 'Starting gramWebApp......'
./dgt2db.py >> logs/dgt2db.log &
gunicorn -k gevent -w 4 -b '0.0.0.0:5000'  webApp:app  >> logs/webApp.log

cd ../gram-counting
./src/db2dens_estimator.py >> others/logs/db2dens_estimator.log &
