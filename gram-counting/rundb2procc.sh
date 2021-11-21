#! /bin/bash
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
		##########							DESCRIPTION					 		 ##########
		##########					 Run full web application					 ##########
		##########																 ##########
		##########																 ##########
		##########		---------------------------------------------------		 ##########
		##########					  Created on Apr 28, 2015					 ##########
		##########																 ##########
		##########				@author: Alejandro Véliz Fernández				 ##########
		##########																 ##########
		###################################################################################
		###################################################################################


PATHTO='/home/alex/Documentos/Repositories/conteodgt/gram-counting/'

cd $PATHTO

echo 'Starting db2dens_estimator......'
./src/db2dens_estimator.py >> others/logs/db2dens_estimator.log &
