import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox

from PIL import Image, ImageDraw


class DrawingApp:
    __sizes = [1, 2, 5, 10]  # Список предопределённых размеров кисти
    __size_brush = 0  # Задаёт размер линии для рисования

    def __init__(self, root):
        self.root = root
        self.root.title("Рисовалка с сохранением в PNG")

        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

        self.canvas = tk.Canvas(root, width=600, height=400, bg='white')
        self.canvas.pack()

        self.setup_ui()

        self.last_x, self.last_y = None, None
        self.pen_color = 'black'

        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)

    def setup_ui(self):
        '''
        Этот метод отвечает за создание и расположение виджетов управления
        :return:
        '''
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill=tk.X)

        clear_button = tk.Button(control_frame, text="Очистить", command=self.clear_canvas)
        clear_button.pack(side=tk.LEFT)

        color_button = tk.Button(control_frame, text="Выбрать цвет", command=self.choose_color)
        color_button.pack(side=tk.LEFT)

        # Создание кнопки ластика
        eraser_button = tk.Button(control_frame, text="Ластик", command=self.erase_canvas)
        eraser_button.pack(side=tk.LEFT)

        save_button = tk.Button(control_frame, text="Сохранить", command=self.save_image)
        save_button.pack(side=tk.LEFT)

        self.brush_size_scale = tk.Scale(control_frame, from_=1, to=10, orient=tk.HORIZONTAL,
                                         command=self.callback_scale)
        self.brush_size_scale.pack(side=tk.LEFT)

        variable = tk.StringVar(self.root)
        variable.set('Размер кисти')
        size_list_brushes = tk.OptionMenu(control_frame, variable, *self.__sizes,
                                          command=self.callback_option_menu)
        size_list_brushes.pack(side=tk.LEFT)

    def erase_canvas(self):
        '''
        Функция применяется для установки цвета фона для реализации ластика
        :return:
        '''
        self.pen_color = 'white'

    def callback_option_menu(self, parametr):
        '''
        Устанавливает размер линии из выпадающего списка размеров
        :param parametr:
        :return:
        '''
        self.__size_brush = parametr

    def callback_scale(self, parametr):
        '''
        Установить размер кисти ползунком
        :param parametr:
        :return:
        '''
        self.__size_brush = parametr

    def paint(self, event):
        '''
        Функция вызывается при движении мыши с нажатой левой кнопкой по холсту. Она рисует линии на холсте Tkinter и параллельно на объекте Image из Pillow
        :param event:
        :return:
        '''

        if self.last_x and self.last_y:
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                    width=self.__size_brush, fill=self.pen_color,
                                    capstyle=tk.ROUND, smooth=tk.TRUE)
            self.draw.line([self.last_x, self.last_y, event.x, event.y], fill=self.pen_color,
                           width=self.brush_size_scale.get())

        self.last_x = event.x
        self.last_y = event.y

    def reset(self, event):
        '''
        Сбрасывает последние координаты кисти.
        Это необходимо для корректного начала новой линии после того, как пользователь отпустил кнопку мыши и снова начал рисовать.
        :param event:
        :return:
        '''
        self.last_x, self.last_y = None, None

    def clear_canvas(self):
        '''
        Очищает холст, удаляя все нарисованное, и пересоздает объекты Image и ImageDrawдля нового изображения.
        :return:
        '''
        self.canvas.delete("all")
        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

    def choose_color(self):
        '''
        Открывает стандартное диалоговое окно выбора цвета и устанавливает выбранный цвет как текущий для кисти.
        :return:
        '''
        self.pen_color = colorchooser.askcolor(color=self.pen_color)[1]

    def save_image(self):
        '''
        Позволяет пользователю сохранить изображение, используя стандартное диалоговое окно для сохранения файла.
        Поддерживает только формат PNG. В случае успешного сохранения выводится сообщение об успешном сохранении.
        :return:
        '''
        file_path = filedialog.asksaveasfilename(filetypes=[('PNG files', '*.png')])
        if file_path:
            if not file_path.endswith('.png'):
                file_path += '.png'
            self.image.save(file_path)
            messagebox.showinfo("Информация", "Изображение успешно сохранено!")


def main():
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
