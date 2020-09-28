import pandas as pd #needs to be installed in virtual envpip 

from new_func import remove_cols, df_to_list, create_folders,get_dir,get_date,df_paste_create_report,report_folder_dir,save_xlsx,create_zip, wait
from db_integrity import list_of_files,integrity_check

today = get_date() #today date in that clean format for the report
dir_path = get_dir() #current directory that the exe is in
report_folder = '.REPORTS_SENT' #sets the report folder
report_dir = report_folder_dir(dir_path,report_folder)

while True:
    excel_file = str(input('Please enter an excel file name. (Please include the extension): '))

    while True:
        try:
            import_xl = pd.read_excel(excel_file,sheet_name='Main Table')
            #import_xl = import_xl.applymap(str)
            break
        except:
            excel_file = str(input('Bad name, please try again: '))


    integrity = bool(input('<1> to run integrity chack, <Enter> to skip: '))
    print(integrity)
    if integrity == True:
        broken = integrity_check(import_xl.copy(),dir_path)
        if len(broken) == 0:
            print('No integrity errors. Excel "DB" lines up with files in the directory')
        else:
            print('Please check the excel file and the folders to make sure that the following files have the same names.')
            print(broken)
    else:
        print('Skipped integrity check')

    report_run = bool(input('<1> to run report, <Enter> to skip: '))
    if report_run == True:
        # these are the columns which are most important from the excel file and which will wbe passed on to everything!
        # they should be the same for both the xlsx files
        # with these cols, you HAVE to be able to make the folders!
        col_to_keep  = ['Study','Subject','Sugg_Name','Jupyter']

        #remove all hte columns which are not in col_to_keep
        df = remove_cols(import_xl.copy(),col_to_keep) #the .copy() here is necessary to maintain function scope, otherwise its global!

        # making a list to create folders, NO DUPLICATES
        clean_list = df_to_list(df)
        # making all the folders
        create_folders(dir_path,report_folder,clean_list) 

        full_list = list_of_files(df,dir_path,report_folder,today)
        df_paste_create_report(full_list)
        #copy and pasting everything form the full_list


        xx = import_xl.copy() #need to use the .copy() to not overwrite the df in globalscope
        col_to_keep_for_report  = ['Study','Subject','Sugg_Name','Total','Comments']
        #excel_df = remove_cols(xx,col_to_keep_for_report)
        #print(excel_df.head())
        save_xlsx(dir_path,report_dir,today,xx,col_to_keep_for_report)
        create_zip(today)
        print('Make sure to read SOP if neccessary. And update the Invoiced column in the Excel file to Yes. ')
    else:
        print('Skipped report generation')
    
    exit = bool(input('<1> to continue, <Enter> to exit:'))
    try:
        if exit == True:
            continue
        else:
            print('Written by AS. https://github.com/storant/ip_trans_py')
            wait(10)
            break
    except ValueError:
        continue






