from tkinter import messagebox
from tkinter import ttk
import sipher_gui_functions as sg
from constructors import *
import time


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


        class Ticker:
            top = tk.Label(self)
            top.place(x=425, y=25)
            mid = tk.Label(self)
            mid.place(x=425, y=50)
            bot = tk.Label(self)
            bot.place(x=425, y=75)

            @classmethod
            def show_string(cls, order, string):
                order.config(text=string)

            @classmethod
            def del_string(cls, order):
                order.config(text='')

            @classmethod
            def info_window(cls, top_str, mid_str, bot_str):
                Ticker.show_string(Ticker.top, top_str)
                Ticker.show_string(Ticker.mid, mid_str)
                Ticker.show_string(Ticker.bot, bot_str)
                self.update_idletasks()
                return

            @classmethod
            def reset_info_window(cls):

                Ticker.show_string(Ticker.top, "")
                Ticker.show_string(Ticker.mid, "")
                Ticker.show_string(Ticker.bot, "")
                self.update()
                self.update_idletasks()
                return




        def update_ticker(numerator, denominator):
            display_count = "({} of {}) files to load".format(str(numerator), str(denominator))
            display_percent = "%{} Loaded".format(str(round((numerator / denominator) * 100, 2)))
            return display_percent, display_count


        # Ticker.get_text_top(Ticker.top, "dope")


        def display_to_ft(parent):
            Ticker.info_window("", "", "Finding Files . . .")
            self.update()
            count = 0

            file_arr = sg.add_data()

            percent, my_count = update_ticker(count, len(file_arr))
            Ticker.info_window(my_count, percent, "Standby . . .")

            for file in file_arr:
                item = str(file)
                b_arr = sg.file_breakdown(file)
                parent.insert('', 'end', item, text=str(b_arr[1]))
                parent.set(item, 'Size', str(b_arr[2]))
                parent.set(item, 'Tech', str(b_arr[3]))
                count += 1
                percent, my_count = update_ticker(count, len(file_arr))
                Ticker.info_window(my_count, percent, "Standby . . .")

            Ticker.show_string(Ticker.bot, "All Files Ready for Database")
            # done_loading()

        # top row buttons
        def add_svy_data():
            Ticker.reset_info_window()
            display_to_ft(tree)
            load.config(state='normal')
            clear.config(state='normal')

        action_btn(self, 'Add Survey Data', lambda: add_svy_data(), 5, 27, 'groove').place(y=27)
        action_btn(self, 'Manage Database', sg.manage_db, 5, 27, 'groove').place(x=200, y=27)

        # action_btn(self, 'Settings', sg.do_nothing, 5, 27, 'groove').place(x=400, y=27)

        # bottom row buttons
        def clr_selection():
            Ticker.reset_info_window()
            for child in tree.get_children():
                tree.delete(child)
            load.config(state='disabled')
            clear.config(state='disabled')

        def add_to_db():
            Ticker.reset_info_window()
            children = tree.get_children()
            children_count = len(children)
            count = 0
            for child in children:
                def show():
                    files_added = "{} of {} added to database".format(count, children_count)
                    added_percent = "%{} completion".format(str(round((count / children_count) * 100, 2)))
                    Ticker.info_window(files_added, added_percent, "Standby . . .")
                try:
                    sg.send_to_sipher_db(child)
                    print(str(child) + "  added to DB")
                except NameError:  # user most likely pressed "Load to Database" Button without selecting Files first
                    messagebox.showerror("Error", "Please Select Files to load")
                    return
                count += 1
                show()
            Ticker.show_string(Ticker.bot, "Complete")

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
