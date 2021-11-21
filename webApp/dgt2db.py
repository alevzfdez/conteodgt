#!/usr/bin/env python2.7
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
##########			Load new images from cameras_dgt table into		 	 ##########
##########				processing_dgt table on dgt database			 ##########
##########																 ##########
##########																 ##########
##########		---------------------------------------------------		 ##########
##########					  Created on March 31, 2015					 ##########
##########																 ##########
##########				@author: Alejandro Véliz Fernández				 ##########
##########																 ##########
###################################################################################
###################################################################################

'''
Imported libraries
'''
import sys, time, datetime, urllib, MySQLdb, hashlib


''' **************************************************************************** '''
''' **************************************************************************** '''
''' CONFIGURATION VARIABLES!! '''

'''
Set verbose to True to see table
'''
VERBOSE = True

'''
Check this paths and md5 hashes
'''
IMG_PATH = 'static/tmp/'
SERVER_ADDR = 'http://infocar.dgt.es/etraffic/data/camaras/'
NOT_AVAILABLE_HASHES = ['647abde69ee89defc905a652d0f41c8e', '5a5adb115ef49a5de8ac25879bce985a', '528b9919bdd1ed352b5fa75cb8dbb98a', 
						'ac9f593f466d1433f2054c8bf809d17a', '4aebafb68d97c5bc3941d44cb8c8d979', 'd3ec318f5667ec64990e2112d027ecaf', 
						'c84db768a1145bed67db8dd60e8a3227', '68b31ebfbaff71429904d655c9df443e', '79d0afdce00d191deb1d9d55095c6b6d']

TOOLBAR_WIDTH = 50
SHORT_SLEEP_TIME = 2
REFRESH_SLEEP_TIME = 5 * 60

'''
Check tables and columns
'''
SEL_ACTV = '''SELECT status FROM cameras_dgt ORDER BY timestamp ASC'''
SEL_ID = '''SELECT id FROM cameras_dgt ORDER BY timestamp ASC'''
SEL_CODELE = '''SELECT codEle FROM cameras_dgt WHERE id=%s ORDER BY timestamp DESC'''
SEL_HASH = '''SELECT hash FROM processing_dgt WHERE id=%s ORDER BY timestamp DESC'''
INSERT_VALS = '''INSERT INTO processing_dgt(id, codEle, hash, img_original, processed) VALUES (%s, %s, %s, %s, %s)'''

'''
Check database access
'''
db = MySQLdb.connect(host = 'localhost', user = 'dgt', passwd = 'tute.fod9', db = 'dgt')


''' **************************************************************************** '''
''' **************************************************************************** '''

''' SLEEP FUNCTION WITH TOOLBAR '''
def waitTimeToolbar(time_):
	# setup toolbar
	sys.stdout.write('\n'+'\033[0;37m   \t[%s]' % ('_' * TOOLBAR_WIDTH))
	sys.stdout.flush()
	sys.stdout.write('\b' * (TOOLBAR_WIDTH+3)) 									# return to start of line, after '['

	for i in xrange(TOOLBAR_WIDTH+1):
		sys.stdout.write('\b'*(TOOLBAR_WIDTH+42)+'%s' % (i*(100/TOOLBAR_WIDTH))+'%\t[')
		sys.stdout.flush()
		for j in xrange(i):
			sys.stdout.write('#')
			sys.stdout.flush()
		time.sleep(time_/TOOLBAR_WIDTH)
	print '\033[0m\n'



