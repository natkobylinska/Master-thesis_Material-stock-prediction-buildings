from pdf2image import convert_from_path
from pathlib import Path

#-Path of the pdf----------------------------------------------------------------------

PDF_file = "D:\MBS\THESIS\\02_work_data\\00_UGZ\materials_database\Ackersteinerstrasse_172\Schadstoffbericht Jäckli Geologie AG vom 2020-09-18.pdf"
my_path = "D:\MBS\THESIS\\02_work_data\\00_UGZ\excel_database\Ackersteinerstrasse_172"
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
	filename = "page_"+str(image_counter)+".jpg"
	
	if filename == "page_40.jpg":
		# Save the image of the page in system
		page.save(filename, 'JPEG')
	else:
		pass

	# Increment the counter to update filename
	image_counter = image_counter + 1

print ("success")