import os
import sys
import re
import Image

def isImg(file):
	return re.search("(\.jpg|\.gif|\.png)",file)

def getClass(file):
	return file[0:re.search("(\.jpg|\.gif|\.png)",file).start()]

dir = "./"
argv = sys.argv
argc = len(argv)

if argc == 2:
	dir = argv[1]
	if not re.search("/$",dir):
		dir += "/"

files = os.listdir(dir);

dx = 0
dy = 0

for file in files:
	if isImg(file):
		img = Image.open(dir+file)
		dy += img.size[1]
		if img.size[0] > dx:
			dx = img.size[0]
			
canvas = Image.new("RGB", (dx,dy), (255,255,255))

cy = 0
css_text = ""
for file in files:
	if isImg(file):
		img = Image.open(dir+file)
		
		size = img.size
		css_text += """
			.%s{
				display: block;
				width: %dpx;
				height: %dpx;
				background-image: url('./sprite.jpg');
				background-repeat: no-repeat;
				background-position: %dpx %dpx;
			}
		""" % (getClass(file),size[0],size[1],0,-cy)
		
		canvas.paste(img, (0, cy))
		cy += img.size[1]
		
canvas.save("./sprite.jpg", "JPEG", quality=100, optimize=True)

f = open("./sprite.htm","w")
f.write("<html><head><style type=\"text/css\">"+css_text+"</style></head><body>")
for file in files:
	if(isImg(file)):
		f.write("""
			<p>%s</p>
			<div class="%s"></div>
		""" % (file,getClass(file)))
		
f.write("</body></html>")
f.close()

