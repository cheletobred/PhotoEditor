from tkinter import *
from tkinter import filedialog, colorchooser
from tkinter.messagebox import showerror
from PIL import Image, ImageTk
import math

window = Tk()
window.title("Редактор фотографий")
window.geometry('1200x800')
window.iconbitmap('rabbit.ico')

def open_image():
    global filepath, image
    filepath = filedialog.askopenfilename(title="Open Image File", filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.gif;*.bmp")])
    if filepath:
        image = Image.open(filepath)
        image = image.resize((Width, Height), Image.LANCZOS)
        image = ImageTk.PhotoImage(image)
        working_space.create_image(0, 0, anchor="nw", image=image)
    drawings=[]

rotation_angle = 0
drawings = []

def image_flip():
    try:
        global image, photo_image, rotation_angle, drawings
        image = Image.open(filepath)
        rotated_image = image.rotate(rotation_angle + 90)
        rotation_angle += 90
        if rotation_angle % 360 == 0:
            rotation_angle = 0
            rotated_image = image
        rotated_image = rotated_image.resize((Width, Height), Image.LANCZOS)
        photo_image = ImageTk.PhotoImage(rotated_image)
        working_space.delete("all")
        working_space.create_image(0, 0, anchor="nw", image=photo_image)
        for drawing in drawings:
            x1, y1, x2, y2 = drawing
            x_center, y_center = (x1 + x2) / 2 - Width / 2, (y1 + y2) / 2 - Height / 2
            new_x_center = x_center * math.cos(math.radians(rotation_angle)) - y_center * math.sin(math.radians(rotation_angle + 180))
            new_y_center = x_center * math.sin(math.radians(rotation_angle + 180)) + y_center * math.cos(math.radians(rotation_angle))
            new_x1, new_y1 = new_x_center + Width / 2 - (x2 - x1) / 2, new_y_center + Height / 2 - (y2 - y1) / 2
            new_x2, new_y2 = new_x_center + Width / 2 + (x2 - x1) / 2, new_y_center + Height / 2 + (y2 - y1) / 2
            working_space.create_oval(new_x1, new_y1, new_x2, new_y2, fill=pen_color, outline="", width=pen_size, tags="oval")
    except:
        showerror(title='Ошибка переворачивания', message='Выберите картинку для переворачивания')

pen_size = 3
pen_color = "black"
draw_enabled = False

def draw(event):
    global filepath, draw_enabled, drawings
    if filepath and draw_enabled:
        x1, y1 = (event.x - pen_size), (event.y - pen_size)
        x2, y2 = (event.x + pen_size), (event.y + pen_size)
        drawing_coords = (x1, y1, x2, y2)
        drawings.append(drawing_coords)
        working_space.create_oval(x1, y1, x2, y2, fill=pen_color, outline="", width=pen_size, tags="oval")

def toggle_draw():
    global draw_enabled
    draw_enabled = not draw_enabled

def change_color():
    global pen_color
    pen_color = colorchooser.askcolor(title="Select Pen Color")[1]

is_flipped = False

def photo_mirror():
    try:
        global image, photo_image, is_flipped
        if not is_flipped:
            image = Image.open(filepath).transpose(Image.FLIP_LEFT_RIGHT)
            is_flipped = True
        else:
            image = Image.open(filepath)
            is_flipped = False
        image = image.resize((Width, Height), Image.LANCZOS)
        photo_image = ImageTk.PhotoImage(image)
        working_space.create_image(0, 0, anchor="nw", image=photo_image)
        working_space.delete("all")
        working_space.create_image(0, 0, anchor="nw", image=photo_image)
        if is_flipped == True:
            angle = 180
        else:
            angle = 0
        for drawing in drawings:
            x1, y1, x2, y2 = drawing
            x_center, y_center = (x1 + x2) / 2 - Width / 2, (y1 + y2) / 2 - Height / 2
            new_x_center = x_center * math.cos(math.radians(angle)) - y_center * math.sin(math.radians(angle))
            new_y_center = x_center * math.sin(math.radians(0)) + y_center * math.cos(math.radians(0))
            new_x1, new_y1 = new_x_center + Width / 2 - (x2 - x1) / 2, new_y_center + Height / 2 - (y2 - y1) / 2
            new_x2, new_y2 = new_x_center + Width / 2 + (x2 - x1) / 2, new_y_center + Height / 2 + (y2 - y1) / 2
            working_space.create_oval(new_x1, new_y1, new_x2, new_y2, fill=pen_color, outline="", width=pen_size, tags="oval")

    except:
        showerror(title='Нельзя отзеркалить', message='Выберите фотографию для отзеркаливания!')

Width = 1100
Height = 700
working_space = Canvas(window, width=Width, height=Height)
working_space.grid(row=0, column=0, columnspan=4)

down_frame = Frame(window, background="light blue", width=1100, height=100)
down_frame.grid(row=1, column=0, columnspan=4)

working_space.bind("<B1-Motion>", draw)

image_open_icon = PhotoImage(file="open_im.png").subsample(12, 12)
button_open_image = Button(down_frame, image=image_open_icon, height=50, width=50, command=open_image)
button_open_image.grid(row=0, column=0, padx=(10, 10))

image_flip_icon = PhotoImage(file="rotate.png").subsample(12, 12)
button_flip_image = Button(down_frame, image=image_flip_icon, height=50, width=50, command=image_flip)
button_flip_image.grid(row=0, column=1, padx=(10, 10))

image_draw = PhotoImage(file="pensil.png").subsample(12, 12)
button_draw = Button(down_frame, image=image_draw, height=50, width=50, command=toggle_draw)
button_draw.grid(row=0, column=2, padx=(10, 10))

image_color = PhotoImage(file="palette.png").subsample(12, 12)
button_color = Button(down_frame, image=image_color, height=50, width=50, command=change_color)
button_color.grid(row=0, column=3, padx=(10, 10))

image_mirror = PhotoImage(file="mirror.png").subsample(12, 12)
button_mirror = Button(down_frame, image=image_mirror, height=50, width=50, command=photo_mirror)
button_mirror.grid(row=0, column=5, padx=(10, 10))

window.mainloop()
