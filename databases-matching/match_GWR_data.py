from numpy import NaN
import pandas as pd
import multiprocessing
import time

#Adjust your directories -------------------------------------------------------------------------------------
df_list = pd.read_csv('D:\MBS\THESIS\\02_work_data\\00_UGZ\\Mothership_for_more_GWR_records.csv')
df_GWR = pd.read_csv('D:\MBS\THESIS\\01_imported_data\\07_GWR\zh\\GWR_filtered_records.csv', on_bad_lines='skip', sep=",", engine='python')

#apt_num = df_list.columns.get_loc('APT_NUM')
#h_type = df_list.columns.get_loc('H_TYPE')
#w_type = df_list.columns.get_loc('W_TYPE')
a_type = df_list.columns.get_loc('Abbruch')

#method = df_list.columns.get_loc('Method')
# baujahr = df_list.columns.get_loc('Baujahr')
# bauperiode = df_list.columns.get_loc('Bauperiode')
# stories = df_list.columns.get_loc('Nr of stories')
# flache = df_list.columns.get_loc('Fläche')
# volume = df_list.columns.get_loc('Volume')

def GWR():
    count = 0
    print("I'm thinking...")
    for i in range (df_list.shape[0]):
        print(count)
        for j in range (df_GWR.shape[0]):
            if df_list.iloc[i]['EGID'] == df_GWR.iloc[j]['EGID']:
                #print("hey")
                # df_list.iat[i,baujahr] = df_GWR.iloc[j]['GBAUJ']
                # df_list.iat[i,bauperiode] = df_GWR.iloc[j]['GBAUP']
                # df_list.iat[i,stories] = df_GWR.iloc[j]['GASTW']
                #df_list.iat[i,w_type] = df_GWR.iloc[j]['GWAERZH1']
                #df_list.iat[i,h_type] = df_GWR.iloc[j]['GWAERZH2']
                df_list.iat[i,a_type] = df_GWR.iloc[j]['GABBJ']
                # control
                # df_list.iat[i,19] = df_GWR.iloc[j]['EGID']
            else:
                pass
        count = count + 1
        if count == 415:
            break
        else:
            pass
    save_path = 'D:\MBS\THESIS\\02_work_data\\00_UGZ\\Mothership_pandas_abbruchjahr.xlsx'
    df_list.to_excel(save_path, index = False)
    print("Success!")

GWR()
# if __name__ == '__main__':
#     # Start foo as a process
#     p = multiprocessing.Process(target=GWR, name="GWR")
#     p.start()

#     # Wait 60 seconds for
#     time.sleep(1800)

#     # Terminate
#     p.terminate()

#     # Cleanup
#     p.join() 

#     print ("Task closed")

