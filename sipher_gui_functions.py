import os
import getpass
from tkinter import filedialog, messagebox
import csv_exploit as csvex
from file_manager import move_file_accordingly
import db

global selected_files


Acceptable_Technology = "GSM DCode Data"

db_path = r"D:\AF\02. DOR\sipher\gti\src\sipher_terminal\database"


# D:\AF\02. DOR\sipher\gti\src\sipher_terminal\temp raw data storage\GSM


"""class progress:
    def __init__(self, parent, length, x, y):
        self.x = Progressbar(parent, orient='horizontal', length=length, mode='determinate')
        self.x.place(y=y, x=x)

    def add_progress(self, p_num):
        self.x['value'] = p_num
        gui.page_one.update_idletasks(self.x)"""

def do_nothing():
    None


def manage_db():
    filedialog.askopenfiles("*", initialdir=db_path)


def add_data():
    global selected_files
    username = getpass.getuser()
    # initialdir="/Users/" + username + "/Desktop"
    folder_name = filedialog.askdirectory(initialdir="C:\\Users\\"
                                                     + username + "\\Desktop")  # add unique cases of files
    selected_files = []  # sets and resets selected_ficles global
    invalid_File_type = []
    for root, dirs, files in os.walk(folder_name):
        for f in files:
            fp = os.path.join(root, f)
            fp = os.path.normpath(fp)
            tech_check = csvex.find_tech(fp)
            print(tech_check)
            if tech_check:
                print(fp)
                selected_files.append(fp)
            else:
                invalid_File_type.append(fp)

    if len(invalid_File_type) > 0:  # alert user to invalid file types
        messagebox.showinfo("Invalid Technology Types",
                            "Some of these files cannot be accepted "
                            "\n Please use only " + Acceptable_Technology)

    print(selected_files)
    return selected_files


def display_to_filetree(parent):
    file_arr = add_data()
    c = 0
    for file in file_arr:
        item = 'file' + str(c)
        b_arr = file_breakdown(file)
        parent.insert('', 'end', item, text=str(b_arr[1]))
        parent.set(item, 'Size', str(b_arr[2]))
        parent.set(item, 'Tech', str(b_arr[3]))
        c += 1


def remove_all_filetree_items(parent):
    global selected_files
    if len(selected_files) > 0:
        for i in parent.get_children():
            parent.delete(i)
        selected_files = []
    else:
        return


def file_breakdown(file):
    result = [file, csvex.path_leaf(file), csvex.file_size(file), csvex.find_tech(file)]
    return result


# D:\AF\02. DOR\sipher\gti\src\sipher_terminal\temp raw data storage\GSM
def send_data_to_db(file):          # do not use with file entry. use only with organized directory "database"
    leaf = csvex.path_leaf(file)    # ~The following variables create the data properties for all
    size = csvex.file_size(file)    # of the entries that will be input to the db
    tech = csvex.find_tech(file)    # ~These also will be the properties sipher will use to query
    type = csvex.find_type(file)    # based off of the user input and then
    date = csvex.find_year(file)

    thresh = csvex.decode_minandmax_latlong(file)
    max_lat, min_lat, max_lon, min_lon = thresh[0][0], thresh[0][1], thresh[1][0], thresh[1][1]

    build_entry = db.File(root_path=file,
                          # builds the entire entry for the entry_array to ingest, prepping it for a db.add_all function
                          name=leaf,
                          tech=tech,
                          data_type=type,
                          date=date,
                          size=size,
                          max_lat=max_lat,
                          min_lat=min_lat,
                          max_lon=max_lon,
                          min_lon=min_lon)

    try:
        db.session.rollback()
        db.session.add(build_entry)
        db.session.commit()
        db.session.close()

    except db.IntegrityError or db.OperationalError:  # This is triggered because a session was open in the python console as well as the running script and sql doesnt like that
        pass
    return


def confirm_filepath_exists_in_db(file):  # boolean to determine f/p exists in both the db and db-folder
    file = str(os.path.normpath(file))  # normalises f/p for windows
    x = db.session.query(db.File.root_path) \
        .filter(db.File.root_path == file) \
        .first()  # queries db with injested function parameter "file" as a string | returns true or false
    db.session.rollback()
    return False if not x else True


# TODO: add loading bar functionality for this function only
    # todo: make the send to sipher db func an individual file func
    # this recieves the file root from the file tree
def send_to_sipher_db(i):  #### !!!!! DO NOT USE PYTHON TERMINAL FOR DB SESSION WHILE TESTING DB !!!! ####
    # master_db_array = []
    # global selected_files                                               # these are the files that were initially loaded by the "Add Survey Data Button"
    #if not len(selected_files) > 0:
    #    messagebox.showerror("Error", "Please Select Files to load")
    #    return
    #try:
    #    for i in selected_files:
    move_file_accordingly(i)
                                                                        # moves files to correct position in sipher db-folder according to their file properties
    print("Printing Filepaths in database")
    for root, dirs, files in os.walk(db_path):                      # scans through the database folder
        for f in files:
            print(str(f))
            fp = os.path.join(root, f)                              # reads root file path
            fp = os.path.normpath(fp)                               # makes windows filepath default
            print(fp)

            #if db.session.query(db.File.root_path).count() > 0:
            #    master_db_array.append(fp)
            #    db.session.rollback()
            if not confirm_filepath_exists_in_db(
                    fp):                                   # boolean compares files in db-folder to existing db entries so to avoid duplicate root paths
                #master_db_array.append(fp)                          # appends non-existing f/p entries an array for later use
                send_data_to_db(i)
            else:
                pass

    """except NameError:  # user most likely pressed "Load to Database" Button without selecting Files first
        messagebox.showerror("Error", "Please Select Files to load")
        return""" # this part needs to go in the for loop on page one when the send_to_sipher_db func is executed
    # print("This is the master db_array before entry " + "\n" + str(master_db_array))

    # for i in master_db_array:  # enters an array of root paths that do not already exist into the db
    # send_data_to_db(i)

    """return messagebox.showinfo("Info",  # visual confirmation for user
                               "All selected files have been moved to the Sipher Database \n To view the database press the 'Manage Database' Button")"""







