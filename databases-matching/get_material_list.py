import pandas as pd
import os
import multiprocessing
import time

#reads multiple csv files, extracts material information and outputs a single .csv file 

main_dir = "D:\\MBS\THESIS\\02_work_data\\00_UGZ\excel_database\\"

df_pro_id = pd.read_csv('D:\MBS\THESIS\\02_work_data\\00_UGZ\\address_project_ID.csv', on_bad_lines='skip', sep=",", engine='python', encoding = "ISO-8859-1")
#df_mat_list = pd.read_csv('D:\MBS\THESIS\\02_work_data\\00_UGZ\\Materials_Analysis.csv', on_bad_lines='skip', sep=",", engine='python')

df_old = pd.DataFrame([0,6])

print("I'm thinking...")
for i in range (df_pro_id.shape[0]):
    file_name =  str(df_pro_id.iloc[i,0]) + ".xlsx"
    save_path = os.path.join(main_dir, str(df_pro_id.iloc[i,1]), file_name)
    df_current = pd.read_excel(save_path)
    for j in range(df_current.shape[0]):
        if pd.isnull(df_current.iloc[j][4]) and pd.isnull(df_current.iloc[j][5]) and pd.isnull(df_current.iloc[j][6]):
            pass
        else:
            df_name = pd.DataFrame([file_name])
            df = df_current.iloc[[j]]
            df.insert(0, "project_id", [file_name])
            frames = [df_old, df]
            df_old = pd.concat(frames) 

save_path = 'D:\MBS\THESIS\\02_work_data\\00_UGZ\\Materials_Analysis.xlsx'
df_old.to_excel(save_path, index = False)
print("Success!")

