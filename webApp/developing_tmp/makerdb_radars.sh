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
		##########		  			 script usage: ./makerdb.sh			 		 ##########
		##########																 ##########
		###################################################################################
		###################################################################################

EXPECTED_ARGS=0
E_BADARGS=65
MYSQL=`which mysql`

# database name
DB="dgt"
# radars table name
TABLE_1="radares_dgt"
# cameras columns
COLS_1="id INT, status INT(1), province CHAR(30), road CHAR(30), pk CHAR(30), way CHAR(30), codEle INT, lat FLOAT(20, 18), lng FLOAT(20, 18), timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP"

C1="CREATE DATABASE IF NOT EXISTS $DB;"
C2="USE $DB;"
C3="CREATE TABLE $TABLE_1 ($COLS_1);"
C4="SHOW TABLES;"
C5="DESCRIBE $TABLE_1;"

SQL="${C1}${C2}${C3}${C4}${C5}"

if [ $# -ne $EXPECTED_ARGS ]
then
  echo "Usage: $0"
  exit $E_BADARGS
fi

$MYSQL -u root -p -e "$SQL"
