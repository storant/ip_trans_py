import os
from os import path
import sys
#import pandas as pd #comment out when no testing

from new_func import remove_cols,get_dir

# returns a list of errors!
# input: df and path
# output: returns a list of all mismatchess

def integrity_check(df,dir_path):
    col_to_keep = ['Study','Subject','Sugg_Name'] #list of columns to keep

    df = remove_cols(df,col_to_keep)

    name = df['Sugg_Name'].tolist()
    name = [x+'.png' for x in name] #adding png at the end for the file naem

    study = df['Study'].astype(str).tolist() # some subjects might be ints, so this converts evrything to a srtring!
    subject = df['Subject'].astype(str).tolist() # some subjects might be ints, so this converts evrything to a srtring!

    full_list = [[x,y,z] for x,y,z in zip(study,subject,name)] 
    # makes 2d list [[study,subj,filename],[study,subj,filename]...]

    full_list = [[a,b,c,os.path.join(dir_path,a,b,c)] for a,b,c in full_list]   #adds the fulll directory of the invoice to the nested lists
    location_full_list = [[a,b,c,d,os.path.exists(d)] for a,b,c,d in full_list] #adds if the invoice exists

    broken = [x for x in location_full_list if x[4]==False] #makes a new list with all the things which are broken. 
    return broken


def list_of_files(df,dir_path,report_folder,today):
    col_to_keep = ['Study','Subject','Sugg_Name','Jupyter'] #list of columns to keep

    df = remove_cols(df,col_to_keep)
    
    name = df['Sugg_Name'].tolist()
    name = [x+'.png' for x in name] #adding png at the end for the file naem

    study = df['Study'].astype(str).tolist() # some subjects might be ints, so this converts evrything to a srtring!
    subject = df['Subject'].astype(str).tolist() # some subjects might be ints, so this converts evrything to a srtring!
    jupyter = df['Jupyter'].astype(str).tolist() # some subjects might be ints, so this converts evrything to a srtring!

    full_list = [[a,b,c,d] for a,b,c,d in zip(jupyter,study,subject,name)] 
    # makes 2d list [[study,subj,filename],[study,subj,filename]...]

    full_list = [[jupyter, study, subject, name, os.path.join(dir_path,study,subject,name),os.path.join(dir_path,report_folder,today,study,subject,name)] for jupyter,study,subject,name in full_list]   #adds the fulll directory of the invoice to the nested lists
    #location_full_list = [[a,b,c,d,os.path.exists(d)] for a,b,c,d in full_list]
    return full_list


'''
excel_file = str(input('Please enter an excel file name. (Please include the extension): '))
import_xl = pd.read_excel(excel_file,sheet_name='Main Table')
print(integrity_check(import_xl,os.getcwd()))
'''