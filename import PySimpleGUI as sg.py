from tkinter import *
from tkinter import filedialog, colorchooser
from tkinter.messagebox import showerror, askyesno
from PIL import Image, ImageTk, ImageGrab, ImageFilter, ImageOps
import math
from tkinter import ttk

window = Tk()
window.title("Редактор фотографий")
window.geometry('1200x800')
window.iconbitmap('rabbit.ico')

def open_image():
    global filepath, image, drawings, rotation_angle, is_flipped

    filepath = filedialog.askopenfilename(title="Open Image File", 
                                          filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.gif;*.bmp")])
    if filepath:
        image = Image.open(filepath)
        image = image.resize((Width, Height), Image.LANCZOS)
        image = ImageTk.PhotoImage(image)
        working_space.create_image(0, 0, anchor="nw", image=image)

    drawings=[]
    rotation_angle=0
    is_flipped = False

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

        filtered_image(filter_for_image.get())
    except:
        showerror(title='Ошибка переворачивания', message='Выберите картинку для переворачивания')

    for drawing in drawings:
        x1, y1, x2, y2 = drawing
        x_center, y_center = (x1 + x2) / 2 - Width / 2, (y1 + y2) / 2 - Height / 2
        new_x_center = x_center * math.cos(math.radians(rotation_angle)) - y_center * math.sin(math.radians(rotation_angle + 180))
        new_y_center = x_center * math.sin(math.radians(rotation_angle + 180)) + y_center * math.cos(math.radians(rotation_angle))
        new_x1, new_y1 = new_x_center + Width / 2 - (x2 - x1) / 2, new_y_center + Height / 2 - (y2 - y1) / 2
        new_x2, new_y2 = new_x_center + Width / 2 + (x2 - x1) / 2, new_y_center + Height / 2 + (y2 - y1) / 2
        working_space.create_oval(new_x1, new_y1, new_x2, new_y2, 
                                  fill=pen_color, 
                                  outline="", 
                                  width=pen_size, 
                                  tags="drawing")

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
        working_space.create_oval(x1, y1, x2, y2, 
                                  fill=pen_color, 
                                  outline="", 
                                  width=pen_size, 
                                  tags="drawing")

def toggle_draw():
    global draw_enabled
    draw_enabled = not draw_enabled

def change_color():
    global pen_color
    pen_color = colorchooser.askcolor(title="Выберите цвет ручки")[1]

is_flipped = False

def photo_mirror():
    global image, photo_image, is_flipped,rotation_angle, drawings

    if is_flipped == True:
        angle = 180
    else:
        angle = 0

    try:
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

        filtered_image(filter_for_image.get())

        for drawing in drawings:
            x1, y1, x2, y2 = drawing
            x_center, y_center = (x1 + x2) / 2 - Width / 2, (y1 + y2) / 2 - Height / 2
            new_x_center = x_center * math.cos(math.radians(angle)) - y_center * math.sin(math.radians(angle))
            new_y_center = x_center * math.sin(math.radians(0)) + y_center * math.cos(math.radians(0))
            new_x1, new_y1 = new_x_center + Width / 2 - (x2 - x1) / 2, new_y_center + Height / 2 - (y2 - y1) / 2
            new_x2, new_y2 = new_x_center + Width / 2 + (x2 - x1) / 2, new_y_center + Height / 2 + (y2 - y1) / 2
            working_space.create_oval(new_x1, new_y1, new_x2, new_y2, 
                                      fill=pen_color, 
                                      outline="", 
                                      width=pen_size, 
                                      tags="drawing")
    except:
        showerror(title='Нельзя отзеркалить', message='Выберите фотографию для отзеркаливания!')

def thin_size():
    global pen_size
    pen_size = 1
    choice_size.destroy()

def middle_size():
    global pen_size
    pen_size = 3
    choice_size.destroy()

def bold_size():
    global pen_size
    pen_size = 5
    choice_size.destroy()

def change_pen_size():
    global choice_size, button_thin, button_middle, button_bold

    choice_size = Toplevel()
    choice_size.title("Выберите толщину линии")
    choice_size.geometry("400x200")

    image_thin_line = PhotoImage(file="thin.png").subsample(12, 12)
    button_thin=Button(choice_size,
                       image=image_thin_line, 
                       height=50, width=50, 
                       command=thin_size)
    button_thin.image =image_thin_line
    button_thin.pack(anchor=CENTER, expand=1)
    
    image_middle_line = PhotoImage(file="middle.png").subsample(12, 12)
    button_middle=Button(choice_size,
                         image=image_middle_line, 
                         height=50, width=50, 
                         command=middle_size)
    button_middle.image =image_middle_line
    button_middle.pack(anchor=CENTER, expand=1)

    image_bold_line = PhotoImage(file="bold.png").subsample(12, 12)
    button_bold=Button(choice_size,
                       image=image_bold_line, 
                       height=50, 
                       width=50, 
                       command=bold_size)
    button_bold.image =image_bold_line
    button_bold.pack(anchor=CENTER, expand=1)

def eraser():
    global drawings
    working_space.delete("oval")
    drawings=[]

def save_image():
    global is_flipped, rotation_angle, filepath

    if filepath:
        image_for_save = ImageGrab.grab(bbox=(working_space.winfo_rootx(), 
                                              working_space.winfo_rooty(), 
                                              working_space.winfo_rootx() + working_space.winfo_width(),
                                              working_space.winfo_rooty() + working_space.winfo_height()))
        if is_flipped or rotation_angle % 360 != 0:

            image_for_save = image_for_save.resize((Width, Height), Image.LANCZOS)

            if is_flipped:
                image_for_save = image_for_save.transpose(Image.FLIP_LEFT_RIGHT)

            if rotation_angle % 360 != 0:
                image_for_save = image_for_save.rotate(rotation_angle)

            filepath = filepath.split(".")[0] + "_mod.jpg"

        filepath = filedialog.asksaveasfilename(defaultextension=".jpg")

        if filepath:

            if askyesno(title='Сохранение фотографии', message='Вы хотите сохранить фотографию?'):
                image_for_save.save(filepath)

def filtered_image(filter):
    global rotation_angle, is_flipped, filepath, photo_image

    try:
        if is_flipped == True:
            copied_image = Image.open(filepath).transpose(Image.FLIP_LEFT_RIGHT)
            copied_image = copied_image.rotate(rotation_angle)

            if filter == "Черно белый":
                copied_image = ImageOps.grayscale(copied_image)
            elif filter == "Размытость":
                copied_image = copied_image.filter(ImageFilter.BLUR)
            elif filter == "Контур":
                copied_image = copied_image.filter(ImageFilter.CONTOUR)
            elif filter == "Детализация":
                copied_image = copied_image.filter(ImageFilter.DETAIL)
            elif filter == "Усиление кромки":
                copied_image = copied_image.filter(ImageFilter.EDGE_ENHANCE)
            elif filter == "Тиснение":
                copied_image = copied_image.filter(ImageFilter.EMBOSS)
            elif filter == "Обострение":
                copied_image = copied_image.filter(ImageFilter.SHARPEN)
            elif filter == "Гладкость":
                copied_image = copied_image.filter(ImageFilter.SMOOTH)
        else:
            copied_image = Image.open(filepath)
            copied_image = copied_image.rotate(rotation_angle)

            if filter == "Черно белый":
                copied_image = ImageOps.grayscale(copied_image)
            elif filter == "Размытость":
                copied_image = copied_image.filter(ImageFilter.BLUR)
            elif filter == "Контур":
                copied_image = copied_image.filter(ImageFilter.CONTOUR)
            elif filter == "Детализация":
                copied_image = copied_image.filter(ImageFilter.DETAIL)
            elif filter == "Усиление кромки":
                copied_image = copied_image.filter(ImageFilter.EDGE_ENHANCE)
            elif filter == "Тиснение":
                copied_image = copied_image.filter(ImageFilter.EMBOSS)
            elif filter == "Обострение":
                copied_image = copied_image.filter(ImageFilter.SHARPEN)
            elif filter == "Гладкость":
                copied_image = copied_image.filter(ImageFilter.SMOOTH)

        for drawing in drawings:
            x1, y1, x2, y2 = drawing
            working_space.create_oval(x1, y1, x2, y2, 
                                      fill=pen_color, 
                                      outline="", 
                                      width=pen_size, 
                                      tags="drawing")
    except:
        showerror(title='Ошибка', message='Невозможно применить фильтр')

    copied_image = copied_image.resize((Width, Height), Image.LANCZOS)
    photo_image = ImageTk.PhotoImage(copied_image)
    working_space.create_image(0, 0, anchor="nw", image=photo_image)

Width = 1100
Height = 700
working_space = Canvas(window, width=Width, height=Height)
working_space.grid(row=0, column=0, columnspan=4)
down_frame = Frame(window, background="light blue", width=1100, height=100)
down_frame.grid(row=1, column=0, columnspan=4)

working_space.bind("<B1-Motion>", draw)

def selected(event):
    selection = filter_for_image.get()
    print(selection)

filters = ["Черно белый", "Размытость", "Контур", "Детализация", "Усиление кромки", "Тиснение", "Обострение", "Гладкость"]
filter_for_image = ttk.Combobox(down_frame, values=filters, width=18, textvariable=StringVar(value=filters[0]))
filter_for_image.grid(row=0, column=0)
filter_for_image.set("Выберите фильтр")
filter_for_image.bind("<<ComboboxSelected>>", lambda event: filtered_image(filter_for_image.get()))

image_open_icon = PhotoImage(file="open_im.png").subsample(12, 12)
button_open_image = Button(down_frame, 
                           image=image_open_icon, 
                           height=50, width=50, 
                           command=open_image)
button_open_image.grid(row=0, column=1, padx=(10, 10))

image_flip_icon = PhotoImage(file="rotate.png").subsample(12, 12)
button_flip_image = Button(down_frame, 
                           image=image_flip_icon, 
                           height=50, width=50, 
                           command=image_flip)
button_flip_image.grid(row=0, column=2, padx=(10, 10))

image_draw = PhotoImage(file="pensil.png").subsample(12, 12)
button_draw = Button(down_frame, 
                     image=image_draw, 
                     height=50, width=50, 
                     command=toggle_draw)
button_draw.grid(row=0, column=4, padx=(10, 10))

image_color = PhotoImage(file="palette.png").subsample(12, 12)
button_color = Button(down_frame, 
                      image=image_color, 
                      height=50, width=50, 
                      command=change_color)
button_color.grid(row=0, column=5, padx=(10, 10))

image_mirror = PhotoImage(file="mirror.png").subsample(12, 12)
button_mirror = Button(down_frame, 
                       image=image_mirror, 
                       height=50, width=50, 
                       command=photo_mirror)
button_mirror.grid(row=0, column=3, padx=(10, 10))

image_pen_size = PhotoImage(file="pen_size.png").subsample(12, 12)
button_change_size = Button(down_frame, 
                            image=image_pen_size, 
                            height=50, width=50, 
                            command=change_pen_size)
button_change_size.grid(row=0, column=6, padx=(10, 10))

image_eraser = PhotoImage(file="eraser.png").subsample(12, 12)
button_eraser = Button(down_frame, 
                       image=image_eraser, 
                       height=50, width=50, 
                       command=eraser)
button_eraser.grid(row=0, column=7, padx=(10, 10))

image_save = PhotoImage(file="save.png").subsample(12, 12)
button_save_image = Button(down_frame, 
                           image=image_save, 
                           height=50, width=50, 
                           command=save_image)
button_save_image.grid(row=0, column=8, padx=(10, 10))

window.mainloop()
