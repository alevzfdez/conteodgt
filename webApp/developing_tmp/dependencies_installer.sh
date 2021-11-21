
#!/bin/bash


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
		##########					  Created on March 25, 2015					 ##########
		##########																 ##########
		##########				@author: Alejandro Véliz Fernández				 ##########
		##########																 ##########
		##########			script usage: ./dependencies_installer.sh			 ##########
		##########																 ##########
		###################################################################################
		###################################################################################

echo "Dependencies script installer\n"

echo 'You are going to install:\n\t python-pip, python-dev, build-essential, virtualenv \n\t flask, urllib3, MySQL-Python, flask-mysql, gevent, gunicorn\n'
read -p  'Are you sure? (yY/nN): ' REPLY
if [ $REPLY != 'y' ] && [ $REPLY != 'Y' ]
then
	echo "\nPlease answer 'y' or 'Y' to continue\n";
	exit 1;
fi
	sudo aptitude install python-pip python-dev build-essential -y
	sudo pip install virtualenv

	#echo '\nChanging directory to /home/dgt/dgt\n'
	#cd /home/alex/dgt
	echo '\nChanging directory to /home/alex/Documentos/Repositories/conteodgt\n'
	cd /home/alex/Documentos/Repositories/conteodgt
	#virtualenv flask
	#. flask/bin/activate
	echo '\nActivated virtual environment\n'
	sudo pip install flask urllib3 MySQL-Python flask-mysql gevent gunicorn

echo '\nAll packages were succesfully installed!\n'

# cd
# echo "export DBAPP_SETTINGS=/home/dgt/dgt/config/db_dgt.cfg" >> /home/dgt/.bashrc
