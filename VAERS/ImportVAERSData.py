#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  ImportVAERSData.py
#
#  Copyright 2021 Kaiyilen <Kaiyilen@Misao>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

#1. "Psycopg" is the most popular PostgreSQL adapter for the Python programming language.
#2. Since we're doing OS scripting/work/whatever, we'll use "os"....
import psycopg2
import os

#After imports and includes come variables
datafolder = "/tmp/VAERS/VAERSData/"

#Commence the jiggling.
#0. Connect to the DB
#1. Access the root folder. VAERSData
#2. Access the working folder
#3. Find the working year
#4. find the ####VAERSSYMPTOMS.csv file and append to the symptoms table, append working year to last column
#5. find the ####VAERSVAX.csv file and append to the vax table, append working year to last column
#6. find the ####VAERSData.csv file and append to the data table, append working year to last column

#Let's establish the connection
try:	
	dbhost = "localhost" 
	dbport = "5432" # default postgres port
	dbname = ""
	dbuser = ""
	dbpw = ""
	dbconn = psycopg2.connect(host=dbhost, dbname=dbname, user=dbuser, password=dbpw)
	dbcursor = dbconn.cursor()

	print ("Connection sccessful.")

except:
	print ("Connection failed.")

def appendomattic(year, wd):
	#For each item in the working directory(wd)
	#1. Ignore the first four characters in the name
	#2. Append to the appropriate table
	#3. append the year as a new column
	for e in os.listdir(wd):
		if e[4:] == "VAERSVAX.csv":
			#print("Importing Vax Data from " + wd + "/" + e + " For The Year: " + year)				
			dbquery = '''COPY vax(VAERS_ID,VAX_TYPE ,VAX_MANU, VAX_LOT, VAX_DOSE_SERIES, VAX_ROUTE, VAX_SITE, VAX_NAME) FROM '/''' + wd + "/" + e + '''' DELIMITER ','CSV HEADER;'''
			with open(wd + "/" + e) as f:
				next(f)
				dbcursor.execute(dbquery)	
				dbconn.commit()								

		if e[4:] == "VAERSSYMPTOMS.csv":
			#print("Importing Symptom Data from " + wd + "/" + e + " For The Year: " + year)				
			dbquery = '''COPY symptoms(VAERS_ID, SYMPTOM1, SYMPTOMVERSION1, SYMPTOM2, SYMPTOMVERSION2, SYMPTOM3, SYMPTOMVERSION3, SYMPTOM4, SYMPTOMVERSION4, SYMPTOM5, SYMPTOMVERSION5) FROM '/''' + wd + "/" + e + '''' DELIMITER ','CSV HEADER;'''
			with open(wd + "/" + e) as f:
				next(f)
				dbcursor.execute(dbquery)	
				dbconn.commit()					

		if e[4:] == "VAERSDATA.csv":
			#print("Importing VAERS Data from " + wd + "/" + e + " For The Year: " + year)	
			dbquery = '''COPY vaers(VAERS_ID, RECVDATE, STATED, AGE_YRS, CAGE_YR, CAGE_MO, SEX, RPT_DATE, SYMPTOM_TEXT, DIED, DATEDIED, L_THREAT, ER_VISIT, HOSPITAL, HOSPDAYS, X_STAY, DISABLED, RECOVD, VAX_DATE, ONSET_DATE, NUMDAYS, LAB_DATA, V_ADMINBY, V_FUNDBY, OTHER_MEDS, CUR_ILL, HISTORY, PRIOR_VAX, SPLTTYPE, FORM_VERS, TODAYS_DATE, BIRTH_DEFECT, OFC_VISIT, ER_ED_VISIT, ALLERGIES) FROM '/''' + wd + "/" + e + '''' DELIMITER ','CSV HEADER;'''
			with open(wd + "/" + e) as f:
				next(f)
				dbcursor.execute(dbquery)	
				dbconn.commit()								

	print ("VAERS data for " + year + " Has been added to the Project12 Database")

def main(args):
	#for each item in the sorted directory list for VAERSData/
	#"i" is the directory name
	for i in sorted(os.listdir(datafolder)):
		#let's extract the year from the directory name
		#first 4 characters are the year
		year = (i[0:4])

		#Let's build the working directory,
		#Should look something like VAERSData/2019VAERSData/
		wd = datafolder + i

		#Let's call a function to append each object in each folder
		appendomattic(year, wd)

	return 0

#wtf is this?
if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))

