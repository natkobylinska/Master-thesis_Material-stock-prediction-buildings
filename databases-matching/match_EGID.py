import pandas as pd
import multiprocessing
import time

# two databases to match
df_list = pd.read_csv('D:\MBS\THESIS\\02_work_data\\00_UGZ\\match_EGID.csv')
df_GWR = pd.read_csv('D:\MBS\THESIS\\01_imported_data\\07_GWR\zh\\filtered_records_GWR.csv', on_bad_lines='skip', sep=",", engine='python')

def EGID():
    print("I'm thinking...")
    for i in range (df_list.shape[0]):
        for j in range (df_GWR.shape[0]):
            if df_list.iloc[i]['Street_nm'] == df_GWR.iloc[j]['ADDRESSE']:
                #print("hey")
                if str(df_list.iloc[i]['Street_nr']) == str(df_GWR.iloc[j]['GEB_NUM']):
                    #print("you")
                    df_list.iat[i,10] = df_GWR.iloc[j]['EGID']
                else:
                    pass
            else:
                pass
    save_path = 'D:\MBS\THESIS\\02_work_data\\00_UGZ\\match_EGID_pandas.xlsx'
    df_list.to_excel(save_path, index = False)
    print("Success!")

def test():
    print ("counting..")

    for j in range (df_GWR.shape[0]):
        if df_GWR.iloc[j]['DEINR'] == "Ackersteinstrasse":
            print("LOL")
    print ("I completed")

if __name__ == '__main__':
    # Start foo as a process
    p = multiprocessing.Process(target=EGID, name="EGID")
    p.start()

    # Wait 60 seconds for
    time.sleep(1200)

    # Terminate
    p.terminate()

    # Cleanup
    p.join() 

    print ("Task closed")

