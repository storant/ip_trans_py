import pandas as pd
#import xlrd
import os
#from os import getcwd
#import os.path
import sys
from datetime import date
from pathlib import Path
import func as f
import shutil #used to copy some files. 
#import openpyxl
from money.money import Money
from money.currency import Currency
import time #used for time sleep 

# https://www.w3schools.com/python

# Declaring some variables
dir_path = os.getcwd() #current directory that the exe is in
report_folder = '.REPORTS_SENT' 
today = date.today().strftime("%d%b%Y").upper() #this is todays time, and will be used to create the report folder. 
folder_name = today 

#this is gonna be used to print out the created folder in the study_to_list fuinction
relative_dir = f'{dir_path}\{report_folder}\{folder_name}'
print(relative_dir)

# choosing and import xlsx files
print(f'\nWritten by that dude. Works on transport_data.xlsx and ip_data.xlsx as is. .png files only!! ')
print(f'--- Current Directory:  {dir_path}')
print(f'--- Report Directory: {dir_path}\{report_folder}')
print(f'--- Current Date:  {today}')

excel_file = str(input('\nPlease enter the name of the xlsx file ( .xlsx will be added automatically )\n: '))
excel_file += '.xlsx'

#STRIP THIS FUCKING INPUT MORON

print('\nExcel file imported. Referencing the "Main Table" sheet ')
df = pd.read_excel(excel_file,sheet_name='Main Table')


choice = int(input('\nEnter 1 for IP data (ip_data.xlsx).\nEnter 2 for Transport data (transport_data.xlsx).\n: '))
if choice == 1:
    print('\n1) cleaning the imported xlsx as a dataframe (DF), by remmoving all columns and rows outside the table ')
    new_df = f.ip_clean(df)
    #print(new_df)
    print('\n2) cleaning the df. by removing exmpty cells and removed comments ')
    print_df = f.ip_clean_xl(df,len(new_df))
    #print(print_df)
else:
    new_df = f.trans_clean(df)
    print('\n1) cleaning the imported xlsx as a dataframe (DF) ')
    print_df = f.trans_clean_xl(df,len(new_df))
    #print(print_df)


#
#new_df['Study'] = new_df['Study'].astype(str)
#new_df['Subject'] = new_df['Subject'].astype(str)

'''
#print(df.info())
#print(new_df.head())

#sample file naem
#print(f.index_to_string(new_df,0))
'''

# this prints where the folder report folder was placed to 
#print(dir_path,'\n',report_folder,'\n',folder_name)

print(f'\nCreating the report folder in: \n{dir_path}\\{report_folder} by the name of {folder_name}')
f.create_folder_report(dir_path,report_folder,folder_name)

print('\nUsing the study_to_list() function, we make a list of all the studies and subjects from the cleaned DF\n In order to make folders')
list_ = f.study_to_list(new_df,relative_dir)


#print(new_dir)

print(f'\n Trying to create subject and study folders\n')
for i in range(len(list_)):
    study = list_[i][0]
    subject = list_[i][1]
    f.create_f_study_subject(dir_path,report_folder,folder_name,study,subject)

dup_list = f.study_to_list_dup(new_df)

for i in range(len(dup_list)):
    #this was the old way of doing it.
    #dir_path = os.path.dirname(os.path.realpath('notebook.ipynb'))
    dir_path = os.getcwd()
    report_folder = '.REPORTS_SENT'
    folder_name = date.today().strftime("%d%b%Y").upper() 
    study = dup_list[i][0]
    subject = dup_list[i][1]
    name = f.index_to_string(new_df,i)
    target = f"{dir_path}\\{report_folder}\\{folder_name}\\{study}\\{subject}\\{name}"
    original = f'{dir_path}\\{study}\\{subject}\\{name}'
    shutil.copyfile(original, target)


f.save_xlsx(dir_path,report_folder,folder_name,print_df)


print('\nMake sure to mark invoiced cells as "Yes" in the appropriate originating xlsx file.\nAnd zip the report folder and send it off!\nThx\n ')	
time.sleep(20)