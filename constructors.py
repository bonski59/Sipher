# widget constructors
import tkinter as tk

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
