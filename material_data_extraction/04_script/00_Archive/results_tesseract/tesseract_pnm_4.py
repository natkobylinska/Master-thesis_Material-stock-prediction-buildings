# Import libraries
from PIL import Image
import pytesseract
from pytesseract import Output
import sys
from pdf2image import convert_from_path
import cv2
import pandas as pd

#path tesseract
pytesseract.pytesseract.tesseract_cmd = "C:\Program Files\Tesseract-OCR\\tesseract.exe"

# Path of the pdf
PDF_file = "D:\MBS\THESIS\\02_work_data\\00_UGZ\\00_bis190522\Aehrenweg_5\Baustellenentsorgungskonzept.pdf"

#Part2 - Recognizing text from the images using OCR

img = cv2.imread("page_2.jpg")

d = pytesseract.image_to_data(img, lang='deu', config='--psm 4 -c tessedit_char_blacklist=,', output_type=Output.DICT)
#d = pytesseract.image_to_data(img, lang='deu', output_type=Output.DICT)
df = pd.DataFrame(d)

# clean up blanks, only cells with the text stay
df1 = df[(df.conf != '-1') & (df.text != ' ') & (df.text != '')]
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

#get rid of the unnecessary text in the page title
for index, row in df1.iterrows():
   if row["text"] == 'Abfallart':
        break
   df1.drop([index],inplace=True)

#check before writing to .csv
filename ="pandass.xlsx"
with open(filename,"w") as f:
	df1.to_excel(filename)

# Creating a text file to write the output
with open("out_text.csv","w") as f:
	# sort blocks vertically
	sorted_blocks = df1.groupby('block_num').first().sort_values('top').index.tolist()

	#iterate through segregated DF objects
	for block in sorted_blocks:
		curr = df1[df1['block_num'] == block] #segragated by block nr
		sel = curr[curr["text"].str.len() > 3]

		# sel = curr
		char_w = (sel.width / sel["text"].str.len()).mean()
		prev_par, prev_line, prev_left = 0, 0, 0
		text = ''

		for ix, ln in curr.iterrows():
			# add new line when necessary
			if prev_par != ln['par_num']:
				text += '\n'
				prev_par = ln['par_num']
				prev_line = ln['line_num']
				prev_left = 0
			elif prev_line != ln['line_num']:
				text += '\n'
				prev_line = ln['line_num']
				prev_left = 0

			added = 0  # num of spaces that should be added
			if ln['left'] / char_w > prev_left + 1:
				added = int((ln['left']) / char_w) - prev_left
				text += '_' * added
			text += ln['text']
			prev_left += len(ln['text']) + added + 1
		text += '\n'
		f.write(text)

f.close()	
print("success!")