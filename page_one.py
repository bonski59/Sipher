from tkinter import messagebox
from tkinter import ttk
import sipher_gui_functions as sg
from constructors import *


class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # phony button
        label = my_lbl(self, text=tab.manage)
        label.place(x=0)
        label.config(width=27)

        # nav buttons
        btn(self, tab.sipher, lambda: controller.show_two(), 0, 27, 'normal').place(x=200)

        # TODO get this mf a mf loading bar !!!!!!!!!!

        def display_to_ft(parent):
            self.update()

            file_arr = sg.add_data()
            self.update_idletasks()
            for file in file_arr:
                item = str(file)
                b_arr = sg.file_breakdown(file)
                parent.insert('', 'end', item, text=str(b_arr[1]))
                parent.set(item, 'Size', str(b_arr[2]))
                parent.set(item, 'Tech', str(b_arr[3]))

            # done_loading()

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
