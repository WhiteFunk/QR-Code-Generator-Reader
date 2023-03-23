from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo, showerror, askyesno
from tkinter import filedialog as fd

from ttkthemes import ThemedStyle
from ttkthemes import ThemedTk

import qrcode
import cv2


        
def generate_qrcode():
    qrcode_data = str(data_entry.get())
    qrcode_name = str(filename_entry.get())
    if qrcode_name == '':
        showerror(title='Error', message='An error occurred' \
                   '\nThe following is ' \
                    'the cause:\n->Empty filename entry field\n' \
                    'Make sure the filename entry field is filled when generating the QRCode')

    else:
        if askyesno(title='Confirmation', message=f'Do you want to create a QRCode with the provided information?'):
            try:
                qr = qrcode.QRCode(version = 1, box_size = 6, border = 4)
                qr.add_data(qrcode_data)
                qr.make(fit = True)
                name = qrcode_name + '.png'
                qrcode_image = qr.make_image(fill_color = 'black', back_color = 'white')
                qrcode_image.save(name)
                global Image
                Image = PhotoImage(file=f'{name}')
                image_label1.config(image=Image)
                reset_button.config(state=NORMAL, command=reset)
        
            except:
                showerror(title='Error', message='Please provide a valid filename')
        
def reset():
    if askyesno(title='Reset', message='Are you sure you want to reset?'):
        image_label1.config(image='')
        reset_button.config(state=DISABLED)
        
        
def open_dialog():
    name = fd.askopenfilename()
    file_entry.delete(0, END)
    file_entry.insert(0, name)


def detect_qrcode():
    
    image_file = file_entry.get()
    if image_file == '':
        showerror(title='Error', message='Please provide a QR Code image file to detect')
    
    else:
        try:
            qr_img = cv2.imread(f'{image_file}')  
            qr_detector = cv2.QRCodeDetector()  
            global qrcode_image
            qrcode_image = PhotoImage(file=f'{image_file}')
            image_label2.config(image=qrcode_image)
            data, pts, st_code = qr_detector.detectAndDecode(qr_img)  
            data_label.config(text=data)
            
        except:
            showerror(title='Error', message='An error occurred while detecting data from the provided file' \
                   '\nThe following could be ' \
                    'the cause:\n->Wrong image file\n' \
                    'Make sure the image file is a valid QRCode')


window = ThemedTk(theme="equilux")
window.title('QR Code Generator-Detector')
window.iconbitmap(window, 'icon.ico')
window.geometry('500x480+440+180')
window.resizable(height=FALSE, width=FALSE)

style = ThemedStyle(window)
style.set_theme("adapta")

tab_control = ttk.Notebook(window)

first_tab = ttk.Frame(tab_control)
second_tab = ttk.Frame(tab_control)

tab_control.add(first_tab, text='QR Code Generator')
tab_control.add(second_tab, text='QR Code Detector')
tab_control.pack(expand=1, fill="both")


first_canvas = Canvas(first_tab, width=500, height=480)

first_canvas.pack()

second_canvas = Canvas(second_tab, width=500, height=480)

second_canvas.pack()


"""Widgets for the first tab"""


image_label1 = Label(window)

first_canvas.create_window(250, 150, window=image_label1)

qrdata_label = ttk.Label(window, text='QRcode Data', style='TLabel')

data_entry = ttk.Entry(window, width=55, style='TEntry')


first_canvas.create_window(70, 330, window=qrdata_label)

first_canvas.create_window(300, 330, window=data_entry)


filename_label = ttk.Label(window, text='Filename', style='TLabel')

filename_entry = ttk.Entry(width=55, style='TEntry')


first_canvas.create_window(84, 360, window=filename_label)

first_canvas.create_window(300, 360, window=filename_entry)



reset_button = ttk.Button(window, text='Reset',  state=DISABLED)

generate_button = ttk.Button(window, text='Generate QRCode',  command=generate_qrcode)


first_canvas.create_window(200, 410, window=reset_button)

first_canvas.create_window(310, 410, window=generate_button)


"""Widgets for the second tab"""


image_label2 = Label(window)

data_label = ttk.Label(window)

second_canvas.create_window(250, 150, window=image_label2)
second_canvas.create_window(250, 300, window=data_label)


browse_button = ttk.Button(window, text='Browse', style='TButton', command=open_dialog)
file_entry = ttk.Entry(window, width=60)

second_canvas.create_window(200, 350, window=file_entry)
second_canvas.create_window(430, 350, window=browse_button)

detect_button = ttk.Button(window, text='Detect QRCode', style='TButton', command=detect_qrcode)
second_canvas.create_window(250, 405,window=detect_button)



window.mainloop()