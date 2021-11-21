#!/usr/bin/python2.7
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
		##########					 Run full web application					 ##########
		##########																 ##########
		##########																 ##########
		##########		---------------------------------------------------		 ##########
		##########					  Created on March 27, 2015					 ##########
		##########																 ##########
		##########				@author: Alejandro Véliz Fernández				 ##########
		##########																 ##########
		###################################################################################
		###################################################################################

'''
Imported libraries
'''
from flask import Flask, url_for, session, flash, render_template, Response, request, redirect, abort, jsonify
import os, json, time, hashlib, datetime, urllib, hashlib
from flaskext.mysql import MySQL


''' **************************************************************************** '''
''' **************************************************************************** '''
''' CONFIGURATION VARIABLES!! '''

mysql = MySQL()
app = Flask(__name__)
'''
Check config.py
'''
app.config.from_object('config')
mysql.init_app(app)

db = mysql.connect()
cursor = db.cursor()
last_timestamp = 'None'
last_codEle = 'None'

IMG_PATH = 'static/tmp/'
SERVER_ADDR = 'http://infocar.dgt.es/etraffic/data/camaras/'


NOT_AVAILABLE_HASHES = ['647abde69ee89defc905a652d0f41c8e', '5a5adb115ef49a5de8ac25879bce985a', '528b9919bdd1ed352b5fa75cb8dbb98a', 
						'ac9f593f466d1433f2054c8bf809d17a', '4aebafb68d97c5bc3941d44cb8c8d979', 'd3ec318f5667ec64990e2112d027ecaf', 
						'c84db768a1145bed67db8dd60e8a3227', '68b31ebfbaff71429904d655c9df443e', '79d0afdce00d191deb1d9d55095c6b6d']

''' **************************************************************************** '''
''' **************************************************************************** '''

#######################   FUNCTS   #######################
def get_ProcessedImage(codEle):
	selImgProc = '''SELECT img_processed FROM processing_dgt WHERE codEle=%s AND processed=1 AND DATE(`timestamp`) = CURDATE()  ORDER BY timestamp DESC'''

	# save downloaded original image controlling posible exceptions 
	try:
		with db:
			cursor.execute (selImgProc, (last_codEle, ))										# get original image
			db.commit()
			Img_proc=cursor.fetchone()[0]
		LOCAL_PROC_FILE = IMG_PATH+last_codEle+'_proc.jpg'
		with open(LOCAL_PROC_FILE, 'wb+') as newFile:								# save image into '/static/images/tmp'
			newFile.write(Img_proc)
		return 'Saved'
	except:
		return 'None'

# chart imt event source
def update_Chart():
	global last_timestamp
	selImt = '''SELECT imt FROM processing_dgt WHERE codEle=%s AND processed = 1 AND DATE(`timestamp`) = CURDATE() ORDER BY timestamp DESC'''
	seltimestamp = '''SELECT timestamp FROM processing_dgt WHERE codEle=%s AND processed = 1 AND DATE(`timestamp`) = CURDATE() ORDER BY timestamp DESC'''
	
	while True:
		if last_codEle != 'None':
			with db:
				cursor.execute(selImt, (last_codEle,))											# get and parse imt values from selected camera
				db.commit() 
				imt = cursor.fetchone()
				cursor.execute(seltimestamp, (last_codEle,))									# get and parse timestamp values from selected camera
				db.commit()
				timestamp = cursor.fetchone()

				get_ProcessedImage(last_codEle)

				data = {"elements":[]}
				if timestamp[0] > last_timestamp:
					data["elements"].append({"imt": imt[0], "timestamp": str(timestamp[0]).replace('-', '/')})
					last_timestamp = timestamp[0]
					
					data_json = json.dumps(data)
					yield 'data: %s\n\n' % data_json
					print '\t\033[1;34m'+'New chart event income\033[0m'
			time.sleep(10)

