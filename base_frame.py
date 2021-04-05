from constructors import *
from page_one import PageOne
from page_two import PageTwo


class BaseFrame(tk.Tk):
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

        for F in (PageOne, PageTwo):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nesw")
            frame.config(bg=si_color.bg)

        self.show_frame(PageTwo)  # TODO: to page one for init

    def show_frame(self, context):
        frame = self.frames[context]
        frame.tkraise()
        return

    def show_one(self):
        self.show_frame(PageOne)
        return

    def show_two(self):
        self.show_frame(PageTwo)
        return
