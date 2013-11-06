#! /usr/bin/env python

# usage: 	./backup.py -s ./source/directory -d ./destination/directory [-i incremental] [-g gzip backup] [-v version number]
#			[-l list backups] [-u upload to storage]
# licence: 	https://github.com/kir-dev/scripts/blob/master/LICENSE
# author: 	Szabolcs Varadi - https://github.com/Kresshy - kresshy[at]gmail[dot]com


# version history:
# v0.1 - the script is able to create a full backup on a specified directory
# v0.2 - the script logs the created backups to the database
# v0.3 - the script stores metadata information about the backup in the backup directory
# v0.4 - the script is able to create incremental backup from a source directory


# planned features: 
# - do a full backup from a source directory to a destination directory 			[#]
# - use sqlite for tracing the backups made with the srcipt 						[#]
# - store backup meta information in json files										[#]
# - restore backup selected from the sqlite database if backup is exist 			[ ]
# - move backup to other directory and track it in the sqlite database 				[ ]
# - gzip the backup to the destination directory 									[ ]
# - create incremental backup of an already backupped directory (without gzip) 		[#]
# - create incremental backup of an already backupped directory (with gzip) 		[ ]
# - adding more types of compressing the backup, bzip, lzo etc... 					[ ]
# - edit the backup in the zip file, only possible with bzip (?)					[ ]
# - upload the backup to a storage via ftp or scp 									[ ]


import os, sys, shutil, argparse, json, sqlite3, datetime, hashlib

# scan the directory and it's subdirs for files to backup while keeping the tree structure
def backupDirectory(src_dirname, dst_dirname, src_length, incremental, metadata):
	
	# list the items in the directory
	for f in os.listdir(src_dirname):

		# if the item is a file then copy it to the backup directory
		if os.path.isfile(os.path.join(src_dirname, f)):

			# create the directory first
			mkdir(dst_dirname + src_dirname[src_length:])

			# destination path and md5 hash from the file
			destination = dst_dirname + os.path.join(src_dirname, f)[src_length:]
			hash_string = hashlib.md5(open(os.path.join(src_dirname, f)).read()).hexdigest()
			
			# store the hash and path of the backuped file for metadata
			if incremental:
				if hash_string not in metadata:
					# incremental backup, store if not in metadata
					metadata[hash_string] = destination
					# then copy the file to that directory
					shutil.copyfile(os.path.join(src_dirname, f), destination)
					print "incremental backup: " + destination
			else:
				# full backup, must store every hash and filename
				metadata[hash_string] = destination
				# then copy the file to that directory
				shutil.copyfile(os.path.join(src_dirname, f), destination)

		# if the item in the directory is another directory			
		elif os.path.isdir(os.path.join(src_dirname, f)):

			# then recursively scan that directory too
			backupDirectory(os.path.join(src_dirname, f), dst_dirname, src_length, incremental, metadata)


# creates a directory for the given path
def mkdir(path):

	# do magic dir creation
    if not os.path.exists(path):
    	if path != "":
        	os.makedirs(path)


# list the created backups from the database
def listBackups(cursor):

	# fetch all info from the backup table
	cursor.execute("SELECT * FROM backup")
	rows = cursor.fetchall()

	for row in rows:
		print row


# the main function of the script
def main(argv):
    
	# parsing the command line arguments
	parser = argparse.ArgumentParser(description = "This script creates a full (default) or incremental backup from a directory")
	
	# the required and optional arguments
	parser.add_argument("-s", "--src", help="source directory which the bacup created from", required = False)
	parser.add_argument("-d", "--dest", help="destination directory where the bacup copied to", required = False)
	parser.add_argument("-i", "--inc", action="store_true", help="creates an incremental backup from the source directory", required = False)
	#parser.add_argument("-f", "--full", action="store_true", help="creates a full backup from the source directory", required = False)
	parser.add_argument("-g", "--gzip", action="store_true", help="compress the backup with gzip", required = False)
	parser.add_argument("-u", "--upload", action="store_true", help="upload the backup to a storage", required = False)
	parser.add_argument("-v", "--version", action="store_true", help="print the script version", required = False)
	parser.add_argument("-l", "--list", action="store_true", help="list the backups created with the script", required = False)
	
	# parse the arguments
	args = parser.parse_args()

	# if no arguments given then print help
	if not len(sys.argv) > 1:
		parser.print_help()
		sys.exit()

	# print the version number
	if (args.version):
		print "\nScript version number: " + version_number + "\n"
		sys.exit()

	# connect to the backup database
	conn = sqlite3.connect("backups.db")
	cursor = conn.cursor()
	
	# create the table backup if not exists and save the changes
	cursor.execute("CREATE TABLE IF NOT EXISTS backup(id INTEGER PRIMARY KEY AUTOINCREMENT, src TEXT, dest TEXT, time TEXT)");
	conn.commit()
	
	# list the old backups if argument is true
	if (args.list):
		listBackups(cursor)
		sys.exit()

	# load the source and destination values from the arguments
	src = args.src
	dest = args.dest

	# open the metadata file to store backup information of the files but ensure that the file exists
	mkdir(dest)
	open(dest + "/metadata", "a").close()
	meta = open(dest + "/metadata", "r")

	# log the backup to the database
	cursor.execute("INSERT INTO backup VALUES(null, ?, ?, ?)", (src, dest, str(datetime.date.today())))

	length = len(src)
	#print "source: " + src + " destination: " + dest

	# create metadata dictionary from json file
	json_metadict = None
	try:
		json_metadict = json.load(meta)
	except:
		json_metadict = {}
	meta.close()

	meta = open(dest + "/metadata", "w")
	# start the backup part of the script
	if (args.inc):
		backupDirectory(src, dest, length, True, json_metadict)
	else:
		backupDirectory(src, dest, length, False, json_metadict)

	if (args.gzip):
		print "gzipping the backup"



	# dump the metadata dictionary into a json file
	meta.write(unicode(json.dumps(json_metadict, ensure_ascii = False, indent = 4)))
	meta.close()
	# close database cursor and connection
	conn.commit()
	conn.close()


# starting the main function of the script
if __name__ == "__main__":

	# ./dest & ./src
	dest = ""
	src = ""
	inc = False
	gzip = False
	vers = False
	version_number = "v0.4"
	length = 0

	# calling main(passing the arguments)
	main(sys.argv)