#! /usr/bin/env python

# usage: 	./backup.py -s ./source/directory -d ./destination/directory [-i incremental] [-g gzip backup] [-v version number]
# licence: 	https://github.com/kir-dev/scripts/blob/master/LICENSE
# author: 	Szabolcs Varadi - https://github.com/Kresshy - kresshy[at]gmail[dot]com

# version history:
# v0.1 - the script is able to do a full backup on a specified directory

# planned features: 
# - do a full backup from a target directory to a destination directory 			[#]
# - use sqlite for tracing the backups made with the srcipt 						[ ]
# - restore backup selected from the sqlite database if backup is exist 			[ ]
# - move backup to other directory and track it in the sqlite database 				[ ]
# - gzip the backup to the destination directory 									[ ]
# - create incremental backup of an already backupped directory (without gzip) 		[ ]
# - create incremental backup of an already backupped directory (with gzip) 		[ ]
# - adding more types of compressing the backup, bzip, lzo etc... 					[ ]
# - edit the backup in the zip file, only possible with bzip (?)					[ ]
# - upload the backup to a storage via ftp or scp 									[ ]


import os, sys, shutil, argparse

# scan the directory and it's subdirs for files to backup while keeping the tree structure
def backupDirectory(src_dirname, dst_dirname, src_length):
	
	# list the items in the directory
	for f in os.listdir(src_dirname):

		# if the item is a file then copy it to the backup directory
		if os.path.isfile(os.path.join(src_dirname, f)):

			# create the directory first
			mkdir(dst_dirname + src_dirname[src_length:])

			# then copy the file to that directory
			# print os.path.join(src_dirname, f), dst_dirname + (os.path.join(src_dirname, f)[src_length:])
			shutil.copyfile(os.path.join(src_dirname, f), dst_dirname + os.path.join(src_dirname, f)[src_length:])

		# if the item in the directory is another directory			
		elif os.path.isdir(os.path.join(src_dirname, f)):

			# then recursively scan that directory too
			backupDirectory(os.path.join(src_dirname, f), dst_dirname, src_length)


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
	parser.add_argument("-s", "--src", help="source directory which the bacup created from", required = True)
	parser.add_argument("-d", "--dest", help="destination directory where the bacup copied to", required = True)
	parser.add_argument("-i", "--inc", action="store_true", help="creates an incremental backup from the source directory", required = False)
	#parser.add_argument("-f", "--full", action="store_true", help="creates a full backup from the source directory", required = False)
	parser.add_argument("-g", "--gzip", action="store_true", help="compress the backup with gzip", required = False)
	parser.add_argument("-v", "--version", action="store_true", help="print the script version", required = False)

	args = parser.parse_args()

	# print the version number
	if (args.version):
		print "\nScript version number: " + str(version_number) + "\n"
		sys.exit()

	src = args.src
	dest = args.dest
	inc = args.inc
	#full = args.full
	gzip = args.gzip

	length = len(src)
	print "source: " + src + " destination: " + dest

	if (inc):
		print "incremental backup"
	else:
		backupDirectory(src, dest, length)

# starting the main function of the script
if __name__ == "__main__":

	# ./dest & ./src
	dest = ""
	src = ""
	inc = False
	#full = False
	gzip = False
	vers = False
	version_number = 0.1
	length = 0

	# calling main(passing the arguments)
	main(sys.argv[1:])