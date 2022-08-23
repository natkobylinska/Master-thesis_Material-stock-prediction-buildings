from pdf2image import convert_from_path
from pathlib import Path
import os
import pandas as pd

#changable
Row_nr = 10
pdf_name = "PK 3.11 Unterlagen"

#-Path of the pdf----------------------------------------------------------------------
#read address_project_ID
ad = pd.read_csv("D:\MBS\THESIS\\02_work_data\\00_UGZ\\address_project_ID.csv", encoding = "ISO-8859-1")
print(ad.iloc[Row_nr,1])

folder_directory = "\\"+ad.iloc[Row_nr,0]
materials_path = "D:\MBS\THESIS\\02_work_data\\00_UGZ\materials_database"+folder_directory
PDF_file = materials_path+"\\"+pdf_name+".pdf"
excel_path = "D:\MBS\THESIS\\02_work_data\\00_UGZ\excel_database"+folder_directory
#--------------------------------------------------------------------------------------

# Store all the pages of the PDF in a variable
pages = convert_from_path(PDF_file, 500, first_page=7, last_page = 7)

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