# initialize daily chart values for selected camera
def init_Chart(request_codEle):
	global last_timestamp
	global last_codEle
	selImt = '''SELECT imt FROM processing_dgt WHERE codEle=%s AND processed = 1 AND DATE(`timestamp`) = CURDATE() ORDER BY timestamp ASC'''
	selId = '''SELECT id FROM cameras_dgt WHERE codEle=%s ORDER BY timestamp DESC'''
	seltimestamp = '''SELECT timestamp FROM processing_dgt WHERE codEle=%s AND processed = 1 AND DATE(`timestamp`) = CURDATE() ORDER BY timestamp ASC'''
	seltimestampGen = '''SELECT timestamp FROM processing_dgt WHERE codEle=%s AND DATE(`timestamp`) = CURDATE() ORDER BY timestamp ASC'''
	INSERT_VALS = '''INSERT INTO processing_dgt(id, codEle, hash, img_original, processed) VALUES (%s, %s, %s, %s, %s)'''
	with db:
		cursor.execute(selImt, (request_codEle,))												# get and parse imt values from selected camera
		db.commit() 
		imt = cursor.fetchall()
		cursor.execute(seltimestamp, (request_codEle,))											# get and parse timestamp values from selected camera
		db.commit()
		timestamp = cursor.fetchall()

		data = {"elements":[]}
		try:
			for i in range(len(imt)):
				data["elements"].append({"imt": imt[i][0], "timestamp": str(timestamp[i][0]).replace('-', '/')})
				last_timestamp = timestamp[i][0]
				last_codEle = request_codEle
		except:
			data["elements"].append({"imt":'', "timestamp": ''})
			
		if (data["elements"] == []):
			cursor.execute(seltimestampGen, (request_codEle,))												# get and parse imt values from selected camera
			db.commit() 
			timestampGen_ = cursor.fetchone()[0]
			f = '%Y-%m-%d %H:%M:%S'
			
			# get minutes difference between now and last updated timestamp from today
			if (datetime.datetime.now().minute-datetime.datetime.strptime(timestampGen_, f).minute) < 5:

				cursor.execute(selId, (request_codEle,))												# get and parse imt values from selected camera
				db.commit() 
				id_ = cursor.fetchone()[0]
				print id_

				try:
					print
					response = urllib.urlopen(SERVER_ADDR+str(request_codEle)+'.jpg').read()		# get image from dgt
				except:
					print 'Error while: getting from dgt from id: %s'%id_+'\t'+'|'+'\t'+'time: %s' %datetime.datetime.now()
				currentHash = hashlib.md5(response).hexdigest()										# get current image hash
				
				try:
					localFile = IMG_PATH+str(request_codEle)+'_ori.jpg'
					with open(localFile, 'wb+') as newFile:									# save image into '/static/images/tmp'
						newFile.write(response)
				except:
					print 'Error while: saving local image from id: %s'%id_+'\t'+'|'+'\t'+'time: %s' %datetime.datetime.now()

				for k in range(len(NOT_AVAILABLE_HASHES)):
					if currentHash == NOT_AVAILABLE_HASHES[k]:
						status = 'NOT AVAILABLE'
						break
					else:
						status = 'AVAILABLE'
					
				if status != 'NOT AVAILABLE':
					try:
						with db:
							currentFile = open(localFile, 'rb').read()
							cursor.execute(INSERT_VALS, (id_, request_codEle, currentHash, currentFile, 0))
					except:
						print 'Error while: loading into database values from id: %s'%id_+'\t'+'|'+'\t'+'time: %s' %datetime.datetime.now()

	'''
	if get_ProcessedImage(last_codEle) == None:
		data["elements"].append({"proc_img":"none"})
	else:
		data["elements"].append({"proc_img":"saved"})		
	
	print data
	'''	
	return data

# load road roptions on selector
def get_PK_Options(request_province, request_road):
	repeated = False
	get_Pk = '''SELECT pk FROM cameras_dgt WHERE province=%s AND road=%s ORDER BY timestamp DESC'''
	with db:
		cursor.execute(get_Pk, (request_province, request_road))
		db.commit
		pk_opts = sorted(cursor.fetchall())
	data = {"elements": []}
	for i in range(len(pk_opts)):
		if i == 0:
			data["elements"].append({"pk": pk_opts[i][0]})
		else:
			repeated = False
			for j in range(len(data["elements"])):
				if pk_opts[i][0] == data["elements"][j]["pk"]:
					repeated = True
			if repeated == False:
				data["elements"].append({"pk": pk_opts[i][0]})
	return data

