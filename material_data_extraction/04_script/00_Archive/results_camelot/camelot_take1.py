import camelot
import pandas

tables=camelot.read_pdf('D:\MBS\THESIS\\02_work_data\\00_UGZ\materials_database\Ackersteinerstrasse_172\Schadstoffbericht Jäckli Geologie AG vom 2020-09-18.pdf', 
flavor='stream', pages='41')

df=tables[0].df
print(df)  

df.to_excel("ps.xlsx")
#print(tables[0].parsing_report)