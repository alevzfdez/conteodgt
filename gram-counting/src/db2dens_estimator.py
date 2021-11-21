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
		##########			Load new images from cameras_dgt table into		 	 ##########
		##########				processing_dgt table on dgt database			 ##########
		##########																 ##########
		##########																 ##########
		##########		---------------------------------------------------		 ##########
		##########					  Created on Apr 28, 2015					 ##########
		##########																 ##########
		##########				@author: Alejandro Véliz Fernández				 ##########
		##########																 ##########
		###################################################################################
		###################################################################################

'''
Imported libraries
'''
import sys, os, MySQLdb
import datetime, time
from dens_estimator import DEstimator


''' **************************************************************************** '''
''' **************************************************************************** '''
''' CONFIGURATION VARIABLES!! '''

'''
Set verbose to True to see table
'''
VERBOSE = False

'''
Check this paths and model
'''
IMG_PATH = 'others/tmp/'
DENSTIMATOR_MODEL = 'models/rf_model_multi.pkl'

'''
Check tables and columns
'''
SEL_ACTV = '''SELECT status FROM cameras_dgt ORDER BY timestamp ASC'''
selImg = '''SELECT img_original FROM processing_dgt WHERE id=%s AND processed=0 ORDER BY timestamp DESC'''
selCodEle = '''SELECT codEle FROM processing_dgt WHERE id=%s AND processed=0 ORDER BY timestamp DESC'''
selTimestamp = '''SELECT timestamp FROM processing_dgt WHERE id=%s AND processed=0 ORDER BY timestamp DESC'''
updateCam = '''UPDATE processing_dgt SET imt=%s, img_processed=%s, processed=1 WHERE id=%s AND timestamp=%s'''

'''
Check database access
'''
db = MySQLdb.connect(host = 'localhost', user = 'dgt', passwd = 'tute.fod9', db = 'dgt')




''' **************************************************************************** '''
''' **************************************************************************** '''


''' MAIN '''
if __name__ == '__main__':

	# main vars
	printTable = True
	printError = True
	last_procTime = datetime.datetime.now()
	cursor = db.cursor()

# running app
	print '\n\n\n' + '############################################'
	print ' App started at: %s' % last_procTime
	print '############################################' + '\n\n\n'
	stm = DEstimator(DENSTIMATOR_MODEL)

	while True:
		if VERBOSE == True:
			print '\n'+'\033[1;34mNew images to process\033[0m'+'\n'
			print '\t'+'ID'+'\t'+'CODE'+'\t'+'ON/OFF'+'\t'+'IMT'+'\t'+'TIMESTAMP'+'\n'+'\t'+'--------------------------------------------'

		try:
			cursor.execute (SEL_ACTV)															# get tuple of image status to check if it's activated
			db.commit()
			actv_ = cursor.fetchall()
		except:
			if printError == True:
				print 'Error while: getting from database status'+'\t'+'|'+'\t'+'time: %s' %datetime.datetime.now()	
				printError = False

		for code in range(len(actv_)):
			if VERBOSE == True:
				actv = '\033[1;31mOFF\033[0m'

			if str(actv_[code][0]) == '1':
				if VERBOSE == True:
					actv = '\033[1;32mON\033[0m'
			
				# get data from database controlling posible exceptions 
				try:
					with db:
						cursor.execute (selCodEle, (code+1,))										# get tuple of image id from cameras_dgt table
						db.commit()
						codEle = str(cursor.fetchone()[0])
						cursor.execute (selTimestamp, (code+1, ))									# get codEle
						db.commit()
						timestamp=str(cursor.fetchone()[0])
						cursor.execute (selImg, (code+1, ))										# get original image
						db.commit()
						Img_ori=cursor.fetchone()[0]

					LOCAL_ORIG_FILE = IMG_PATH+codEle+'_ori.jpg'
					LOCAL_PROC_FILE = IMG_PATH+codEle+'_proc.jpg'


					# save downloaded original image controlling posible exceptions 
					try:
						with open(LOCAL_ORIG_FILE, 'wb+') as newFile:								# save image into '/static/images/tmp'
							newFile.write(Img_ori)
					except:
						if printError == True:
							print 'Error while: saving original image from id: %s'%str(code+1)+'\t'+'|'+'\t'+'time: %s' %datetime.datetime.now()
							printError = False

					# process imt controlling posible exceptions 
					try:
						count_ = '%.2f' % stm.predict(LOCAL_ORIG_FILE, LOCAL_PROC_FILE)
					except:
						if printError == True:
							print 'Error while: predicting imt from id: %s'%str(code+1)+'\t'+'|'+'\t'+'time: %s' %datetime.datetime.now()		
							printError = False					

					# read processed image controlling posible exceptions 
					try:
						fileProc = open(LOCAL_PROC_FILE, 'rb').read()
					except:
						if printError == True:
							print 'Error while: reading saved original image from id: %s'%str(code+1)+'\t'+'|'+'\t'+'time: %s' %datetime.datetime.now()	
							printError = False
							
					# update database controlling posible exceptions 
					try:
						cursor.execute(updateCam, (count_, fileProc, code+1, timestamp))
						printTable = True
						printError = True
					except:
						if printError == True:
							print 'Error while: updating values from id: %s'%str(code+1) +'\t'+'|'+'\t'+'time: %s' %datetime.datetime.now()	
							printError = False

					# remove temporary data controlling posible exceptions 
					try:
						os.remove(LOCAL_ORIG_FILE)
						os.remove(LOCAL_PROC_FILE)
					except OSError:
						pass
						
				except:					
					# check if time difference between las processed image or started time is equal to 15 minutes
					now = datetime.datetime.now()
					diff = (now-last_procTime).seconds / 60
					if diff >= 0:
						if printError == True:
							print ('\033[1;31mSomething is going wrong...'+'\n'+
								'Check yor dgt2db application\033[0m'+'\n'+			
								'%d' %diff + '\033[1;31m minutes without processing images'+'\n'+
								'Last process........ ' +'\t\t\t\t'+'|'+'\t'+'time: %s' %last_procTime+'\n'+
								'Current time........'+'\t\t\t\t'+'|'+'\t'+'time: %s'%now+'\033[0m')
							printError = False
					else:
						if VERBOSE == True:
							codEle = '+'
							count_ = '+'
							timestamp = '+'

						if printTable == True:
							print 'Waiting for new images to process...'+'\t\t'+'|'+'\t'+'time: %s' %datetime.datetime.now()
							printTable = False
					


			else:
				if VERBOSE == True:
					codEle = '-'
					count_ = '-'
					timestamp = '-'

			if VERBOSE == True:
					print '\t'+str(code+1)+'\t'+'\033[1;34m'+str(codEle)+'\033[0m'+'\t'+actv+'\t'+'\033[0;37m'+str(count_)+'\033[0m'+'\t'+timestamp

		time.sleep(30)