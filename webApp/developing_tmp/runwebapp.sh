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
		##########					  Created on Apr X, 2015					 ##########
		##########																 ##########
		##########				@author: Alejandro Véliz Fernández				 ##########
		##########																 ##########
		###################################################################################
		###################################################################################


cd xX
. flask/bin/activate

echo 'Starting dgt2db......'
pkill dgt2db
./dgt2db.py >> logs/dgt2db.log &

echo 'Starting web application......'
pkill gunicorn
gunicorn -k gevent -w 4 -b '0.0.0.0:5000'  webApp:app  >> logs/webApp.log 2>&1


echo 'Application has been closed!'
rm -rf *.pyc
rm -rf static/tmp/*
