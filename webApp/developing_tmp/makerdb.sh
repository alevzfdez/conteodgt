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
		##########					  Created on March 18, 2015					 ##########
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
# cameras table name
TABLE_1="cameras_dgt"
# processing table name
TABLE_2="processing_dgt"
# cameras columns
COLS_1="id INT, status INT(1), province CHAR(30), road CHAR(30), pk CHAR(30), way CHAR(30), codEle INT, lat FLOAT(20, 18), lng FLOAT(20, 18), timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
# processing columns
COLS_2="id INT, codEle INT, hash CHAR(35), processed INT(1), imt INT, img_original BLOB, img_processed BLOB, timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP"

C1="CREATE DATABASE IF NOT EXISTS $DB;"
C2="USE $DB;"
C3="CREATE TABLE $TABLE_1 ($COLS_1);"
C4="CREATE TABLE $TABLE_2 ($COLS_2);"
C5="SHOW TABLES;"
C6="DESCRIBE $TABLE_1;"
C7="DESCRIBE $TABLE_2;"

SQL="${C1}${C2}${C3}${C4}${C5}${C6}${C7}"

if [ $# -ne $EXPECTED_ARGS ]
then
  echo "Usage: $0"
  exit $E_BADARGS
fi

$MYSQL -u root -p -e "$SQL"
