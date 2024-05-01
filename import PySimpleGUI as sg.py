from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter.messagebox import showerror, askyesno
from tkinter import colorchooser
from PIL import ImageOps, ImageFilter, ImageGrab
from PIL import Image, ImageTk
import math;

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
drawings=[]
def image_flip():
    try:
        global image, photo_image, rotation_angle, drawings
        # Открываем изображение и поворачиваем его
        image = Image.open(filepath)
        image = image.resize((Width, Height), Image.LANCZOS)
        rotated_image = image.rotate(rotation_angle + 90)
        rotation_angle += 90
        # Сбрасываем изображение, если угол поворота кратен 360 градусам
        if rotation_angle % 360 == 0:
            rotation_angle = 0
            rotated_image = image
        # Конвертируем PIL изображение в объект ImageTk.PhotoImage и отображаем его на холсте
        photo_image = ImageTk.PhotoImage(rotated_image)
        working_space.delete("all")  # Удаляем все объекты на холсте

        # Создаем изображение на холсте
        working_space.create_image(0, 0, anchor="nw", image=photo_image)

        # Перерисовываем все рисунки на холсте с новыми координатами и размерами
        for drawing in drawings:
            x1, y1, x2, y2 = drawing
            # Координаты рисунка относительно центра холста
            x_center, y_center = (x1 + x2) / 2 - Width / 2, (y1 + y2) / 2 - Height / 2
            # Поворачиваем координаты рисунка
            new_x_center = x_center * math.cos(math.radians(rotation_angle)) - y_center * math.sin(math.radians(rotation_angle))
            new_y_center = x_center * math.sin(math.radians(rotation_angle)) + y_center * math.cos(math.radians(rotation_angle))
            # Масштабируем координаты рисунка относительно нового размера изображения
            new_x1, new_y1 = new_x_center + Width / 2 - (x2 - x1) / 2, new_y_center + Height / 2 - (y2 - y1) / 2
            new_x2, new_y2 = new_x_center + Width / 2 + (x2 - x1) / 2, new_y_center + Height / 2 + (y2 - y1) / 2
            # Создаем овал с новыми координатами
            working_space.create_oval(new_x1, new_y1, new_x2, new_y2, fill=pen_color, outline="", width=pen_size, tags="oval")

    except:
        showerror(title='Ошибка переворачивания', message='Выберите картинку для переворачивания')

pen_size=3
pen_color="red"
draw_enabled = False  # Переменная для отслеживания состояния рисования

def draw(event):
    global filepath, draw_enabled, drawings;
    if filepath and draw_enabled:  # Рисовать только если filepath определен и режим рисования включен
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

Width=1100
Height=700
working_space = Canvas(window, width=Width, height=Height)
working_space.pack()
down_frame=Frame(window, background="blue", width=1100, height=100)
down_frame.pack(fill='both')
working_space.bind("<B1-Motion>", draw)

image_open_icon=PhotoImage(file = "open_im.png").subsample(12, 12)
button_open_image = Button(down_frame, image=image_open_icon, height=50, width=50, command=open_image)
button_open_image.pack( side= "left",pady=5)

image_flip_icon=PhotoImage(file="free-icon-inverted-man-posture-with-head-down-on-floor-46678.png").subsample(12, 12)
button_flip_image=Button(down_frame, image=image_flip_icon, height=50, width=50, command=image_flip)
button_flip_image.pack(side="left",pady=5)

image_draw=PhotoImage(file = "pensil.png").subsample(12, 12)
button_draw = Button(down_frame, image=image_draw, height=50, width=50, command=toggle_draw)
button_draw.pack( side= "left",pady=5)

image_color=PhotoImage(file="palette.png").subsample(12, 12)
button_color = Button(down_frame, image=image_color, height=50, width=50, command=change_color)
button_color.pack(side="left", pady=5)

window.mainloop()