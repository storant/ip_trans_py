import os
import sys
from datetime import date
#import os.path
from os import path
import shutil #copy and pasting files
from money.money import Money
from money.currency import Currency

#take the excel spreadsheet, scan it, return new_df which only contains rows which
#havent been invoiced
def trans_clean(df):
    df = df.iloc[:,[0,1,2,3,5,7,11]]
    new_df = df.dropna()
    new_df = new_df[new_df['Jupyter'] == 0]
    new_df = new_df.reset_index(drop=True)
    new_df = new_df.iloc[:,[0,1,2,3,4,5]] 
    #removes the invoiced column, cause 
    return new_df

def ip_clean(df):
    df = df.iloc[:,[0,1,2,3,4,5,9]]
    #print(df)
    new_df = df.dropna()
    new_df = new_df[new_df['Jupyter'] == 0]
    new_df = new_df.reset_index(drop=True)
    new_df = new_df.iloc[:,[0,1,2,3,4,5]] 
    #print(df)
    #removes the invoiced column, cause 
    return new_df

#segmens and prints the a requested study in the df
def study_pull(df,study):
    print(df[df.Study.isin([study])])

#returns the file name of each invoice .png
#MOVE TO THE FEDEX
def index_to_string(df,index):
    df_values = df.values
    list_ind = df_values[index].tolist()
    list_ind[4] = list_ind[4].strftime("%d.%m.%Y")
    hello = list_ind[5]
    hello = Money(str(hello),Currency.USD).format('en_US')
    list_ind[5] = hello
    #list_ind[5] = '$'+str(Money(list_ind[5],Currency.USD))
    fin = ' - '.join(map(str,list_ind))
    fin = fin+'.png'
    return fin

#return all folders to be created in the report from the df, going by the first
# 2 columns. THE STUDY AND SUBJECT. no dublicates
#use this list to create the report folders 
def study_to_list(df,relative_dir):
    test_df = df.loc[:,['Study','Subject']] #create new df with only study and subject
    #print(test_df)
    #print(test_df.info())
    test_df['Study'] = test_df['Study'].astype(str)
    test_df['Subject'] = test_df['Subject'].astype(str)
    test_df_2 = test_df.values.tolist() #convert this def to 
    #print(test_df_2)

    #make list into set to remove duplicates
    this_set = set()
    for occurance in test_df_2:
        new_ = occurance[0],occurance[1]
        this_set.add(new_)

    #make set back into list, cause other stuff is expecting a list, could be changed. 
    no_dup_list = list()

    #print(f'\nfolders created inside the report folder: ')
    for x in this_set:
        no_dup_list.append([x[0],x[1]])
        #this will print the directories which will be created in the future.
        #print(f'{relative_dir}\{x[0]}\{x[1]}')
        
    return no_dup_list

def study_to_list_dup(df):
    test_df = df.iloc[:,[0,1]] #create new df with only study and subject
    #print(test_df)
    test_df_2 = test_df.values.tolist() #convert this def to 
    return test_df_2


#create the report folder,
# inside the directory of where the file is (dir_path)
# dest_folder, where to create the folder. .REPORTS_SENT
# folder name, just the date of the report
def create_folder_report(dir_path,dest_folder,folder_name):
    #dir_path, original starting directory, 
    #dest_folder, wehre to create the report folder
    try:
        new_path = dir_path+'\\'+dest_folder
        os.chdir(new_path)
        os.mkdir(folder_name)
        os.chdir(dir_path)
        print('\nCreting report directory. Directory created. Using - create_folder_report()')
    except FileExistsError:
        print('ERROR - Report directory not created, because it exists. - FileExistsError')
        os.chdir(dir_path)
    except FileNotFoundError:
        print('Directory not created. - FileNotFoundError')
        os.chdir(dir_path)


def create_f_study_subject(dir_path,report_folder,report,study,subject):
    #dir_path, original starting directory, 
    #dest_folder, wehre to create the report folder, 
    #folder_name = SUBJECT ID
    try:
        new_path = dir_path+'\\'+report_folder+'\\'+report
        if path.exists(new_path+'\\'+study) == False:
            new_path = dir_path+'\\'+report_folder+'\\'+report
            #print(new_path)
            os.chdir(new_path)
            os.mkdir(study)
            next_path = dir_path+'\\'+report_folder+'\\'+report+'\\'+study
            os.chdir(next_path)
            os.mkdir(subject)
            os.chdir(dir_path)
            #this will print the path of the folder which was created, WHEN it was created
            print(f'\ncreated:\n{next_path}\{subject}')
            '''
            print('----------------------- new_path')
            print(new_path,subject)
            print(next_path,subject)
            print('----------------------- new_path')
            '''
        # this else statement is necessary because a study might contain more than 1 subject when inside the report, 
        # this else statement creates a folder for subjects, when a study has >1 subjects
        else:
            next_path = dir_path+'\\'+report_folder+'\\'+report+'\\'+study
            os.chdir(next_path)
            os.mkdir(subject)
            os.chdir(dir_path)
            #this will print the path of the folder which was created, WHEN it was created
            print(f'\ncreated:\n{next_path}\{subject}')
            '''
            print('----------------------- next_path')
            print(next_path,subject)
            print('----------------------- next_path')
            '''
    except FileExistsError:
        print('\nDirectory not created. - FileExistsError')
        os.chdir(dir_path)
        #print(new_path)
        print(f'{next_path}\{subject}')
    except FileNotFoundError:
        print('Directory not created. - FileNotFoundError')
        os.chdir(dir_path)

#take nrow of new df, and print only that of the xl spreadsheet
#in order to preserve commetn
def trans_clean_xl(df,len):
    new_df = df.iloc[:,[0,1,2,3,5,6,7,11,12]]
    new_df = new_df[new_df['Jupyter'] == 0]
    new_df = new_df.reset_index(drop=True)
    new_df = new_df.iloc[:,[0,1,2,3,4,5,8]] 
    new_df = new_df.iloc[0:len]
    return new_df


def ip_clean_xl(df,len):
    new_df = df.iloc[:,[0,1,2,3,4,5,9,10]]
    new_df = new_df[new_df['Jupyter'] == 0]
    new_df = new_df.reset_index(drop=True)
    new_df = new_df.iloc[:,[0,1,2,3,4,5,7]] 
    new_df = new_df.iloc[0:len]
    return new_df


def save_xlsx(dir_path,report_folder,report,df):
    new_path = dir_path+'\\'+report_folder+'\\'+report
    os.chdir(new_path)
    name = str(report)+'_report.xlsx'
    df.to_excel(name, sheet_name='Table')  
