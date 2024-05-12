import tkinter as tk
from tkinter import filedialog, colorchooser, ttk
from tkinter.messagebox import showerror, askyesno
from PIL import Image, ImageTk, ImageGrab, ImageFilter, ImageOps
import math
from tkinter import ttk

class PhotoEditorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Редактор фотографий")
        self.geometry('1200x800')
        self.iconbitmap('rabbit.ico')

        self.Width = 1100
        self.Height = 700

        self.pen_size = 3
        self.pen_color = "black"
        self.draw_enabled = False
        self.is_flipped = False

        self.create_widgets()

    def create_widgets(self):
        self.working_space = tk.Canvas(self, width=self.Width, height=self.Height)
        self.working_space.grid(row=0, column=0, columnspan=4)
        self.down_frame = tk.Frame(self, background="light blue", width=self.Width, height=100)
        self.down_frame.grid(row=1, column=0, columnspan=4)

        self.draw_enabled = False
        self.drawings = []
        self.rotation_angle = 0
        self.is_flipped = False
        self.pen_size = 3
        self.pen_color = "black"

        self.working_space.bind("<B1-Motion>", self.draw)

        self.filter = ["Черно белый", "Размытость", "Контур", "Детализация", "Усиление кромки", "Тиснение", "Обострение", "Гладкость"]
        self.filter_for_image = ttk.Combobox(self.down_frame, values=self.filter, width=18)
        self.filter_for_image.grid(row=0, column=0)
        self.filter_for_image.set("Выберите фильтр")
        self.filter_for_image.bind("<<ComboboxSelected>>", lambda event : self.filtered_image(self.filter_for_image.get()))

        self.image_open_icon = tk.PhotoImage(file="open_im.png").subsample(12, 12)
        self.button_open_image = tk.Button(self.down_frame, image=self.image_open_icon, height=50, width=50, command=self.open_image)
        self.button_open_image.grid(row=0, column=1, padx=(10, 10))

        self.image_flip_icon = tk.PhotoImage(file="rotate.png").subsample(12, 12)
        self.button_flip_image = tk.Button(self.down_frame, 
                                image=self.image_flip_icon, 
                                height=50, width=50, 
                                command=self.image_flip)
        self.button_flip_image.grid(row=0, column=2, padx=(10, 10))

        self.image_draw = tk.PhotoImage(file="pensil.png").subsample(12, 12)
        self.button_draw = tk.Button(self.down_frame, 
                            image=self.image_draw, 
                            height=50, width=50, 
                            command=self.toggle_draw)
        self.button_draw.grid(row=0, column=4, padx=(10, 10))

        self.image_color = tk.PhotoImage(file="palette.png").subsample(12, 12)
        self.button_color = tk.Button(self.down_frame, 
                            image=self.image_color, 
                            height=50, width=50, 
                            command=self.change_color)
        self.button_color.grid(row=0, column=5, padx=(10, 10))

        self.image_mirror = tk.PhotoImage(file="mirror.png").subsample(12, 12)
        self.button_mirror = tk.Button(self.down_frame, 
                            image=self.image_mirror, 
                            height=50, width=50, 
                            command=self.photo_mirror)
        self.button_mirror.grid(row=0, column=3, padx=(10, 10))

        self.image_pen_size = tk.PhotoImage(file="pen_size.png").subsample(12, 12)
        self.button_change_size = tk.Button(self.down_frame, 
                                    image=self.image_pen_size, 
                                    height=50, width=50, 
                                    command=self.change_pen_size)
        self.button_change_size.grid(row=0, column=6, padx=(10, 10))

        self.image_eraser = tk.PhotoImage(file="eraser.png").subsample(12, 12)
        self.button_eraser = tk.Button(self.down_frame, 
                            image=self.image_eraser, 
                            height=50, width=50, 
                            command=self.eraser)
        self.button_eraser.grid(row=0, column=7, padx=(10, 10))

        self.image_save = tk.PhotoImage(file="save.png").subsample(12, 12)
        self.button_save_image = tk.Button(self.down_frame, 
                                image=self.image_save, 
                                height=50, width=50, 
                                command=self.save_image)
        self.button_save_image.grid(row=0, column=8, padx=(10, 10))

    def open_image(self):
        self.filepath = filedialog.askopenfilename(title="Open Image File", filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.gif;*.bmp")])
        if self.filepath:
            self.image = Image.open(self.filepath)
            self.image = self.image.resize((self.Width, self.Height), Image.LANCZOS)
            self.image = ImageTk.PhotoImage(self.image)
            self.working_space.create_image(0, 0, anchor="nw", image=self.image)

        self.drawings = []
        self.rotation_angle = 0
        self.is_flipped = False

    def filtered_image(self, filter):
        try:
            if self.is_flipped == True:
                copied_image = Image.open(self.filepath).transpose(Image.FLIP_LEFT_RIGHT)
                copied_image = copied_image.rotate(self.rotation_angle)

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
                copied_image = Image.open(self.filepath)
                copied_image = copied_image.rotate(self.rotation_angle)

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
        except:
            showerror(title='Ошибка', message='Невозможно применить фильтр')
        copied_image = copied_image.resize((self.Width, self.Height), Image.LANCZOS)
        self.photo_image = ImageTk.PhotoImage(copied_image)
        self.working_space.create_image(0, 0, anchor="nw", image=self.photo_image)

        for drawing in self.drawings:
            x1, y1, x2, y2 = drawing
            self.working_space.create_oval(x1, y1, x2, y2, 
                                        fill=self.pen_color, 
                                        outline="", 
                                        width=self.pen_size, 
                                        tags="drawing")
        if self.rotation_angle!=0:
            self.working_space.delete("drawing")
        if self.is_flipped == True:
            self.working_space.delete("drawing")

    def image_flip(self):
        try:
            self.image = Image.open(self.filepath)
            rotated_image = self.image.rotate(self.rotation_angle + 90)
            self.rotation_angle += 90

            if self.rotation_angle % 360 == 0:
                self.rotation_angle = 0
                rotated_image = self.image

            rotated_image = rotated_image.resize((self.Width, self.Height), Image.LANCZOS)
            self.photo_image = ImageTk.PhotoImage(rotated_image)
            self.working_space.delete("drawing")
            self.working_space.create_image(0, 0, anchor="nw", image=self.photo_image)
            self.filtered_image(self.filter_for_image.get())

        except:
            showerror(title='Ошибка переворачивания', message='Выберите картинку для переворачивания')
        
        if self.is_flipped == True:
            for drawing in self.drawings:
                x1, y1, x2, y2 = drawing
                x_center, y_center = (x1 + x2) / 2 - self.Width / 2, (y1 + y2) / 2 - self.Height / 2
                new_x_center = x_center * math.cos(math.radians(self.rotation_angle + 180 )) - y_center * math.sin(math.radians(self.rotation_angle + 180))
                new_y_center = x_center * math.sin(math.radians(self.rotation_angle)) + y_center * math.cos(math.radians(self.rotation_angle))
                new_x1, new_y1 = new_x_center + self.Width / 2 - (x2 - x1) / 2, new_y_center + self.Height / 2 - (y2 - y1) / 2
                new_x2, new_y2 = new_x_center + self.Width / 2 + (x2 - x1) / 2, new_y_center + self.Height / 2 + (y2 - y1) / 2
                self.working_space.create_oval(new_x1, new_y1, new_x2, new_y2, 
                                        fill=self.pen_color, 
                                        outline="", 
                                        width=self.pen_size, 
                                        tags="drawing")
        else:
            for drawing in self.drawings:
                x1, y1, x2, y2 = drawing
                x_center, y_center = (x1 + x2) / 2 - self.Width / 2, (y1 + y2) / 2 - self.Height / 2
                new_x_center = x_center * math.cos(math.radians(self.rotation_angle )) - y_center * math.sin(math.radians(self.rotation_angle + 180))
                new_y_center = x_center * math.sin(math.radians(self.rotation_angle + 180)) + y_center * math.cos(math.radians(self.rotation_angle))
                new_x1, new_y1 = new_x_center + self.Width / 2 - (x2 - x1) / 2, new_y_center + self.Height / 2 - (y2 - y1) / 2
                new_x2, new_y2 = new_x_center + self.Width / 2 + (x2 - x1) / 2, new_y_center + self.Height / 2 + (y2 - y1) / 2
                self.working_space.create_oval(new_x1, new_y1, new_x2, new_y2, 
                                        fill=self.pen_color, 
                                        outline="", 
                                        width=self.pen_size, 
                                        tags="drawing")

    def draw(self, event):
        if self.filepath and self.draw_enabled:
            if self.is_flipped==True:
                x1, y1 = (event.x - self.pen_size), (event.y - self.pen_size)
                x2, y2 = (event.x + self.pen_size), (event.y + self.pen_size)
                drawing_coords = (self.Width - x1, y1, self.Width - x2, y2)
                self.drawings.append(drawing_coords)
                self.working_space.create_oval(x1, y1, x2, y2, 
                                        fill=self.pen_color, 
                                        outline="", 
                                        width=self.pen_size, 
                                        tags="drawing")
            else:
                x1, y1 = (event.x - self.pen_size), (event.y - self.pen_size)
                x2, y2 = (event.x + self.pen_size), (event.y + self.pen_size)
                drawing_coords = (x1, y1, x2, y2)
                self.drawings.append(drawing_coords)
                self.working_space.create_oval(x1, y1, x2, y2, 
                                        fill=self.pen_color, 
                                        outline="", 
                                        width=self.pen_size, 
                                        tags="drawing")

                

    def toggle_draw(self):
        self.draw_enabled = not self.draw_enabled

    def change_color(self):
        self.pen_color = colorchooser.askcolor(title="Выберите цвет ручки")[1]

    def photo_mirror(self):
        try:
            if not self.is_flipped:
                self.image=Image.open(self.filepath).rotate(self.rotation_angle)
                self.image =self.image.transpose(Image.FLIP_LEFT_RIGHT)
                self.is_flipped = True
            else:
                self.image=Image.open(self.filepath).rotate(self.rotation_angle)
                self.is_flipped = False
            if self.is_flipped == True:
                angle = 180
            else:
                angle = 0


            self.image = self.image.resize((self.Width, self.Height), Image.LANCZOS)
            self.photo_image = ImageTk.PhotoImage(self.image)
            self.working_space.create_image(0, 0, anchor="nw", image=self.photo_image)
            self.working_space.delete("all")

            self.filtered_image(self.filter_for_image.get())

        except:
            showerror(title='Нельзя отзеркалить', message='Выберите фотографию для отзеркаливания!')
        for drawing in self.drawings:
                x1, y1, x2, y2 = drawing
                x_center, y_center = (x1 + x2) / 2 - self.Width / 2, (y1 + y2) / 2 - self.Height / 2
                new_x_center = x_center * math.cos(math.radians(angle)) - y_center * math.sin(math.radians(angle))
                new_y_center = x_center * math.sin(math.radians(0)) + y_center * math.cos(math.radians(0))
                new_x1, new_y1 = new_x_center + self.Width / 2 - (x2 - x1) / 2, new_y_center + self.Height / 2 - (y2 - y1) / 2
                new_x2, new_y2 = new_x_center + self.Width / 2 + (x2 - x1) / 2, new_y_center + self.Height / 2 + (y2 - y1) / 2
                self.working_space.create_oval(new_x1, new_y1, new_x2, new_y2, 
                                        fill=self.pen_color, 
                                        outline="", 
                                        width=self.pen_size, 
                                        tags="drawing")

    def thin_size(self):
        self.pen_size = 1
        self.choice_size.destroy()

    def middle_size(self):
        self.pen_size = 3
        self.choice_size.destroy()

    def bold_size(self):
        self.pen_size = 5
        self.choice_size.destroy()

    def change_pen_size(self):
        self.choice_size = tk.Toplevel()
        self.choice_size.title("Выберите толщину линии")
        self.choice_size.geometry("400x200")

        image_thin_line = tk.PhotoImage(file="thin.png").subsample(12, 12)
        self.button_thin=tk.Button(self.choice_size,
                        image=image_thin_line, 
                        height=50, width=50, 
                        command=self.thin_size)
        self.button_thin.image =image_thin_line
        self.button_thin.pack(anchor="center", expand=1)
        
        image_middle_line = tk.PhotoImage(file="middle.png").subsample(12, 12)
        self.button_middle=tk.Button(self.choice_size,
                            image=image_middle_line, 
                            height=50, width=50, 
                            command=self.middle_size)
        self.button_middle.image =image_middle_line
        self.button_middle.pack(anchor="center", expand=1)

        image_bold_line = tk.PhotoImage(file="bold.png").subsample(12, 12)
        self.button_bold=tk.Button(self.choice_size,
                        image=image_bold_line, 
                        height=50, 
                        width=50, 
                        command=self.bold_size)
        self.button_bold.image =image_bold_line
        self.button_bold.pack(anchor="center", expand=1)

    def eraser(self):
        self.working_space.delete("drawing")
        self.drawings=[]

    def save_image(self):
        if self.filepath:
            image_for_save = ImageGrab.grab(bbox=(self.working_space.winfo_rootx(), 
                                                self.working_space.winfo_rooty(), 
                                                self.working_space.winfo_rootx() + self.working_space.winfo_width(),
                                                self.working_space.winfo_rooty() + self.working_space.winfo_height()))
            if self.is_flipped or self.rotation_angle % 360 != 0:

                image_for_save = image_for_save.resize((self.Width, self.Height), Image.LANCZOS)

                if self.is_flipped:
                    image_for_save = image_for_save.transpose(Image.FLIP_LEFT_RIGHT)

                if self.rotation_angle % 360 != 0:
                    image_for_save = image_for_save.rotate(self.rotation_angle)

                self.filepath = self.filepath.split(".")[0] + "_mod.jpg"

            self.filepath = filedialog.asksaveasfilename(defaultextension=".jpg")

            if self.filepath:

                if askyesno(title='Сохранение фотографии', message='Вы хотите сохранить фотографию?'):
                    image_for_save.save(self.filepath)

if __name__ == "__main__":
    app = PhotoEditorApp()
    app.mainloop()