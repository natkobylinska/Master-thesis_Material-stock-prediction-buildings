from fileinput import filename
import os 
import pandas as pd

main_dir = "D:\\MBS\THESIS\\02_work_data\\00_UGZ\excel_database\\"

def folders_list(mother_path):

    database_path = mother_path + "\\02_work_data\\00_UGZ\materials_database"
    my_list = os.listdir(database_path)

    return len(my_list), my_list, database_path

def create_folders(root_path):
    _, extracted, _ = folders_list("D:\\MBS\THESIS")
    folders = extracted
    for folder in folders:
        os.mkdir(os.path.join(root_path,folder))

def rename_batch(path):
    for filename in os.listdir(path):
        os.rename(os.path.join(path,filename),os.path.join(path, filename.replace(' ', '_')))

def create_files():
    # to cal la cell in pandas pd.iloc[row_num, col_num]
    df = pd.read_csv('D:\MBS\THESIS\\02_work_data\\00_UGZ\\address_project_ID.csv')

    for i in range (df.shape[0]):
        file_name =  str(df.iloc[i,0]) + ".xlsx"
        save_path = os.path.join(main_dir, str(df.iloc[i,1]), file_name)
        df.to_excel(save_path, index = False)

    #path = os.path.join(main_dir, df.iloc[0,1], df.iloc[0,0])
    #path = "D:\\MBS\THESIS\\02_work_data\\00_UGZ\excel_database\\Ackersteinerstrasse_172"

def replace_excel_sheet():
    df = pd.read_csv('D:\MBS\THESIS\\02_work_data\\00_UGZ\\address_project_ID.csv', skiprows=49, encoding = "ISO-8859-1")
    df_frame = pd.read_csv('D:\MBS\THESIS\\02_work_data\\00_UGZ\material_framework.csv')
    #print(df_frame)

    for i in range (df.shape[0]):
        excelname = str(df.iloc[i,0]) + ".xlsx"  
        save_path = os.path.join(main_dir, str(df.iloc[i,1]), excelname)
        df_frame.to_excel(save_path, index = False)
 
#-------------------------------------------------------------------------------------------------------------------------------------------------



