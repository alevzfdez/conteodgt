#!/usr/bin/python
# -*- coding: utf-8 -*-


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
		##########			Load data from all dgt cameras working from dgt		 ##########
		##########				into cameras_dgt table on dgt database			 ##########
		##########																 ##########
		##########																 ##########
		##########		---------------------------------------------------		 ##########
		##########					  Created on Apr X, 2015					 ##########
		##########																 ##########
		##########				@author: Alejandro Véliz Fernández				 ##########
		##########																 ##########
		##########		  		 	script usage: ./cam2db.py 					 ##########
		##########																 ##########
		###################################################################################
		###################################################################################


import sys, MySQLdb, json, urllib, time

if __name__ == '__main__':
	db = MySQLdb.connect(host = 'localhost', user = 'dgt', passwd = 'tute.fod9', db = 'dgt')
	cursor = db.cursor()

	# variables
	with open('radares.json') as cameras:    
		responseCameras = json.load(cameras)
	dbquery_1 = ('''INSERT INTO radares_dgt(id, codEle, status, province, road , pk, way, lat, lng) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)''')
	var_addcomp = False
	totalCamsAdded = 0
	counter = 1

	print '\t'+'ID'+'\t\t'+'CAMERA'+'\t\t'+'WAY'+'\t\t'+'PK'+'\n'+'\t'+'-------------------------------------'
	for i in responseCameras:
		urlProvince = 'https://maps.googleapis.com/maps/api/geocode/json?latlng='+str(i['lat'])+','+str(i['lng'])+'&sensor=false'
		json_obj = json.load(urllib.urlopen(urlProvince))
		for j in json_obj['results']:
			for k in j['address_components']:
				if k['types'][0] == 'administrative_area_level_2':
					if 'sentido' in i:
						if i['sentido'] == 'CRE':
							way = 'Upwards'
							space = '\t\t'
						else:
							way = 'Downwards'
							space = '\t'
					else:
						way = 'Both ways'
						space = '\t'
					dbquery_2 = (totalCamsAdded, i['codEle'], i['estado'], k['long_name'], i['carretera'], i['PK'], way, i['lat'], i['lng'])
					with db:
						cursor.execute(dbquery_1, dbquery_2)
						counter+=1
						totalCamsAdded+=1
					print '\t'+str(totalCamsAdded)+'\t\t'+str(i['carretera'])+'\t\t'+way+space+str(i['PK'])
					var_addcomp = True
					break
			if var_addcomp == True:
				break
		if counter>300:
			print '\n'+'Waiting 5s to avoid issues'
			# setup toolbar
			toolbar_width = 50
			sys.stdout.write("\033[0;37m   \t[%s]" % ("-" * toolbar_width))
			sys.stdout.flush()
			sys.stdout.write("\b" * (toolbar_width+3)) 								# return to start of line, after '['

			for i in xrange(toolbar_width+1):
				sys.stdout.write('\b'*(toolbar_width+42)+"%s" % (i*2)+'%\t[')
				sys.stdout.flush()
				for j in xrange(i):
					sys.stdout.write("#")
					sys.stdout.flush()
				time.sleep(0.1)	
			counter = 1											 					# wait 5 minutes until next request (same time that dgt waste updating images
			print "\033[0m\n"+'\n'
	print '\t'+'-------------------------------------'+'\n'+'\t'+str(totalCamsAdded)+' cameras added to DB'+'\n'
	db.close()
