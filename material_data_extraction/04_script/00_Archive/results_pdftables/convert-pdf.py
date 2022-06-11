import pdftables_api
import os 

# change directory path
os.chdir('d:\MBS\THESIS\\02_work_data\\00_UGZ\\00_bis190522\Aehrenweg_5')
		
# Get the current directory path
current_directory = os.getcwd()

c = pdftables_api.Client('9htta3nm40wu')
c.xlsx('Baustellenentsorgungskonzept2.pdf', 'output') 

#replace c.xlsx with c.csv to convert to CSV
#replace c.xlsx with c.xml to convert to XML
#replace c.xlsx with c.html to convert to HTML

