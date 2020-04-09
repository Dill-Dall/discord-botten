import wget
import csv
import os
import time

from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM


if not os.path.exists('flags'):
	os.makedirs('flags')
	

file = csv.reader(open('Country_Flags.csv'), delimiter=',')
failed_list = ""
for line in file:
	countryname = line[0]
	svgfilename = line[1]
	url = line[2]
	try:
		print(f'downloading flag for {countryname} from {url} -> flags/{svgfilename}\n')
		wget.download(url, f'flags/{svgfilename}')
		print(f'converting "flags/{svgfilename}" -> "flags/{countryname}.png"')
		drawing = svg2rlg(f'flags/{svgfilename}')
		renderPM.drawToFile(drawing, f'flags/{countryname}.png', fmt="PNG")
	except Exception as e:
   		print(f'{url} failed\n')
		#failed_list = failed_list + countryname

print(f'Failed creating png file for: \n {failed_list}')
