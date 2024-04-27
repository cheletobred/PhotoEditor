from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter.messagebox import showerror, askyesno
from tkinter import colorchooser
from PIL import ImageOps, ImageFilter, ImageGrab
from PIL import Image, ImageTk

window = Tk()
window.title("Редактор фотографий")
window.geometry('1200x800')
window.iconbitmap('rabbit.ico')

def open_image():
    global filepath
    filepath = filedialog.askopenfilename(title="Open Image File", filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.gif;*.bmp")])
    if filepath:
        global image
        image = Image.open(filepath)
        image = image.resize((Width, Height), Image.LANCZOS)
            
        image = ImageTk.PhotoImage(image)
        working_space.create_image(0, 0, anchor="nw", image=image)

rotation_angle=0
def image_flip():
    try:
        global image, photo_image, rotation_angle
        
        image = Image.open(filepath)
        new_image = image.rotate(rotation_angle + 90)
        rotation_angle += 90
        if rotation_angle % 360 == 0:
            rotation_angle = 0
            image = Image.open(filepath)
            image = image.resize((Width, Height), Image.LANCZOS)
            new_image = image
        photo_image = ImageTk.PhotoImage(new_image)
        working_space.create_image(0, 0, anchor="nw", image=photo_image)
    except:
        showerror(title='Ошибка переворачивания', message='Выберите картинку для переворачивания')

Width=1100
Height=700
working_space = Canvas(window, width=Width, height=Height)
working_space.pack()
down_frame=Frame(window, background="blue", width=1100, height=100)
down_frame.pack(fill='both')

image_open_icon=PhotoImage(file = "free-icon-photos-4618132.png").subsample(12, 12)
button_open_image = Button(down_frame, image=image_open_icon, height=50, width=50, command=open_image)
button_open_image.pack( side= "left",pady=5)

image_flip_icon=PhotoImage(file="free-icon-inverted-man-posture-with-head-down-on-floor-46678.png").subsample(12, 12)
button_flip_image=Button(down_frame, image=image_flip_icon, height=50, width=50, command=image_flip)
button_flip_image.pack(side="left",pady=5)

window.mainloop()