import csv_exploit as csvex
import os
import shutil

# f = r"D:\AF\02. DOR\sipher\gti\src\sipher_terminal\mess_data\dcode files\DCode_GSM_2019-04-19_09-01-22.txt"

db_path = r"{}.\sipher_terminal\database".format(os.getcwd())

def build_file_path(file):
    path = ''
    type = csvex.define_dcode(file)
    if type:
        path = db_path + r"\ics_500"
    else:
        path = db_path + r"\unknown_machines"
        return path
    tech = str(csvex.find_tech(file))

    # if tech != 'GSM':     # TODO this will have to be removed when we define/find a way to get UTC time from CDMA UMTS and LTE files
        #path = path + "\\" + tech
        #return path

    yr = csvex.find_year(file)
    if not yr:
        path = path + "\\" + tech
    else:
        path = path + "\\" + tech + "\\" + str(yr)
    return path


def move_file_accordingly(file):   # moves file based on its contents to the database folder
    dir = build_file_path(file)
    just_filename = csvex.path_leaf(file)
    if not os.path.isdir(dir):
        print(str(dir) + " does not exist, making dir")
        os.makedirs(dir)
    else:
        print(str(dir) + " exists")

    new_path = dir + "\\" + just_filename
    if not os.path.isfile(new_path):
        print(str(new_path) + " does not exist, renaming now")
        shutil.copy(file, new_path)                                 # THIS IS THE SMOKING GUN
    else:
        print(str(new_path) + " does exist")

        # TODO: design some sort of file protections "Do you wish to overwrite?" kind of thing


