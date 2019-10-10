import tkinter
import rsa
from tkinter import filedialog
from tkinter import messagebox


class KeyInputBlock:
    file_path = ''

    def __init__(self, tk, label_text, file_format):
        self.input_frame = tkinter.Frame(master=tk, bg="#f5f5f5", bd=2)
        self.input_label = tkinter.Label(master=self.input_frame, text=label_text, justify=tkinter.CENTER, bd=2)
        self.input_entry = tkinter.Entry(master=self.input_frame, justify=tkinter.LEFT, bd=2)
        self.input_button = tkinter.Button(master=self.input_frame, width=5, text='...', command=self.__get_key_path)
        self.file_format = file_format

    def draw_interface(self, col):
        self.input_frame.grid(column=col, row=0, sticky="WESN")
        self.input_label.grid(column=0, row=0, sticky="WESN")
        self.input_entry.grid(column=1, row=0, sticky="WESN")
        self.input_button.grid(column=2, row=0, sticky="WESN")

        self.input_frame.columnconfigure(1, weight=1)

    def __get_key_path(self):
        f_path = filedialog.askopenfilename()
        f_format = f_path.split('/')[-1].split('.')[-1]

        if f_format == self.file_format:
            self.file_path = f_path
            self.input_entry.delete(0, tkinter.END)
            self.input_entry.insert(0, self.file_path)
        else:
            messagebox.showinfo("Invalid file format", f"The file must has '.{self.file_format}' format")

    def get_key(self):
        key = None
        if self.file_path:
            with open(self.file_path, "rb") as file:
                key = file.read()
        return key


class TextBlock:

    def __init__(self, tk, button_text, func):
        self.text_frame = tkinter.Frame(master=tk, bg="#f5f5f5", bd=2)
        self.input_text = tkinter.Text(master=self.text_frame)
        self.button = tkinter.Button(master=self.text_frame, text=button_text, command=func)
        self.output_text = tkinter.Text(master=self.text_frame)

    def draw_interface(self, col):
        self.text_frame.grid(column=col, row=1, sticky="WESN")
        self.input_text.grid(column=0, row=0, sticky="WESN")
        self.button.grid(column=0, row=1, sticky="WESN")
        self.output_text.grid(column=0, row=2, sticky="WESN")

        self.text_frame.columnconfigure(0, weight=1)
        self.text_frame.rowconfigure(0, weight=1)
        self.text_frame.rowconfigure(2, weight=1)


class Application(tkinter.Tk):

    def __init__(self):
        super().__init__()

        self.configure(background='#f5f5f5')
        self.geometry("{0}x{1}+0+0".format(int(self.winfo_screenwidth() * 0.99), int(self.winfo_screenheight() * 0.9)))
        self.bind('<Escape>', lambda e: self.destroy())

        self.title("Text encryption")
        self.iconbitmap('img/lock.ico')

        self.public_key_block = KeyInputBlock(self, 'Public key', 'pub')
        self.private_key_block = KeyInputBlock(self, 'Private key', 'prv')
        self.encrypt_text = TextBlock(self, 'Encrypt', self.__encrypt)
        self.decrypt_text = TextBlock(self,  'Load data & Decrypt', self.__decrypt)

    def draw_interface(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)

        self.public_key_block.draw_interface(0)
        self.private_key_block.draw_interface(1)
        self.encrypt_text.draw_interface(0)
        self.decrypt_text.draw_interface(1)

    @staticmethod
    def save_data(data):
        with open("output.txt", "wb") as file:
            file.write(data)

    def open_data(self):
        with open("output.txt", "rb") as file:
            data = file.read()
        self.decrypt_text.input_text.insert(tkinter.END, data)

        return data

    def __encrypt(self):
        self.encrypt_text.output_text.delete(1.0, tkinter.END)
        file_key = self.public_key_block.get_key()
        if file_key:
            key = rsa.PublicKey.load_pkcs1(file_key)
            message = self.encrypt_text.input_text.get(1.0, 'end-1c').encode('utf-8')
            crypto = rsa.encrypt(message, key)
            self.save_data(crypto)
            self.encrypt_text.output_text.insert(tkinter.END, crypto)
        else:
            messagebox.showinfo("Error", "Input the path to the public key")

    def __decrypt(self):
        file_key = self.private_key_block.get_key()
        if file_key:
            self.decrypt_text.output_text.delete(1.0, tkinter.END)
            self.decrypt_text.input_text.delete(1.0, tkinter.END)
            key = rsa.PrivateKey.load_pkcs1(file_key)
            self.decrypt_text.output_text.insert(tkinter.END, rsa.decrypt(self.open_data(), key))
        else:
            messagebox.showinfo("Error", "Input the path to the private key")


if __name__ == '__main__':
    app = Application()
    app.draw_interface()
    app.mainloop()
