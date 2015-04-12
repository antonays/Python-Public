#my first primitive folder backup utility,
#written and compiled on windows, python 2.7
#runs from windows powershell, will back up basically any folder (or folder tree) to any destination
#for my set up: rootOfEvil is the user folder, i was concerned with backing up music,pictures, documents folders from that folder
#wil prompt the user for the directory to which to backup, create a folder BACKUP in that directory and create a folder
# with a datestamp for any directory that is copied

#also presents a progress line when copying files

import os
from datetime import datetime
from os.path import join, splitext, split, exists
from shutil import copyfile
import win32api

drives = win32api.GetLogicalDriveStrings()
def main():
	flag=0
	control=""
	print "Enter User Name (As Defined In Windows):"
	user = raw_input(">>")
	rootOfEvil="c:\users\\"+user+"\\"
	print "Enter Destination Drive,\nAvailable Drives: " + str(getDrives())
	while flag!=1:
		drive=raw_input("Drive>>")
		if (len(drive)==1):
			if (drive in getDrives()) or (drive.upper() in getDrives()):
				dest = drive + ":\BACKUP\\"
				flag=1;
		else:
			print "Enter only drive letter, no : or \\"
			flag=0
	if not exists(dest):
		try:
			os.mkdir(dest)
		except:
			print "main folder creation error - maybe drive does not exist"
			exit()
			
	while control!="exit":
		print "What to Back up?\n1-Music\n2-Pictures\n3-Documents\n4-ALL\n5-Exit"
		myInput=raw_input(">>")
		if (myInput=="1"):
			keyWord="music"
			go(rootOfEvil+keyWord,dest,keyWord)
		elif (myInput=="2"):
			keyWord="pictures"
			go(rootOfEvil+keyWord,dest,keyWord)
		elif (myInput=="3"):
			keyWord="documents"
			go(rootOfEvil+keyWord,dest,keyWord)
		elif (myInput=="4"):
			go(rootOfEvil+"music",dest,"music")
			go(rootOfEvil+"pictures",dest,"pictures")
			go(rootOfEvil+"documents",dest,"documents")
		elif (myInput=="5"):
			control="exit"

def getDrives():
	drives=[]
	for drive in win32api.GetLogicalDriveStrings().split("\x00"):
		if drive!="":
			drives.append(drive[0])
	return drives
			
def go(src,destinationRoot,what):
	count=0
	total=0
	print src
	dest=destinationRoot+what.upper()+"_BACKUP"+datetime.now().strftime("%Y-%m-%d")+"\\"
	for path, dirname, fnames in os.walk(src):
		total += len(fnames)
	print "Total: %d "%total+what.title()+" Files"+"\n--------------------------------"
	count = copy_directory(src,dest,total)
	print "--------------------------------\n"+"Done "+ what.upper()+", copied %d out of %d"%(count,total)+"\n--------------------------------"
	
def copy_directory(source, target,total):
	count=0
	skipped=0
	error=0
	if not os.path.exists(target):
		os.mkdir(target)
	for root, dirs, files in os.walk(source):
		for file in files:
			from_ = join(root, file)
			to_ = from_.replace(source, target, 1)
			to_directory = split(to_)[0]
			if not exists(to_directory):
				os.makedirs(to_directory)
			if not exists(to_):
				try:
					copyfile(from_, to_)
					count+=1
					printIteration(count,total)
				except Exception as e:
					print "error" + str(e)
					print "\nError - Probably encoding issue, Exception:" + str(e)
					error+=1
					count+=1
					printIteration(count,total)
			else:
				skipped+=1
				count+=1
				printIteration(count,total)
			
	sys.stdout.write("\n")
	print "Copied: %d\nSkipped: %d\nErrors:%d\nOut Of Total %d"%(count,skipped,error,total)
	return count

def printIteration(count,total):
	sys.stdout.write("\r%d Out of: %d"%(count,total))
	sys.stdout.flush()
	
if __name__ == "__main__":
	main()
