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
		##########					  Created on May X, 2015					 ##########
		##########																 ##########
		##########				@author: Alejandro Véliz Fernández				 ##########
		##########																 ##########
		###################################################################################
		###################################################################################


import sys, os, MySQLdb
import datetime
from dens_estimator import DEstimator


if __name__ == '__main__':

	db = MySQLdb.connect(host = 'localhost', user = 'dgt', passwd = 'tute.fod9', db = 'dgt')
	cursor=db.cursor()

	img_path = 'tmp/'

	# main vars
	printTable = True
	last_procTime = datetime.datetime.now()
	selActv = '''SELECT status FROM cameras_dgt WHERE id=%s'''
	selImg = '''SELECT img_original FROM processing_dgt WHERE id=%s AND processed=0 ORDER BY timestamp DESC'''
	selCodEle = '''SELECT codEle FROM processing_dgt WHERE id=%s AND processed=0 ORDER BY timestamp DESC'''
	selTimestamp = '''SELECT timestamp FROM processing_dgt WHERE id=%s AND processed=0 ORDER BY timestamp DESC'''
	updateCam = '''UPDATE processing_dgt SET imt=%s, img_processed=%s, processed=1 WHERE id=%s AND timestamp=%s'''
	

	print '\n\n\n' + '######################################' +'App started at: %s' % last_procTime + '######################################' + '\n\n\n'
	stm = DEstimator('models/rf_model_multi.pkl')

	while True:
		if printTable == True:
			print '\n'+'\033[1;34mNew images to process\033[0m'+'\n'
			print '\t'+'ID'+'\t'+'CODE'+'\t'+'ON/OFF'+'\t'+'IMT'+'\t'+'TIMESTAMP'+'\n'+'\t'+'--------------------------------------------'
		for code in range(1,1262):
			actv = '\033[1;31mOFF\033[0m'
			try:
				cursor.execute (selActv, (code,))												# get codEle
				db.commit()
				actv_=str(cursor.fetchone()[0])
				if actv_ == '1':
					printTable = True
					actv = '\033[1;32mON\033[0m'
					with db:
						cursor.execute (selCodEle, (code, ))										# get codEle
						db.commit()
						codEle=str(cursor.fetchone()[0])
						cursor.execute (selTimestamp, (code, ))										# get codEle
						db.commit()
						timestamp=str(cursor.fetchone()[0])
						cursor.execute (selImg, (code, ))											# get original image
						db.commit()
						Img_ori=cursor.fetchone()[0]

					local_orig_File = img_path+codEle+'_ori.jpg'
					local_proc_File = img_path+codEle+'_proc.jpg'
					newFile = open(local_orig_File, 'wb+')											# save image into '/static/images/tmp'
					newFile.write(Img_ori)
					newFile.close()

					count = stm.predict(local_orig_File, local_proc_File)
					count_ = '%.2f' % count

					with db:
						fileProc = open(local_proc_File, 'rb').read()
						cursor.execute(updateCam, (count_, fileProc, code, timestamp))

					os.remove(local_orig_File)
					os.remove(local_proc_File)
					last_procTime = datetime.datetime.now()

				else:
					codEle = '-'
					count_ = '-'
					timestamp = '-'

			except:
				# check if time difference between las processed image or started time is higher than 15 minutes
				now = datetime.datetime.now()
				diff = (now-last_procTime).seconds / 60
				if diff > 0:
					print ('\033[1;31mSomething is going wrong...'+'\n'+
						'Check yor dgt2db application\033[0m')				
					print '%d' %diff + ' minutes without processing images'
					print 'Last process: %s' %last_procTime
					print 'Current time: %s' %now
					printTable = False
				codEle = '+'
				count_ = '+'
				timestamp = '+'

			if printTable == True:
				print '\t'+str(code)+'\t'+'\033[1;34m'+str(codEle)+'\033[0m'+'\t'+actv+'\t'+'\033[0;37m'+str(count_)+'\033[0m'+'\t'+timestamp

