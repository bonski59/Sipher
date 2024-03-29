import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from _datetime import datetime as dt
import os
import sipher_gui_functions as sg
import db
import shutil
from tkinter.ttk import Progressbar

import csv_exploit as csvex

class color_scheme:
    def __init__(self, bg, fg, abg, pressed, warning, caution, note, complete):
        self.bg = bg
        self.fg = fg
        self.abg = abg
        self.pressed = pressed
        self.warning = warning
        self.caution = caution
        self.note = note
        self.complete = complete

class tab_names:
    def __init__(self, spr, manage):
        self.sipher = spr
        self.manage = manage



tab = tab_names('SIPHER', 'MANAGE')
si_color = color_scheme('#3a464b', 'white', '#6E7A7F', 'white', 'red', 'orange', 'yellow', 'green')

# noinspection PyShadowingNames
class sipher(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # setup window
        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        container.configure(background=si_color.bg)
        self.title('Sipher')
        self.geometry('600x400+500+125')

        self.wm_iconbitmap('logo.ico')

        self.frames = {}

        for F in (page_one, page_two):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nesw")
            frame.config(bg=si_color.bg)

        self.show_frame(page_two)

    def show_frame(self, context):
        frame = self.frames[context]
        frame.tkraise()

class page_one(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # phony button
        label = my_lbl(self, text=tab.manage)
        label.place(x=0)
        label.config(width=27)

        # nav buttons
        btn(self, tab.sipher, lambda: controller.show_frame(page_two), 0, 27, 'normal').place(x=200)

        load_bar = Progressbar(self, orient='horizontal', length=146, mode='indeterminate')

        def loading():
            self.update()
            load_bar.place(y=60, x=430)
            load_bar.start()


        def done_loading():
            load_bar.stop()
            load_bar.place_forget()

        # TODO get this mf a mf loading bar !!!!!!!!!!

        def display_to_ft(parent):
            self.update()
            loading()
            file_arr = sg.add_data()
            self.update_idletasks()
            for file in file_arr:
                item = str(file)
                b_arr = sg.file_breakdown(file)
                parent.insert('', 'end', item, text=str(b_arr[1]))
                parent.set(item, 'Size', str(b_arr[2]))
                parent.set(item, 'Tech', str(b_arr[3]))

            done_loading()

        # top row buttons
        def add_svy_data():
            display_to_ft(tree)
            load.config(state='normal')
            clear.config(state='normal')

        action_btn(self, 'Add Survey Data', lambda: add_svy_data(), 5, 27, 'groove').place(y=27)
        action_btn(self, 'Manage Database', sg.manage_db, 5, 27, 'groove').place(x=200, y=27)
        # action_btn(self, 'Settings', sg.do_nothing, 5, 27, 'groove').place(x=400, y=27)

        # bottom row buttons
        def clr_selection():
            for child in tree.get_children():
                tree.delete(child)
            load.config(state='disabled')
            clear.config(state='disabled')

        def add_to_db():

            for child in tree.get_children():
                try:
                    sg.send_to_sipher_db(child)
                except NameError:  # user most likely pressed "Load to Database" Button without selecting Files first
                    messagebox.showerror("Error", "Please Select Files to load")
                    return

        clear = btn(self, 'Clear Selection', lambda: clr_selection(), 2, 19, 'disabled')
        load = btn(self, 'Load to Database', add_to_db, 2, 19, 'disabled')
        quit_ = btn(self, 'Quit', lambda: quit(), 2, 19, 'normal')


        bottom_btn_arr = [clear, load, quit_]
        cx = 0

        for i in bottom_btn_arr:
            i.place(y=354, x=5 + cx)
            cx += 149



        # file selection viewer
        tree = ttk.Treeview(self)
        lbl_arr = ('Size', 'Tech')
        tree.config(columns=lbl_arr, height=10)
        for i in lbl_arr:
            tree.column(i, width=len(i) + 110, anchor='w')
            tree.heading(i, text=i)
        tree.column("#0", width=len('File Name') + 350, anchor='w')
        tree.heading('#0', text='File Name')
        tree.place(x=5, y=120)

# noinspection PyUnusedLocal
class page_two(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # top row btns
        label = my_lbl(self, text=tab.sipher)
        label.place(x=200)
        label.config(width=27)
        btn(self, tab.manage, lambda: controller.show_frame(page_one), 0, 27, 'normal').place(x=0)

        # inputs - tech(checkmks) ftype(dcode, twr, csv) yr(old>new dropdown) location(GAR, KBKP, DD, DD area)
        # data - tree view(f_name, size, area data, UTC date, air/grnd)
        self.columnconfigure((0, 1, 2, 3, 4, 5, 6, 7), minsize=75, weight=1)
        self.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), minsize=40, weight=1)

        # widget separation -- (parent, row, col, col_span, row_span) always sticky='nsew'
        techbox = container(self, 1, 2, 2, 2)
        techbox.rowconfigure((0, 1, 2), weight=1)
        techbox.columnconfigure((0, 1), weight=1)

        typebox = container(self, 1, 4, 2, 2)

        timebox = container(self, 1, 6, 2, 2)
        locbox = container(self, 1, 0, 2, 6)
        btnbox = container(self, 7, 0, 2, 3)


        tk.Label(techbox, text='Technology', bg=si_color.abg).grid(row=0, column=0, columnspan=2)

        gsm_bool = tk.IntVar()
        gsm = check_box(techbox, 'GSM', 1, 0, gsm_bool, 'normal')
        cdma_bool = tk.IntVar()
        cdma = check_box(techbox, 'CDMA', 2, 0, cdma_bool, 'normal')
        umts_bool = tk.IntVar()
        umts = check_box(techbox, 'UMTS', 1, 1, umts_bool, 'normal')
        lte_bool = tk.IntVar()
        lte = check_box(techbox, 'LTE', 2, 1, lte_bool, 'normal')


        # time box
        def find_dates():
            thresh = 20
            currentyr = dt.now().year
            yrs_opt = []
            while thresh >= 0:
                yrs_opt.append(currentyr - thresh)
                thresh -= 1
            return yrs_opt

        timebox.rowconfigure((0, 1, 2), weight=1)
        timebox.columnconfigure((0, 1), weight=1)
        tk.Label(timebox, text='Time Frame', bg=si_color.abg).grid(row=0, column=0, columnspan=2)
        yr_list = find_dates()


        tk.Label(timebox, text='Earliest >', bg=si_color.abg).grid(row=1, column=0, sticky='e')
        earliest_var = tk.IntVar()
        earliest_var.set(yr_list[-4])
        earliest = tk.OptionMenu(timebox, earliest_var, *yr_list)
        earliest.grid(row=1, column=1, sticky='e')

        tk.Label(timebox, text='Latest >', bg=si_color.abg).grid(row=2, column=0, sticky='e')
        latest_var = tk.IntVar()
        latest_var.set(yr_list[-1])
        latest = tk.OptionMenu(timebox, latest_var, *yr_list)
        latest.grid(row=2, column=1, sticky='e')

        # type box
        typebox.columnconfigure((0, 1), weight=1)
        typebox.rowconfigure((0, 1, 2), weight=1)
        tk.Label(typebox, text='File Types', bg=si_color.abg).grid(row=0, column=0, columnspan=2)

        dcode_bool = tk.IntVar(value=1)
        check_box(typebox, 'DCode', 1, 0, dcode_bool, 'normal')
        tower_bool = tk.IntVar()
        tower_box = check_box(typebox, 'Tower', 1, 1, tower_bool, 'disabled')
        csv_bool = tk.IntVar()
        check_box(typebox, 'CSV', 2, 0, csv_bool, 'disabled')
        rns_bool = tk.IntVar()
        check_box(typebox, 'RNS', 2, 1, rns_bool, 'disabled')
        # location
        locbox.columnconfigure((0, 1), weight=1)
        locbox.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), minsize=20, weight=1)
        tk.Label(locbox, text='Location', bg=si_color.abg).grid(row=0, column=0, columnspan=1, sticky='nw')

        def del_then_insert(show, data):
            show.delete(0, "end")
            show.insert(0, data)

        # 'convert' button function
        def remove_ent(ent_box, elim):
            if ent_box.get() == elim:
                ent_box.delete(0, "end")
                ent_box.insert(0, '')
                ent_box.config(fg='black')

        def include_ent(ent_box, elim):
            if ent_box.get() == '':
                ent_box.insert(0, elim)
                ent_box.config(fg='grey')

        # LAT entry
        def focus_in_lat(event):
            remove_ent(lat_ent, 'LAT')

        def focus_out_lat(event):
            include_ent(lat_ent, 'LAT')

        lat_ent = tk.Entry(locbox)
        lat_ent.insert(0, 'LAT')
        lat_ent.bind('<FocusIn>', focus_in_lat)
        lat_ent.bind('<FocusOut>', focus_out_lat)
        lat_ent.config(fg='grey')
        lat_ent.grid(row=3, column=0, columnspan=2, sticky='new')

        # LON entry
        def focus_in_lon(event):
            remove_ent(lon_ent, 'LON')

        def focus_out_lon(event):
            include_ent(lon_ent, 'LON')

        lon_ent = tk.Entry(locbox)
        lon_ent.insert(0, 'LON')
        lon_ent.bind('<FocusIn>', focus_in_lon)
        lon_ent.bind('<FocusOut>', focus_out_lon)
        lon_ent.config(fg='grey')
        lon_ent.grid(row=4, column=0, columnspan=2, sticky='nwe')

        # area in NM
        def focus_in_NM(event):
            remove_ent(nm_ent, 'sqr. NM')

        def focus_out_NM(event):
            include_ent(nm_ent, 'sqr. NM')

        nm_ent = tk.Entry(locbox)
        nm_ent.insert(0, 'sqr. NM')
        nm_ent.bind('<FocusIn>', focus_in_NM)
        nm_ent.bind('<FocusOut>', focus_out_NM)
        nm_ent.config(fg='grey')
        nm_ent.grid(row=5, column=0, sticky='nw')

        # area in Km
        def focus_in_Km(event):
            remove_ent(km_ent, 'sqr. Km')

        def focus_out_Km(event):
            include_ent(km_ent, 'sqr. Km')

        km_ent = tk.Entry(locbox)
        km_ent.insert(0, 'sqr. Km')
        km_ent.bind('<FocusIn>', focus_in_Km)
        km_ent.bind('<FocusOut>', focus_out_Km)
        km_ent.config(fg='grey')
        km_ent.grid(row=5, column=1, sticky='nw')

        # btn box
        btnbox.columnconfigure((0, 1), weight=1)
        btnbox.rowconfigure((0, 1, 2, 3), weight=1)

        def sipher_query(tech, ft, lat, lon, radius, oldest, newest):
            thresh_conv_dd = (1 / 60) * float(radius)
            lat = float(lat)
            lon = float(lon)
            db_check = db.session.query(db.File).count()
            q = db.session.query(db.File.name,
                                 db.File.size,
                                 db.File.tech,
                                 db.File.date,
                                 db.File.data_type,
                                 db.File.root_path). \
                filter(db.or_(db.File.tech == v for v in tech),
                       db.or_(db.File.data_type == v for v in ft),
                       db.File.min_lat <= lat + thresh_conv_dd,
                       db.File.max_lat >= lat - thresh_conv_dd,
                       db.File.min_lon <= lon + thresh_conv_dd,
                       db.File.max_lon >= lon - thresh_conv_dd,
                       db.File.date >= oldest,
                       db.File.date <= newest)
            print(q)
            print(tech)
            q_count = q.count()
            print(q_count)
            if not db_check > 0:
                messagebox.showerror("Error", "Please Add Files to the Database on the Manage Tab")
                return
            if not q_count > 0:
                messagebox.showinfo("Info", "The Given Parameters Yield No Results \n \n Either Parameters are Incorrect \n               or \n Files with listed parameters are not available")
                return
            btn_copy.config(state='normal', relief='raised')
            x = 0
            for row in q:
                row = dict(
                    zip(row.keys(), row))  # after this line is when it needs to add data to the file tree by iteration
                print(row)
                # noinspection PyShadowingNames
                def display_to_sipher(parent, rw):

                    item = rw['root_path']
                    parent.insert('', 'end', item, text=rw['name'])
                    parent.set(item, 'Size', rw['size'])
                    parent.set(item, 'Tech', rw['tech'])
                    parent.set(item, 'Area Data', 'N/A')        # determine if we still want this one
                    parent.set(item, 'Type', rw['data_type'])
                    parent.set(item, 'Year', rw['date'])
                    parent.bind("<Double-1>", link_tree)

                display_to_sipher(tree, row)

                x += 1

        def get_grid():  # gets DD values now
            # TODO: Delete these value inserts on release (for testing only)
            del_then_insert(lat_ent, 34.411965)
            del_then_insert(lon_ent, -103.196675)
            del_then_insert(nm_ent, 10)
            return


        def sipher_btn():
            for i in tree.get_children():
                tree.delete(i)
            tech = {
                'gsm': [bool(gsm_bool.get()), 'GSM'],
                'cdma': [bool(cdma_bool.get()), 'CDMA'],
                'evdo': [bool(cdma_bool.get()), 'EVDO'],
                'umts': [bool(umts_bool.get()), 'WCDMA'],
                'lte': [bool(lte_bool.get()), 'LTE']
            }
            # type
            ftype = {
                'dcode': [bool(dcode_bool.get()), 'DCode'],
                'twr': [bool(tower_bool.get()), 'Tower File'],
                'rns': [bool(rns_bool.get()), 'rns'],
                'csv': [bool(csv_bool.get()), 'csv']
            }
            # time_frame
            time_frame = {
                'newest': latest_var.get(),
                'oldest': earliest_var.get()
            }

            def find_true_dict(dct):
                true_array = []
                for vals in dct:
                    if dct[vals][0] is True:
                        true_array.append(dct[vals][1])
                return true_array

            true_tech = find_true_dict(tech)
            print(true_tech)
            print("True Tech " + str(bool(true_tech)))
            true_ftypes = find_true_dict(ftype)
            if not bool(true_tech) or not bool(true_ftypes):
                messagebox.showinfo("Info",
                                    "The Given Parameters Yield No Results \n \n Either Parameters are Incorrect \n               or \n Files with listed parameters are not available")
                return
            # reset_ents(tree)
            get_grid()  # TODO: remove after testing complete

            sipher_query(true_tech, true_ftypes, lat_ent.get(), lon_ent.get(), nm_ent.get(),            # THIS IS THE SHIT RIGHT HERE
                         time_frame['oldest'], time_frame['newest'])

        btn_sipher = tk.Button(btnbox, text='Sipher', command=sipher_btn, bg=si_color.bg,
                               fg=si_color.fg)                                                          # mk command to use parameters of time, loc, type and find data
        btn_sipher.grid(row=0, column=0, columnspan=2, sticky='nsew')
        btn_sipher.config(width=20)


        def drag_and_drop_prompt():

            files_arr = tree.get_children()
            dest = r"{}\sipher_terminal\database\tmp".format(os.getcwd())
            if os.path.isdir(dest):
                shutil.rmtree(dest)
            if not os.path.isdir(dest):
                os.makedirs(dest)
            for i in files_arr:
                if os.path.isfile(i):
                   shutil.copy(os.path.normpath(i), os.path.normpath(r"{}\{}".format(dest, csvex.path_leaf(i))))
                else:
                    db.session.query(db.File).filter(db.File.root_path == i).delete()
                    db.session.commit()

            os.system("explorer {}".format(str(dest)))


        btn_copy = tk.Button(btnbox, text='Drag And Drop Files', command=drag_and_drop_prompt, bg=si_color.bg, fg=si_color.fg, state='disabled', relief='sunken')
        btn_copy.grid(row=1, column=0, columnspan=2, sticky='nsew')
        btn_copy.config(width=20)

        # noinspection PyShadowingNames
        def reset_ents(parent):
            btn_copy.config(state='disable', relief='sunken')
            arr = [[lat_ent, 'LAT'], [lon_ent, 'LON'], [nm_ent, 'sqr. NM'],
                   [km_ent, 'sqr. Km']]
            for i in arr:
                i[0].delete(0, "end")
                i[0].insert(0, i[1])
                i[0].configure(fg='grey')
            for i in parent.get_children():
                parent.delete(i)


        btn_canx = tk.Button(btnbox, text='Reset', command=lambda: reset_ents(tree), bg=si_color.bg, fg=si_color.fg)
        btn_canx.grid(row=2, column=0, columnspan=2, sticky='nsew')
        btn_canx.config(width=20)

        btn_quit = tk.Button(btnbox, text='Quit', command=lambda: quit(), bg=si_color.bg, fg=si_color.fg)
        btn_quit.grid(row=3, column=0, columnspan=2, sticky='nsew')
        btn_quit.config(width=20)

        # tree view for sipher
        tree = ttk.Treeview(self)
        lbl_arr = ('Tech', 'Type', 'Year', 'Size', 'Area Data')
        tree.config(columns=lbl_arr)

        def link_tree(event):
            input_id = tree.selection()
            y = input_id[0]
            print(y)
            os.system("explorer " + '"' + y + '"')

        for i in lbl_arr:
            tree.column(i, width=75, anchor='w')
            tree.heading(i, text=i)
        tree.column("#0", anchor='w')
        tree.heading("#0", text='File Name')
        vsb = ttk.Scrollbar(tree, orient='vertical', command=tree.yview)
        vsb.pack(side='left', fill='y')
        hsb = ttk.Scrollbar(tree, orient='horizontal', command=tree.xview)
        hsb.pack(side='bottom', fill='x')
        tree.grid(row=3, column=2, columnspan=6, rowspan=7, sticky='nsew')

        # grid description window - SW corner to NE corner in DD
        grid_desc = tk.LabelFrame(locbox, bg=si_color.bg, relief='sunken')
        grid_desc.grid(row=6, column=0, columnspan=2, rowspan=4, sticky='nsew')






