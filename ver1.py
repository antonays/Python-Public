import sys, os
from datetime import datetime
from os.path import join, splitext, split, exists
from shutil import copyfile
from filecmp import cmp

rootOfEvil="c:\users\Anton\\"

def main():
	flag=0
	control=""
	print "Enter Destination Drive"
	while flag!=1:
		drive=raw_input("Drive>>")
		if (len(drive)==1):
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

def go(src,d,what):
	count=0
	total=0
	print src
	dest=d+what.upper()+"_BACKUP"+datetime.now().strftime("%Y-%m-%d")+"\\"
	for path, dirname, fnames in os.walk(src):
		total += len(fnames)
	print "Total: %d "%total+what.title()+" Files"
	count = copy_directory(src,dest,total)
	print "Done"+ what.upper()+", copied %d out of %d"%(count,total)
	
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
				except:
					print "error"
					error+=1
			else:
				skipped+=1
			sys.stdout.write("\r%d Out of: %d"%(count,total))
			sys.stdout.flush()
	sys.stdout.write("\n")
	print "Copied: %d\nSkipped: %d\nErrors:%d\nOut Of Total %d"%(count,skipped,error,total)
	return count

if __name__ == "__main__":
	main()