''' MAIN '''
if __name__ == '__main__':
	cursor=db.cursor()
 	
 # running app
	print ('\n\n\n' + '############################################'+'\n'+
		 ' App started at: %s' % datetime.datetime.now()+'\n'+
		 '############################################' + '\n\n\n')

	# needed vars
	wastedTime = 0
	counter = 0
	status = 'OLD'
	
	while True:
		if VERBOSE == True:
			print ('\n'+'\033[1;34mNew images received\033[0m'+'\n'+
				 	'\t'+'ID'+'\t'+'CODE'+'\t'+'ON/OFF'+'\t'+'STATUS'+'\n'+'\t'+'-------------------------------')

		try:
			cursor.execute (SEL_ACTV)															# get tuple of image status to check if it's activated
			db.commit()
			actv_ = cursor.fetchall()
		except:
			print 'Error while: getting from database status'+'\t'+'|'+'\t'+'time: %s' %datetime.datetime.now()	

		try:
			cursor.execute (SEL_ID)																# get tuple of image id from cameras_dgt table
			db.commit()
			id_ = cursor.fetchall()
		except:
			print 'Error while: getting from database ids'+'\t'+'|'+'\t'+'time: %s' %datetime.datetime.now()

		counter = 0																				# reset counter

		for code in range(len(id_)):															# get images from all registered cameras
			if counter > 200:
				if VERBOSE == True:
					print ('\t'+'-------------------------------'+'\n'+
						'\t'+'waiting 2 seconds after keeping updating images...\033[0m')		# wait 2 seconds until next request if there is a lot of images to download
					waitTimeToolbar(SHORT_SLEEP_TIME)
				else:
					time.sleep(SHORT_SLEEP_TIME)
				wastedTime += SHORT_SLEEP_TIME													# take short wasted time for refreshing sleep time
				counter = 0
			if str(actv_[code][0]) == '1':
				counter += 1
				on_off = 'ON'

				try:
					cursor.execute (SEL_CODELE, (id_[code][0],))								# get tuple of image id from cameras_dgt table
					db.commit()
					codEle = str(cursor.fetchone()[0])
				except:
					print 'Error while: getting from database codEle from %s'%id_[code][0]+'\t'+'|'+'\t'+'time: %s' %datetime.datetime.now()

				try:
					response = urllib.urlopen(SERVER_ADDR+str(codEle)+'.jpg').read()			# get image from dgt
				except:
					print 'Error while: getting from dgt image from id: %s'%id_[code][0]+'\t'+'|'+'\t'+'time: %s' %datetime.datetime.now()

				try:
					cursor.execute (SEL_HASH, (id_[code][0],))									# get image last hash from processing_dgt table
					db.commit()
					lastHash=cursor.fetchone()
				except:
					print 'Error while: getting from database lasthash from id: %s'%id_[code][0]+'\t'+'|'+'\t'+'time: %s' %datetime.datetime.now()
				currentHash = hashlib.md5(response).hexdigest()									# get current image hash

				Check = True

				if lastHash != None:  															# check if there is no previous values in database
					if currentHash == str(lastHash[0]):											# check f image is new
						Check = False

				if Check == True:																# if it is new upload data to database
					try:
						localFile = IMG_PATH+str(codEle)+'_ori.jpg'
						with open(localFile, 'wb+') as newFile:									# save image into '/static/images/tmp'
							newFile.write(response)
					except:
						print 'Error while: saving local image from id: %s'%id_[code][0]+'\t'+'|'+'\t'+'time: %s' %datetime.datetime.now()

					for k in range(len(NOT_AVAILABLE_HASHES)):
						if currentHash == NOT_AVAILABLE_HASHES[k]:
							status = 'NOT AVAILABLE'
							break
						
					if status != 'NOT AVAILABLE':
						status = 'NEW'

						try:
							with db:
								currentFile = open(localFile, 'rb').read()
								cursor.execute(INSERT_VALS, (id_[code][0], codEle, currentHash, currentFile, 0))
						except:
							print 'Error while: loading into database values from id: %s'%id_[code][0]+'\t'+'|'+'\t'+'time: %s' %datetime.datetime.now()
					
				else:
					status = 'OLD'

				if VERBOSE == True:
					print '\t'+str(id_[code][0])+'\t'+str(codEle)+'\t'+on_off+'\t'+status

					
			else:
				on_off = 'OFF'
				_id_ = '-'
				status = '-'
				if VERBOSE == True:
					print '\t'+str(id_[code][0])+'\t'+_id_+'\t'+on_off+'\t'+status

		if VERBOSE == True:
			print ('\t'+'-------------------------------'+'\n'+
		 		'\t'+'waiting 5 minutes after updating images...\033[0m')						# wait 5 minutes until next request (same time that dgt updating images time)
		
			waitTimeToolbar(REFRESH_SLEEP_TIME)
		else:
			time.sleep(REFRESH_SLEEP_TIME)
		wastedTime = 0
		counter = 0
