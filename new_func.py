import os
from os import path, chdir

import time 
from datetime import date #needs to be installed in virtual env

from shutil import copyfile,make_archive
import pandas as pd

def get_dir():
    return os.getcwd() 

def get_date():
    return date.today().strftime("%d%b%Y").upper()

def report_folder_dir(dir,report):
    return os.path.join(dir,report,get_date())

def wait(amount):
    time.sleep(amount)

# function to remove all unecessary columns from a data frame
# input is a df, list of ones to remove, also removes all NaN
# output is changed df
def remove_cols(dataframe,col_to_keep):
    all_cols = dataframe.columns.tolist() #creates a list of all DF columns
    to_remove = [x for x in all_cols if x not in col_to_keep] #makes a new list with all columns to remove

    for removal in to_remove: #removes all columns from the df
        dataframe.pop(removal)

    dataframe = dataframe.dropna(subset=['Study']) #drop na only scans for NA in this column!, so it doesnt drop everything in Comments!
    return dataframe

# making a list to create fodlers.
# input: df
# output: nested list of studies and subjects, no duplicates!
def df_to_list(df):
    study = df['Study'].astype(str).tolist()
    subject = df['Subject'].astype(str).tolist()
    jupyter = df['Jupyter'].astype(str).tolist()

    fresh_list = [[x,y,z] for x,y,z in zip(study,subject,jupyter)] #makes a 2d list of study and subject for folder creation
    fresh_set = { (nested[0],nested[1],nested[2]) for nested in fresh_list } #converts it to a set to remove duplicates
    fresh_set = [[x,y] for x,y,z in fresh_set if z=='0'] #back to 2d list

    return fresh_set

#make a nested list of [[study,subject,jupyter,dir1,dir2]]
#list of folders. 
def df_paste_create_report(a_list):
    for item in a_list:
        if item[0] == '0':
            try:
                copyfile(item[4],item[5])
            except FileNotFoundError:
                print('\nDO NOT SEND OUT REPORT.\nPlease run the intergrity check. You have either missing or missnamed files.\nThere might be more errors than necessarily outlined here.\nPlease delete the report generated today as well which contains this error.\n You will be able to rerun the report generation after making correcitons after the intergrity check! ')
                print('File note found (as per xlsx database)')
                print(item[3])
                time.sleep(5)
    
#cretes the report and study folders
#input: list of dirs to create, current os, report folder
#output: nothing
def create_folders(dir,report,clean_list):
    creating = os.path.join(dir,report,get_date())
    try:
        os.mkdir(creating)
    except FileExistsError:
        print('Report folder already created',creating)

    #crate a list of paths' to create
    dir_list = [os.path.join(creating,x[0],x[1]) for x in clean_list]

    #create all the paths', in a seperate loop to enable try except for error handlings. 
    for dir in dir_list:
        try:
            os.makedirs(dir)
        except FileExistsError:
            print('Study/Subject folder already created',dir)

#create the xlsx file for the report. 
# input: 
    # directory to save the excel file in 
    # today, to name the excel file,
    # dfr just the data  frame...
    # keep cols....
# output: nothing
def save_xlsx(dir_path,report_path,today,dfr,keep_cols):
    dfr = dfr.reset_index(drop=True) #necessary
    dfr = dfr[dfr['Jupyter'] == 0]
    dfr = remove_cols(dfr,keep_cols)
    os.chdir(report_path) #cahnge path to the today directory report
    name = str(today)+'_report.xlsx'
    dfr.reset_index(inplace = True, drop = True) #reset the index to 0, idk why the above one doesnt do it
    dfr.to_excel(name, sheet_name='Main_Table') #save excel spreadsheet
    create_zip(today) #create the zip file
    os.chdir(dir_path)

def create_zip(today):
    make_archive(str(today)+'_report','zip',root_dir=None,base_dir=None)