# widget constructors

# custom function buttons
class btn(tk.Button):  # add  xpos, ypos,
    def __init__(self, parent, label, command, height, width, state):
        tk.Button.__init__(self, parent, text=label, command=command, activebackground=si_color.abg, bg=si_color.bg,
                           fg=si_color.fg, state=state)
        self.config(width=width, height=height)
        # btn default height in y is 25.


# menu buttons
class action_btn(tk.Button):
    def __init__(self, parent, label, command, height, width, relief):
        tk.Button.__init__(self, parent, text=label, wraplength=80, command=command, bg=si_color.bg, fg=si_color.fg)
        self.config(height=height, width=width, relief=relief)


# custom label
class my_lbl(tk.Label):
    def __init__(self, parent, text):
        tk.Label.__init__(self, parent, text=text, fg=si_color.fg, bg=si_color.bg)


# standard container
class container(tk.LabelFrame):
    def __init__(self, parent, row, col, col_span, row_span):
        tk.LabelFrame.__init__(self, parent, bg=si_color.abg)
        self.grid(row=row, column=col, rowspan=row_span, columnspan=col_span, sticky='nsew')

# standard checkbox
class check_box(tk.Checkbutton):    
    def __init__(self, parent, label, row, col, get_bool, state):
        tk.Checkbutton.__init__(self, parent, text=label, state=state, bg=si_color.abg, variable=get_bool)
        self.get_bool = get_bool
        self.grid(row=row, column=col, sticky='w')
        """self.config(state=state)
        self."""


si = sipher()
if __name__ == '__main__':
    si.mainloop()
