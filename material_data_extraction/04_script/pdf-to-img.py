from pdf2image import convert_from_path
from pathlib import Path
import os

#-Path of the pdf----------------------------------------------------------------------
folder_directory = "\Affolternstrasse134"
materials_path = "D:\MBS\THESIS\\02_work_data\\00_UGZ\materials_database"+folder_directory
PDF_file = materials_path+"\\Transportdispositiv , Entsorgungskonzept Kantone.pdf"
excel_path = "D:\MBS\THESIS\\02_work_data\\00_UGZ\excel_database"+folder_directory
#--------------------------------------------------------------------------------------

# Store all the pages of the PDF in a variable
pages = convert_from_path(PDF_file, 500)

# Counter to store images of each page of PDF to image
image_counter = 1

# Iterate through all the pages stored above
for page in pages:

	# Declaring filename for each page of PDF as JPG
	# For each page, filename will be:
	# PDF page 1 -> page_1.jpg
	# PDF page 2 -> page_2.jpg
	# PDF page 3 -> page_3.jpg
	# ....
	# PDF page n -> page_n.jpg
	filename = os.path.join(excel_path,"page_"+str(image_counter)+".jpg")
	
	page.save(filename, 'JPEG')

	# Increment the counter to update filename
	image_counter = image_counter + 1

print ("success")