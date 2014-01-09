#! /usr/bin/env python

# usage: 	./backup.py -s ./source/directory -d ./destination/directory [-v version] [-f ftp upload] [-n name] 
# 			cancelled features: [-i incremental] [-g gzip backup] [-l list backups] 
# licence: 	https://github.com/kir-dev/scripts/blob/master/LICENSE
# author: 	Szabolcs Varadi - https://github.com/Kresshy - kresshy[at]gmail[dot]com

# version history:
# v0.1 		- create a full backup on a specified directory
# v0.2 		- logs the created backups to the database
# v0.3 		- store metadata information about the backup in the backup directory
# v0.4 		- create incremental backup from a source directory
# v0.5 		- create tar.gz file from backup 
# v0.5.1 	- there are too many unnecessary features the followings will be cancelled: 2, 3, 4, 6, 7, 8, 9, 10

# planned features: 
# 1.	- do a full backup from a source directory to a destination directory 			[#]
# 2.	- use sqlite for tracing the backups made with the srcipt 						[#]
# 3.	- store backup meta information in json files									[#]
# 4.	- restore backup selected from the sqlite database if backup is exist 			[ ]
# 5.	- move backup to other directory and track it in the sqlite database 			[ ]
# 6.	- gzip the backup to the destination directory 									[#]
# 7.	- create incremental backup of an already backupped directory (without gzip) 	[#]
# 8.	- create incremental backup of an already backupped directory (with gzip) 		[ ]
# 9.	- adding more types of compressing the backup, bzip, lzo etc... 				[ ]
# 10.	- edit the backup in the zip file, only possible with bzip (?)					[ ]
# 11.	- upload the backup to a storage via ftp or scp 								[ ]
# 12. 	- email from any backup created with the script to specified members			[ ]


import os, sys, shutil, argparse, json, sqlite3, datetime, hashlib, gzip, tarfile

# scan the directory and it's subdirs for files to backup while keeping the tree structure
def backupDirectory(src_dirname, dst_dirname, src_length, metadata):
	
	# list the items in the directory
	for f in os.listdir(src_dirname):

		# if the item is a file then copy it to the backup directory
		if os.path.isfile(os.path.join(src_dirname, f)):

			# keep the directory structure
			# mkdir(dst_dirname + src_dirname[src_length:])

			# destination path and md5 hash from the file
			# destination = dst_dirname + os.path.join(src_dirname, f)[src_length:]
			hash_string = hashlib.md5(open(os.path.join(src_dirname, f)).read()).hexdigest()
			# tarfile.add(os.path.join(src_dirname, f))
			
			# store the hash and path of the backuped file for metadata	
			# always do a full backup, must store every hash and filename
			fname = os.path.join(src_dirname, f)[2:]
			#print fname

			metadata[hash_string] = fname

			# then copy the file to that directory
			# shutil.copyfile(os.path.join(src_dirname, f), destination)

		# if the item in the directory is another directory			
		elif os.path.isdir(os.path.join(src_dirname, f)):

			# then recursively scan that directory too
			backupDirectory(os.path.join(src_dirname, f), dst_dirname, src_length, metadata)


# creates a directory for the given path
def mkdir(path):

	# do magic dir creation
    if not os.path.exists(path):
    	if path != "":
        	os.makedirs(path)

# the main function of the script
def main(argv):
    
	# parsing the command line arguments
	parser = argparse.ArgumentParser(description = "This script creates a full (default) or incremental backup from a directory")
	
	# the required and optional arguments
	parser.add_argument("-s", "--src", help="source directory which the bacup created from", required = False)
	parser.add_argument("-d", "--dest", help="destination directory where the bacup copied to", required = False)
	parser.add_argument("-n", "--name", action="store_true", help="name of the backup", required = False)
	#parser.add_argument("-i", "--inc", action="store_true", help="creates an incremental backup from the source directory", required = False)
	parser.add_argument("-f", "--ftp", action="store_true", help="upload the backup to ftp storage", required = False)
	parser.add_argument("-v", "--version", action="store_true", help="print the script version", required = False)
	#parser.add_argument("-l", "--list", action="store_true", help="list the backups created with the script", required = False)
	
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

	# load the source and destination values from the arguments
	src = args.src
	dest = args.dest
	name = args.name

	# validating backup name input
	if not args.name:
		name = "backup"

	# open the metadata file to store backup information of the files
	# ensure that the metadata file exists
	# mkdir(dest)
	open(src + "/metadata", "a").close()

	# open the metadata file for read the data
	meta = open(src + "/metadata", "r")

	# create a dictionary from the metadata json file
	json_metadata = None

	try:
		json_metadata = json.load(meta)
	except:
		json_metadata = {}

	# close the metadata file after loading the data
	meta.close()

	# open the metadata as writable for writing new hashes
	meta = open(src + "/metadata", "w")

	# create compressed file
	backup_tarfile = name + "-" + str(datetime.date.today()) + ".tar.gz" 
	tar = tarfile.open(backup_tarfile, "w:gz")

	# we need this for path magic :)
	length = len(src)

	backupDirectory(src, dest, length, json_metadata)

	# dump the metadata into a json file and close
	meta.write(unicode(json.dumps(json_metadata, ensure_ascii = False, indent = 4)))
	meta.close()
	
	# compress the source directory
	tar.add(src[2:])

	# check the created tar file
	if tarfile.is_tarfile(name + "-" + str(datetime.date.today()) + ".tar.gz"):
		print "valid file"

	tar.close()

	# ftp upload process


# starting the main function of the script
if __name__ == "__main__":

	# version number
	version_number = "v0.5.1"

	# calling main(passing the arguments)
	main(sys.argv)