import cv2 as cv
import numpy as np
import pandas as pd
import pytesseract

#link pytesseract location
pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\\tesseract.exe'

#-----------------------------------------------------------------------------------------
#Project specific:

#image to extract
filename = 'page_2.jpg'
## set keywords = expected columns
keywords = ['Abfallart','m','t','Angaben zu Entsorgung']
## set line index = expected rows
first_line_index = 1
last_line_index = 26
## output document
excelname = "aa.xlsx"
#-----------------------------------------------------------------------------------------

#PREPROCESSING
# resize image if needed (it'll be harder for cv to 'read' a very small picture)
#scale_percent = 100 # percent of original size
#width = int(img.shape[1] * scale_percent / 100)
#height = int(img.shape[0] * scale_percent / 100)
#dim = (width, height)
#img = cv.resize(img, dim, interpolation = cv.INTER_AREA)
img = cv.imread(cv.samples.findFile(filename))
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

def is_vertical(line):
    return line[0]==line[2]

def is_horizontal(line):
    return line[1]==line[3]

def overlapping_filter(lines, sorting_index):
    filtered_lines = []
    
    lines = sorted(lines, key=lambda lines: lines[sorting_index])
    separation = 5    
    for i in range(len(lines)):
        l_curr = lines[i]
        if(i>0):
            l_prev = lines[i-1]
            if ( (l_curr[sorting_index] - l_prev[sorting_index]) > separation):
                filtered_lines.append(l_curr)
        else:
            filtered_lines.append(l_curr)
                
    return filtered_lines
    
def detect_lines(img, title='default', rho = 1, theta = np.pi/180, threshold = 50, minLinLength = 290, maxLineGap = 6, display = False, write = False):
    # Check if image is loaded fine
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    
    if gray is None:
        print ('Error opening image!')
        return -1
    
    dst = cv.Canny(gray, 50, 150, None, 3)
    
    # Copy edges to the images that will display the results in BGR
    cImage = np.copy(img)
    
    #linesP = cv.HoughLinesP(dst, 1 , np.pi / 180, 50, None, 290, 6)
    linesP = cv.HoughLinesP(dst, rho , theta, threshold, None, minLinLength, maxLineGap)
    
    horizontal_lines = []
    vertical_lines = []
    
    if linesP is not None:
        #for i in range(40, nb_lines):
        for i in range(0, len(linesP)):
            l = linesP[i][0]

            if (is_vertical(l)):
                vertical_lines.append(l)
                
            elif (is_horizontal(l)):
                horizontal_lines.append(l)
        
        horizontal_lines = overlapping_filter(horizontal_lines, 1)
        vertical_lines = overlapping_filter(vertical_lines, 0)
            
    if (display):
        for i, line in enumerate(horizontal_lines):
            cv.line(cImage, (line[0], line[1]), (line[2], line[3]), (0,255,0), 3, cv.LINE_AA)
            
            cv.putText(cImage, str(i) + "h", (line[0] + 5, line[1]), cv.FONT_HERSHEY_SIMPLEX,  
                       0.5, (0, 0, 0), 1, cv.LINE_AA) 
            
        for i, line in enumerate(vertical_lines):
            cv.line(cImage, (line[0], line[1]), (line[2], line[3]), (0,0,255), 3, cv.LINE_AA)
            cv.putText(cImage, str(i) + "v", (line[0], line[1] + 5), cv.FONT_HERSHEY_SIMPLEX,  
                       0.5, (0, 0, 0), 1, cv.LINE_AA) 
            
        cv.imshow("Source", cImage)
        #cv.imshow("Canny", cdstP)
        cv.waitKey(0)
        cv.destroyAllWindows()
        
    if (write):
        cv.imwrite("../Images/" + title + ".png", cImage);
        
    return (horizontal_lines, vertical_lines)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------
#ROI SELECTION

#crop image
def get_cropped_image(img, x, y, w, h):
    cropped_image = img[ y:y+h , x:x+w ]
    return cropped_image

def get_ROI(img, horizontal, vertical, left_line_index, right_line_index, top_line_index, bottom_line_index, offset=2):
    x1 = vertical[left_line_index][2] + offset
    y1 = horizontal[top_line_index][3] + offset
    x2 = vertical[right_line_index][2] - offset
    y2 = horizontal[bottom_line_index][3] - offset
    
    w = x2 - x1
    h = y2 - y1
    
    cropped_image = get_cropped_image(img, x1, y1, w, h)
    
    return cropped_image, (x1, y1, w, h)

def draw_text(src, x, y, w, h, text):
    cFrame = np.copy(src)
    cv.rectangle(cFrame, (x, y), (x+w, y+h), (255, 0, 0), 2)
    cv.putText(cFrame, "text: " + text, (50, 50), cv.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 5, cv.LINE_AA)
    
    return cFrame

def detect(cropped_frame, is_number = False):
    if (is_number):
        text = pytesseract.image_to_string(cropped_frame, lang = "deu", config='--psm 10')
    else:
        text = pytesseract.image_to_string(cropped_frame, lang = "deu", config='--psm 10')              
    return text

horizontal, vertical = detect_lines(img, minLinLength=350, display=True, write = True)

#-------------------------------------------------------------------------------------------------------------------
# TEXT EXTRACTION

output = {}
counter = 0

print("Start detecting text...")

(thresh, bw) = cv.threshold(gray, 100, 255, cv.THRESH_BINARY)

for i in range(first_line_index, last_line_index):
    for j, keyword in enumerate(keywords):

        counter += 1 
        left_line_index = j
        right_line_index = j+1
        top_line_index = i
        bottom_line_index = i+1
            
        cropped_image, (x,y,w,h) = get_ROI(bw, horizontal, vertical, left_line_index, right_line_index, top_line_index, bottom_line_index)

        # uncomment to check cropped images
        #filename = 'savedImage'+str(j)+'.jpg'
        #cv.imwrite(filename, cropped_image)   

        text = detect(cropped_image, is_number=True)
        output.setdefault(j, []).append(text)

#------------------------------------------------------------------------------------------------------------------------------------------------
#PANDAS MAGIC

df = pd.DataFrame(output).T
df.reset_index(inplace=True)
df = df.transpose()
df.columns = ['material', 'm3', 't', 'disposal']

#get rid of the unnecessary text in the page title
#for index, row in df.iterrows():
#   if row['material'] == 'Abfallart' or row['material'] == 'Ahfallart':
#       break
#   df.drop([index],inplace=True)

df.to_excel(excelname)

#-------------------------------------------------------------------------------------------------------------------------------------------------
print ("success")
