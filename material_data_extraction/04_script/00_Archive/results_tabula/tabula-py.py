import tabula as tb
import pandas as pd
import os

# change directory path
os.chdir('D:\MBS\THESIS\\02_work_data\\00_UGZ\materials_database\Ackersteinerstrasse_172')
		
# Get the current directory path
current_directory = os.getcwd()
	
# Print the current working directory
print("Current working directory:", current_directory)

df = tb.read_pdf('Schadstoffbericht Jäckli Geologie AG vom 2020-09-18.pdf', pages = '40')
for i in range(len(df)):
 df[i].to_excel('file_'+str(i)+'.xlsx')
