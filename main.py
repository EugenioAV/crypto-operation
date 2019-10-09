import tkinter


class KeyInputBlock:

    def __init__(self, tk, label_text):
        self.input_frame = tkinter.Frame(master=tk, bg="#f5f5f5", bd=2)
        self.input_label = tkinter.Label(master=self.input_frame, text=label_text, justify=tkinter.CENTER, bd=2)
        self.input_entry = tkinter.Entry(master=self.input_frame, justify=tkinter.RIGHT, bd=2)
        self.input_button = tkinter.Button(master=self.input_frame, width=5, text='...', command=self.open_key)

    def draw_interface(self, col):
        self.input_frame.grid(column=col, row=0, sticky="WESN")
        self.input_label.grid(column=0, row=0, sticky="WESN")
        self.input_entry.grid(column=1, row=0, sticky="WESN")
        self.input_button.grid(column=2, row=0, sticky="WESN")

        self.input_frame.columnconfigure(1, weight=1)

    def open_key(self):
        pass


class Application(tkinter.Tk):

    def __init__(self):
        super().__init__()

        self.configure(background='#f5f5f5')
        self.geometry("{0}x{1}+0+0".format(int(self.winfo_screenwidth() * 0.99), int(self.winfo_screenheight() * 0.9)))
        self.bind('<Escape>', lambda e: self.destroy())

        self.title("Text encryption")
        self.iconbitmap('img/lock.ico')

        self.public_key_block = KeyInputBlock(self, 'Public key')
        self.private_key_block = KeyInputBlock(self, 'Private key')

    def draw_interface(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self.public_key_block.draw_interface(0)
        self.private_key_block.draw_interface(1)


if __name__ == '__main__':
    app = Application()
    app.draw_interface()
    app.mainloop()