# load road roptions on selector
def get_Road_Options(request_province):
	repeated = False
	get_Road = '''SELECT road FROM cameras_dgt WHERE province=%s ORDER BY timestamp DESC''' 
	with db:
		cursor.execute(get_Road, (request_province,))
		db.commit
		road_opts = sorted(cursor.fetchall())
	data = {"elements": []}
	for i in range(len(road_opts)):
		if i == 0:
			data["elements"].append({"road": road_opts[i][0]})
		else:
			repeated = False
			for j in range(len(data["elements"])):
				if road_opts[i][0] == data["elements"][j]["road"]:
					repeated = True
			if repeated == False:
				data["elements"].append({"road": road_opts[i][0]})
	return data

# load road roptions on selector
def get_Province_Options():
	repeated = False
	get_Province = '''SELECT province FROM cameras_dgt ORDER BY timestamp DESC''' 
	with db:
		cursor.execute(get_Province)
		db.commit
		province_opts = sorted(cursor.fetchall())
	data = {"elements": []}
	for i in range(len(province_opts)):
		if i == 0:
			data["elements"].append({"province": province_opts[i][0]})
		else:
			repeated = False
			for j in range(len(data["elements"])):
				if province_opts[i][0] == data["elements"][j]["province"]:
					repeated = True
			if repeated == False:
				data["elements"].append({"province": province_opts[i][0]})
	return data


# update cam status active / deactive
def deactivate_One_Cam(request_codEle):
	query_cam_deact = '''UPDATE cameras_dgt SET status=0 WHERE codEle=%s '''

	with db:
		cursor.execute(query_cam_deact, (request_codEle,))
		db.commit
	# remove temporary data controlling posible exceptions 
	try:
		os.remove(IMG_PATH+request_codEle+'_ori.jpg')
		os.remove(IMG_PATH+request_codEle+'_proc.jpg')
	except OSError:
		pass

# update cam status active / deactive
def update_Cam(request_opt,request_province, request_road, request_pk):
	query_all_act = '''UPDATE cameras_dgt SET status=1'''
	query_all_deact = '''UPDATE cameras_dgt SET status=0'''
	query_province_act = '''UPDATE cameras_dgt SET status=1 WHERE province=%s'''
	query_road_act = '''UPDATE cameras_dgt SET status=1 WHERE road=%s AND province=%s'''
	query_pk_act = '''UPDATE cameras_dgt SET status=1 WHERE pk=%s AND road=%s AND province=%s'''
	query_province_deact = '''UPDATE cameras_dgt SET status=0 WHERE province=%s'''
	query_road_deact = '''UPDATE cameras_dgt SET status=0 WHERE road=%s AND province=%s'''
	query_pk_deact = '''UPDATE cameras_dgt SET status=0 WHERE pk=%s AND road=%s AND province=%s'''

	with db:
		if request_pk == 'default':														# check if pk is selected
			if request_road == 'default':												# if it is not, check if road is selected
				if request_province == 'default':										# if all cameras are selected
					if request_opt == 'activate':										# is the option selected activate o deactivate?
						cursor.execute(query_all_act)
						db.commit
					else:
						cursor.execute(query_all_deact)
						db.commit
				else:
					if request_opt == 'activate':
						cursor.execute(query_province_act, (request_province,))
						db.commit
					else:
						cursor.execute(query_province_deact, (request_province,))
						db.commit
			else:
				if request_opt == 'activate':
					cursor.execute(query_road_act, (request_road, request_province))
					db.commit
				else:
					cursor.execute(query_road_deact, (request_road, request_province))
					db.commit
		else:
			if request_opt == 'activate':
				cursor.execute(query_pk_act, (request_pk, request_road, request_province))
				db.commit
			else:
				cursor.execute(query_pk_deact, (request_pk, request_road, request_province))
				db.commit


# update markers depending on selection
def mapCams():
	showActive_codEle = '''SELECT codEle FROM cameras_dgt WHERE status=1 ORDER BY timestamp DESC''' 
	showActive_lat = '''SELECT lat FROM cameras_dgt WHERE status=1 ORDER BY timestamp DESC''' 
	showActive_lng = '''SELECT lng FROM cameras_dgt WHERE status=1 ORDER BY timestamp DESC''' 
	with db:																			# get cameras data depending on request
		cursor.execute(showActive_codEle)
		db.commit()
		codEle = cursor.fetchall()
		cursor.execute(showActive_lat)
		db.commit()
		lat = cursor.fetchall()
		cursor.execute(showActive_lng)
		db.commit()
		lng = cursor.fetchall()

		data = {"elements":[]}
		try:
			for i in range(len(codEle)):
				data["elements"].append({"codEle": str(codEle[i][0]), "lat": float(lat[i][0]), "lng": float(lng[i][0])})
		except:
			data["elements"].append({"codEle": '', "lat": '', "lng": ''})
	return data


#######################   ROUTES   #######################

# new chart value event
@app.route('/updateChart')
def updateChart():
	return Response(update_Chart(), mimetype='text/event-stream')	

# load daily camera imt values on chart
@app.route('/initChart')
def initChart():
	request_codEle = request.args.get('codEle')
	print '\t\033[1;34m'+'CHART selector updated\033[0m'
	return jsonify(init_Chart(request_codEle))

# update pk options
@app.route('/updatePK')
def getPKOptions():
	request_province = request.args.get('province')
	request_road = request.args.get('road')
	print '\t\033[1;34m'+'PK selector updated\033[0m'
	return jsonify(get_PK_Options(request_province, request_road))

# update road options
@app.route('/updateRoad')
def getRoadOptions():
	request_province = request.args.get('province')
	print '\t\033[1;34m'+'ROAD selector updated\033[0m'
	return jsonify(get_Road_Options(request_province))

# update province options
@app.route('/updateProvince')
def getProvinceOptions():
	print '\t\033[1;34m'+'PROVINCE selector updated\033[0m'
	return jsonify(get_Province_Options())

# deactivate showed camera
@app.route('/deactivateOneCam')
def deactivateOneCam():
	request_codEle = request.args.get('codEle')
	deactivate_One_Cam(request_codEle)

	print ('\t\033[1;34m'+'ACTION'+'\t\t'+'CODELE'+'\n\t'+'-----------------------------------------------'+'\n'
			'\t'+'deactivate'+'\t'+request_codEle+'\033[0m')
	
	return render_template('demonstrator.html')

# update selected camera status
@app.route('/updateCam')
def updateCam():
	request_opt = request.args.get('option')
	request_province = request.args.get('province')
	request_road = request.args.get('road')
	request_pk = request.args.get('pk')
	update_Cam(request_opt, request_province, request_road, request_pk)

	print ('\t\033[1;34m'+'ACTION'+'\t\t'+'PROVINCE'+'\t'+'ROAD'+'\t'+'PK'+'\n\t'+'-----------------------------------------------'+'\n'
			'\t'+request_opt+'\t'+request_province+'\t\t'+request_road+'\t'+request_pk+'\t\033[0m')
	
	return render_template('demonstrator.html')

# update map markers
@app.route('/updateMaps')
def update_Maps():
	print '\t\033[1;34m'+'Map markers updated\033[0m'
	return jsonify(mapCams())

# main page, demonstrator, shows all data
@app.route('/demonstrator')
def demonstrator():
	return render_template('demonstrator.html')

# login route
@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != app.config['USERNAME']:
			error = 'Nombre de usuario incorrecto'
		elif hashlib.sha512(request.form['password']).hexdigest() != hashlib.sha512(app.config['PASSWORD']).hexdigest():
			error = 'Contraseña incorrecta'
		else:
			session['logged_in'] = True
			return redirect(url_for('demonstrator'))
	return render_template('index.html', error=error.decode('utf-8'))

# logout route return clear session var
@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	return render_template('index.html')

# index page loaded if route '/' is requested by user
@app.route('/')
def main():
	return render_template('index.html')
	

### MAIN ###
if __name__=='__main__':
 # running app
	print '\n\n\n' + '############################################'
	print ' App started at: %s' % datetime.datetime.now()
	print '############################################' + '\n\n\n'

	with app.test_request_context():
		# reload app after every code changes automatically
		# also enable debugger
		# make server externally visible
		# run application allowing server to listen all public IPs
		app.run(host = '0.0.0.0', port=5000)
	db.close()
